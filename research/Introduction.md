# Introduction

**Technologies that detect/track humans wirelessly:**

#### 1. WiFi-Based (your domain)

- **Single WiFi link (your project)** — One transmitter, one receiver. Detects presence & falls in a room.
- **Multi-WiFi / Multi-link** — Multiple routers triangulate position. More accurate localization. (This is what Dr. Ahmed told you to drop — Localization)
- **WiFi RTT (Round Trip Time)** — Measures signal travel time to estimate distance. Used in indoor positioning.
- **802.11bf** — The new 2024 WiFi standard that bakes sensing natively into WiFi hardware. Future of this whole field.

#### 2. GPS

- Outdoor only. Useless indoors. Tracks location, not presence or activity.

#### 3. Radar-Based

- **UWB Radar** — Very accurate, detects breathing, heartbeat, falls. Used in hospitals. Expensive dedicated hardware.
- **mmWave Radar** — Used in phones (Pixel, some iPhones) and smart home devices. Very precise.

#### 4. Cellular / 5G Sensing

- Base stations detect human presence and movement using signal reflections. Emerging research area.

#### 5. Bluetooth

- Short range. Used for proximity detection, not activity sensing.

#### 6. RFID

- Passive tags on objects/people. Detects presence only when tagged.

---

### CSI Data Formats

**Broad context — what exists:**

CSI can be represented in several formats depending on what information you extract and how you process it:

| Format | What it contains | Common use |
| --- | --- | --- |
| **Raw complex (amplitude + phase)** | Full H[k] matrix per subcarrier | Maximum information, needs cleaning |
| **Amplitude only** | ||H[k]|| per subcarrier | Most common in sensing literature |
| **Phase only / phase difference** | ∠H[k], or difference between antennas | Gesture recognition, subtle motion |
| **CSI ratio** | Amplitude ratio between two antennas | Noise reduction, extended range |
| **Spectrogram / time-frequency** | STFT of CSI time series | Fall detection via CNN on images |
| **BVP (Body-coordinate Velocity Profile)** | Doppler-derived, domain-invariant | Cross-environment gesture recognition (Widar) |

**The key trade-offs:**

- Raw phase is unreliable from a single antenna due to random phase offsets — phase *difference* between antennas is stable
- Amplitude is stable and works well for most sensing tasks with simple denoising
- BVP removes environmental dependency but requires more processing