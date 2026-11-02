# 📹 VAYUDAKSH Camera & Video Stream Setup Guide
### Complete Setup for USB Webcam, Raspberry Pi Companion Computer, and Smartphone IP Streaming

This guide provides step-by-step instructions to connect physical video feeds to the **VAYUDAKSH Ground Control Station (GCS)** web application.

---

## 📑 Table of Contents
1. [Camera Architecture Overview](#1-camera-architecture-overview)
2. [Mode 1: Laptop & USB Webcam Setup](#2-mode-1-laptop--usb-webcam-setup)
3. [Mode 2: Raspberry Pi Drone Companion Computer Setup](#3-mode-2-raspberry-pi-drone-companion-computer-setup)
4. [Mode 3: Smartphone Wireless IP Camera Setup (Quick Test)](#4-mode-3-smartphone-wireless-ip-camera-setup-quick-test)
5. [Connecting & Operating in the Web Dashboard](#5-connecting--operating-in-the-web-dashboard)
6. [Troubleshooting & Diagnostics](#6-troubleshooting--diagnostics)

---

## 1. Camera Architecture Overview

VAYUDAKSH supports 3 real-time optical ingestion modes:

```
                  ┌────────────────────────────────────────┐
                  │ 1. Built-in Simulation Engine          │
                  │    (Internal 8-Stage Autonomous Canvas)│
                  └──────────────────┬─────────────────────┘
                                     │
┌─────────────────────────┐          │          ┌─────────────────────────┐
│ 2. Physical USB Webcam  ├──────────┼──────────┤ 3. Raspberry Pi Stream  │
│    (OpenCV Device /dev) │          │          │    (HTTP MJPEG / RTSP)  │
└─────────────────────────┘          ▼          └─────────────────────────┘
                       ┌───────────────────────────┐
                       │  VAYUDAKSH Vision AI      │
                       │  - YOLO Object Counter    │
                       │  - AprilTag (36h11) SLAM  │
                       │  - Package Defect Engine  │
                       │  - OSHA Safety Auditor    │
                       └─────────────┬─────────────┘
                                     ▼
                       ┌───────────────────────────┐
                       │  VAYUDAKSH GCS Dashboard  │
                       │  http://localhost:5173    │
                       └───────────────────────────┘
```

---

## 2. Mode 1: Laptop & USB Webcam Setup

Use this mode for desk development, algorithmic testing, and verifying computer vision without hardware drones.

### 2.1 Hardware Requirements
* Any built-in laptop camera or external USB Webcam (e.g., Logitech C920 / 720p / 1080p).

### 2.2 Configuration
By default, the webcam device index is set to `0` in [`backend/config.py`](file:///Users/apple/.gemini/antigravity/scratch/vayudaksh-system/backend/config.py):
```python
VIDEO_SOURCES = {
    "simulated": "simulated",
    "webcam": 0,  # Change to 1 or 2 if you have multiple external USB cameras
    "pi_stream": "http://192.168.1.100:8080/stream.mjpg"
}
```

### 2.3 How to Test with Physical Markers
1. Start the VAYUDAKSH servers (`./run_demo.sh` or `npm run dev` + `uvicorn backend.main:app`).
2. Open **[http://localhost:5173](http://localhost:5173)** in your browser.
3. In the top header bar, click **`Webcam`**.
4. Click the **`Tags`** button in the header to view printable **AprilTags** (Tag IDs: 0, 1, 2, 3) and Defect markers.
5. Point your webcam at the screen or printed AprilTag:
   - **Tag 0**: Identified as **Shelf A1 (Sensors & Boards)**
   - **Tag 1**: Identified as **Shelf A2 (Robotics Actuators)**
   - **Tag 2**: Identified as **Shelf B1 (Carbon Fiber Plates)**
   - **Tag 3**: Identified as **Shelf B2 (Lithium Batteries)**
6. Hold up a cardboard box or red defect marker in front of the camera — the AI will detect bounding boxes, package counts, and defect flags in real time.

---

## 3. Mode 2: Raspberry Pi Drone Companion Computer Setup

Use this mode when flying a physical drone inside a warehouse or laboratory.

### 3.1 Hardware Components
* **Companion Computer**: Raspberry Pi 4, Raspberry Pi 5, or Raspberry Pi Zero 2 W.
* **Camera Sensor**: Raspberry Pi Camera Module V2 / V3 (IMX708 Autofocus) or USB Global Shutter Camera.
* **Flight Controller Interface**: Pixhawk / SpeedyBee connected via UART telemetry.

---

### 3.2 Network Configuration
Connect your **Ground Control Station (laptop)** and the **Raspberry Pi** to the **same Wi-Fi network** (or laptop Wi-Fi hotspot).

Find the IP address of your Raspberry Pi:
```bash
# On Raspberry Pi terminal
hostname -I
# Example output: 192.168.1.105
```

---

### 3.3 Installing Dependencies on Raspberry Pi
SSH into the Raspberry Pi:
```bash
ssh pi@192.168.1.105
```

Install Python and OpenCV dependencies:
```bash
sudo apt update && sudo apt install -y python3-pip python3-opencv python3-picamera2
```

---

### 3.4 Deploying the VAYUDAKSH Low-Latency Streamer
Copy the streamer script from your backend to the Raspberry Pi:
```bash
# Run from your laptop terminal inside vayudaksh-system/
scp backend/companion/vayudaksh_pi_streamer.py pi@192.168.1.105:~/vayudaksh_pi_streamer.py
```

Run the video streamer on the Pi:
```bash
# On Raspberry Pi
python3 ~/vayudaksh_pi_streamer.py --port 8080 --width 640 --height 480 --fps 30
```

The camera will begin streaming low-latency video at:
`http://192.168.1.105:8080/stream.mjpg`

---

### 3.5 Auto-Start on Drone Boot (systemd Service)
To ensure video streams automatically when the drone battery is plugged in:

1. Create a systemd service file on the Pi:
```bash
sudo nano /etc/systemd/system/vayudaksh-camera.service
```

2. Paste the following configuration:
```ini
[Unit]
Description=VAYUDAKSH Autonomous Drone Camera Streamer
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/vayudaksh_pi_streamer.py --port 8080 --width 640 --height 480 --fps 30
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vayudaksh-camera.service
sudo systemctl start vayudaksh-camera.service
```

---

### 3.6 Configuring VAYUDAKSH GCS Backend
On your laptop, edit [`backend/config.py`](file:///Users/apple/.gemini/antigravity/scratch/vayudaksh-system/backend/config.py#L46) to set your Pi's IP address:

```python
VIDEO_SOURCES = {
    "simulated": "simulated",
    "webcam": 0,
    "pi_stream": "http://192.168.1.105:8080/stream.mjpg"  # <-- Put your Raspberry Pi IP here
}
```

---

## 4. Mode 3: Smartphone Wireless IP Camera Setup (Quick Test)

If you don't have a Raspberry Pi ready, you can turn any iPhone or Android phone into a wireless drone camera in **60 seconds**:

1. **Android**: Download **IP Webcam** (from Google Play Store).
2. **iPhone**: Download **IP Camera Lite** or **EpocCam** (from App Store).
3. Connect your phone to the same Wi-Fi network as your laptop.
4. Tap **"Start Server"** in the app. The app will display an address (e.g. `http://192.168.1.45:8080/video`).
5. Update `backend/config.py`:
   ```python
   VIDEO_SOURCES = {
       "simulated": "simulated",
       "webcam": 0,
       "pi_stream": "http://192.168.1.45:8080/video"
   }
   ```
6. In the dashboard header, click **`Pi Stream`** — your phone is now acting as a live wireless drone camera!

---

## 5. Connecting & Operating in the Web Dashboard

1. Navigate to **[http://localhost:5173](http://localhost:5173)**.
2. In the top header bar, use the **Camera Source Switcher**:
   - 🛸 **`Simulated`**: Built-in 8-stage automated simulation.
   - 💻 **`Webcam`**: Physical USB/laptop camera.
   - 🍓 **`Pi Stream`**: Live wireless drone stream.
3. In the live video HUD, you can dynamically toggle **Vision Filters**:
   - **`RGB`**: Full daylight color mode.
   - **`FLIR`**: Thermal false-color heatmap simulation.
   - **`NVG`**: High-contrast Night Vision phosphor mode for dark warehouse aisles.

---

## 6. Troubleshooting & Diagnostics

### Q1: Webcam screen is black in Webcam mode.
* **Mac OS**: Ensure terminal/IDE has Camera permissions granted (*System Settings → Privacy & Security → Camera*).
* **Linux**: Ensure your user is in the `video` group: `sudo usermod -aG video $USER`.
* **Multiple Cameras**: If your laptop has multiple cameras or an external USB cam, change `"webcam": 0` to `"webcam": 1` in `backend/config.py`.

### Q2: Pi Stream says connection refused / timeout.
* Check if you can ping the Pi from your laptop: `ping 192.168.1.105`.
* Open `http://<PI_IP>:8080/stream.mjpg` directly in a browser tab to confirm the Pi is broadcasting video.
* Check Pi camera service logs: `sudo journalctl -u vayudaksh-camera -f`.

### Q3: High video latency (> 300ms) over Wi-Fi.
* Lower frame resolution to `640x480` and JPEG quality to `70%` in `vayudaksh_pi_streamer.py`.
* Ensure the drone and laptop are on a 5 GHz Wi-Fi band or direct Wi-Fi hotspot rather than a congested 2.4 GHz office network.
