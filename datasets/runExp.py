import os
import pandas as pd
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights
from sklearn.metrics import classification_report, confusion_matrix


# ==========================================
# 1. CUSTOM DATASET LOADER
# ==========================================
class CSIPresenceDataset(Dataset):

  def __init__(self, image_dir, label_csv, transform=None):
    self.image_dir = image_dir
    self.labels_df = pd.read_csv(label_csv, header=None)  # Format: [index, class]
    self.transform = transform

  def __len__(self):
    return len(self.labels_df)

  def __getitem__(self, idx):
    img_idx = self.labels_df.iloc[idx, 0]
    label = self.labels_df.iloc[idx, 1]

    img_path = os.path.join(self.image_dir, f"{img_idx}.png")
    image = Image.open(img_path).convert("RGB")

    if self.transform:
      image = self.transform(image)

    return image, label


# ==========================================
# 2. EVALUATION FUNCTION
# ==========================================
def evaluate_model(model, loader, device, criterion):
  model.eval()
  total_loss = 0
  correct = 0
  total = 0

  with torch.no_grad():
    for images, labels in loader:
      images, labels = images.to(device), labels.to(device)
      outputs = model(images)
      loss = criterion(outputs, labels)

      total_loss += loss.item() * images.size(0)
      _, predicted = torch.max(outputs.data, 1)
      total += labels.size(0)
      correct += (predicted == labels).sum().item()

  return total_loss / total, correct / total


# ==========================================
# 3. DETAILED REPORT FUNCTION
# ==========================================
def generate_classification_report(model, loader):
  model.eval()
  all_preds = []
  all_labels = []

  device = next(model.parameters()).device

  with torch.no_grad():
    for images, labels in loader:
      images = images.to(device)
      outputs = model(images)
      _, preds = torch.max(outputs, 1)

      all_preds.extend(preds.cpu().numpy())
      all_labels.extend(labels.numpy())

  class_names = [
      "No Presence",
      "Room 1",
      "Room 2",
      "Room 3",
      "Room 4",
      "Room 5",
  ]

  print("\n--- Confusion Matrix ---")
  print(confusion_matrix(all_labels, all_preds))
  print("\n--- Classification Report ---")
  print(
      classification_report(
          all_labels, all_preds, target_names=class_names, zero_division=0
      )
  )


# ==========================================
# 4. MAIN EXECUTION PIPELINE
# ==========================================
if __name__ == "__main__":
  # Define image transforms
  transform = transforms.Compose([
      transforms.Resize((224, 224)),
      transforms.ToTensor(),
      transforms.Normalize(
          mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
      ),
  ])

  # Initialize datasets and dataloaders
  # (Make sure 'DP_NLOS', 'trainLabels.csv', and 'testLabels.csv' are in your working directory)
  print("Loading datasets...")
  train_dataset = CSIPresenceDataset(
      image_dir="DP_NLOS", label_csv="trainLabels.csv", transform=transform
  )
  test_dataset = CSIPresenceDataset(
      image_dir="DP_NLOS", label_csv="testLabels.csv", transform=transform
  )

  train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
  test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

  # Setup model, loss, and optimizer
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  print(f"Using device: {device}")

  model = efficientnet_v2_s(weights=EfficientNet_V2_S_Weights.DEFAULT)
  model.classifier[1] = nn.Linear(model.classifier[1].in_features, 6)
  model = model.to(device)

  criterion = nn.CrossEntropyLoss()
  optimizer = optim.Adam(model.parameters(), lr=1e-4)

  # Quick training loop example (e.g., 1 epoch for testing)
  print("Starting training epoch...")
  model.train()
  for epoch in range(10):  # Increase epochs as needed
    running_loss = 0.0
    for i, (images, labels) in enumerate(train_loader):
      images, labels = images.to(device), labels.to(device)

      optimizer.zero_grad()
      outputs = model(images)
      loss = criterion(outputs, labels)
      loss.backward()
      optimizer.step()

      running_loss += loss.item()
      if i % 10 == 0:
        print(f"Batch {i}/{len(train_loader)} - Loss: {loss.item():.4f}")

  # Run evaluation
  print("\nEvaluating model on test set...")
  test_loss, test_acc = evaluate_model(model, test_loader, device, criterion)
  print(f"Test Loss: {test_loss:.4f} | Test Accuracy: {test_acc * 100:.2f}%")

  # Generate final classification report and confusion matrix
  generate_classification_report(model, test_loader)