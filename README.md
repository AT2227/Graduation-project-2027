# WiFi CSI-Based Through-Wall Human Activity & Fall Detection

## Overview

This repository contains the work for our Computer and Communication Engineering graduation project.

The project aims to develop a **non-invasive human sensing system** capable of detecting human presence, monitoring activities, and identifying fall events through walls using **WiFi Channel State Information (CSI)** and **Machine Learning**.

Unlike traditional monitoring systems that rely on cameras, microphones, or wearable devices, this system leverages existing WiFi infrastructure to perform passive sensing while preserving user privacy.

---

## Project Objectives

* Understand WiFi Channel State Information (CSI) and its applications.
* Collect CSI data using WiFi-enabled embedded devices.
* Process and clean CSI measurements using Digital Signal Processing techniques.
* Train Machine Learning models to recognize human activities and detect falls.
* Develop a real-time monitoring dashboard with alert capabilities.
* Evaluate the system under different indoor environments and scenarios.

---

## System Overview

```text
WiFi Router
      │
      ▼
WiFi OFDM Packets
      │
      ▼
CSI Collection (ESP32 / Raspberry Pi)
      │
      ▼
Signal Processing
      │
      ▼
Feature Extraction
      │
      ▼
Machine Learning
      │
      ▼
Activity & Fall Detection
      │
      ▼
Dashboard / Alerts
```

---

## Technology Stack


## Repository Structure

```text
.
├── docs/               # Literature review, notes, reports
├── research/           # Papers, summaries, references
├── datasets/           # Collected and processed CSI datasets
├── hardware/           # Hardware setup and configurations
├── software/           # Source code
├── models/             # Trained machine learning models
├── experiments/        # Testing scripts and results
├── presentations/      # Presentation slides
└── README.md
```

---

## Current Status

**Phase 1 — Research & Planning**

The project is currently focused on:

* Understanding WiFi communication fundamentals.
* Studying Channel State Information (CSI).
* Reviewing related research papers.
* Designing the overall system architecture.
* Preparing the implementation roadmap.

---

## Learning Roadmap

The primary topics to be studied include:

* Wireless Communications
* IEEE 802.11 WiFi
* OFDM
* Wireless Propagation & Multipath
* Channel State Information (CSI)
* Digital Signal Processing (DSP)
* Machine Learning
* Embedded Systems
* Raspberry Pi & ESP32 Development
* Real-Time System Integration

---

## Team

Graduation Project Team

Computer and Communication Engineering

Alexandria National University (ANU)

---

## License

This repository is intended for educational and academic purposes as part of our graduation project.
