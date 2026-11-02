# VAYUDAKSH — System Design & Architecture

## Core Architecture Stack
- **Edge Device (Drone)**: Raspberry Pi Zero 2 W running lightweight Debian.
- **Video Transport**: High-speed UDP streaming (`rpicam-vid` -> `ffmpeg` -> `UDP`).
- **Backend Station**: Python 3.10+, FastAPI, OpenCV, WebSockets.
- **Frontend Dashboard**: React 18, Vite, Tailwind CSS, Lucide Icons.

## Major Components

### 1. Vision Detector (`backend/vision/detector.py`)
The master coordinator for all computer vision. 
- In **Tag Scanner Mode**, it relies on `marker_engine.py` to identify QR codes and ArUco markers.
- In **AI Mode**, it relies on `yolo_engine.py` (Phase 2).
- It injects the resulting data (bounding boxes, IDs) into the video stream as a heads-up display (HUD) via `draw_hud.py`.

### 2. Persistent Inventory Engine (`backend/vision/inventory_engine.py`)
Solves the "live viewfinder" problem. Rather than just returning tags visible in the *current* frame, this engine maintains a persistent `global_tags` dictionary. When the drone scans a new box, its timestamp and ID are locked into memory and streamed to the UI indefinitely until the mission resets.

### 3. UDP Video Ingestion
The system requires a non-blocking `cv2.VideoCapture` thread. The video fetcher runs in a dedicated background `asyncio` worker thread in `main.py` with exponential backoff. This ensures the FastAPI event loop never freezes, even if the drone loses Wi-Fi connection.

### 4. React Dashboard (`frontend/`)
A highly modular component tree featuring:
- **VideoHUD**: Draws crosshairs, pitch ladders, and bounding boxes over the MJPEG stream.
- **RightSidebar**: Dynamically swaps between `QR Inventory List` (for Tag Scanner mode) and `Inventory Matrix` (for AI mode).
- **WarehouseMap**: A 2D SVG map that dynamically alters its layout based on the active tracking mode (e.g., showing a generic "Active Scan Zone" during tag scanning, avoiding crashes associated with hardcoded AI waypoints).
