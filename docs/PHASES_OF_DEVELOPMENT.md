# VAYUDAKSH — Development Phases & Milestone Roadmap

This document outlines the engineering roadmap for the **VAYUDAKSH Autonomous Warehouse Inspection Drone System & Command Center**.

---

## 🚀 Phase 1: Tag Scanner Mode & Edge Infrastructure (COMPLETED)
**Objective**: Build a robust, end-to-end telemetry and inventory tracking system using visual markers (QR/AprilTags).

### Features Delivered:
- **FastAPI Backend & WebSockets**: Low-latency telemetry and command bridge.
- **UDP Video Pipeline**: Raspberry Pi Zero 2 W `rpicam-vid` UDP stream mapped seamlessly into the OpenCV backend thread.
- **Persistent QR Inventory Registry**: A global memory state that logs unique tags as they are scanned in real-time.
- **Aerospace-Grade Dashboard**: React + Vite frontend featuring glassmorphism, responsive data matrices, and a high-tech dark theme.
- **Dynamic 2D Floorplan**: Context-aware map that updates dynamically based on the active tracking mode.
- **Test Tags Modal**: Integrated digital marker generator for easy testing without physical printing.
- **Offline Simulation**: Built-in 3D renderer fallback for testing when the physical drone is disconnected.

---

## 🚧 Phase 2: AI Vision Engine (UNDER CONSTRUCTION)
**Objective**: Transition from marker-based identification to pure AI-based object detection and safety compliance auditing.

### Planned Features:
- **YOLOv8/v11 Object Detection**: Count unmarked cardboard boxes directly.
- **Defect Detection**: Identify crushed, water-damaged, or improperly stacked boxes.
- **Safety Compliance**: Recognize blocked fire extinguishers, missing hardhats, and unsealed hazardous materials.
- **Warehouse Digital Twin**: Complete mapping of Shelves A1, A2, B1, and B2.

---

## 🚁 Phase 3: Autonomous Flight Control (FUTURE)
**Objective**: Integrate the dashboard with physical drone flight controllers via MAVLink.

### Planned Features:
- **Pixhawk/ArduPilot Integration**: Send GPS/Optical Flow waypoints directly from the dashboard.
- **Real-Time RTL (Return To Launch)**: Emergency override buttons mapped to MAVLink commands.
- **Automated Mission Auto-Complete**: Use MAVLink `MISSION_ITEM_REACHED` triggers to advance dashboard stages automatically, replacing the current time-based simulation.
