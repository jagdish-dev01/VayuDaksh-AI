# VAYUDAKSH — Demo & Testing Guide

This guide explains how to present and test the VAYUDAKSH system, specifically the functional **Tag Scanner** mode.

## 1. Running the System Locally
Ensure your backend and frontend servers are running:
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 2. Using the "Test Tags" Feature (No Drone Required)
You can test the computer vision pipeline right at your desk using the built-in simulator.
1. Open the UI at `http://localhost:5173`.
2. Click **Test Tags** in the top right corner.
3. Select **Boxes** to display a grid of QR codes on your monitor.
4. Set Video Source to **Simulation**.
5. Set Tracking Mode to **Tag Scanner**.
6. The simulator will synthesize a drone flying past the tags and registering them in the `QR Inventory` sidebar.

## 3. Testing with a Real Raspberry Pi Camera
1. Ensure your Raspberry Pi is connected to the same Wi-Fi network.
2. In the UI, set Video Source to **Drone Camera**.
3. Open the **Test Tags** modal on your computer screen.
4. Point the physical Raspberry Pi camera at your monitor.
5. Watch the bounding boxes appear on the HUD and the tags lock into the persistent **QR Inventory** list!

**Note on Timers**: The `Start Mission` button currently uses a simulated time-based clock. If you wish to freely scan tags for an extended period with the real drone camera, leave the mission in `STANDBY` mode. The scanner will run indefinitely.

## 4. The "AI Vision" Mode
Clicking `AI Vision` will display an "Under Construction" modal, explicitly outlining that the YOLO-based visual pipeline is slated for Phase 2, while the current active system is the Tag Scanner.
