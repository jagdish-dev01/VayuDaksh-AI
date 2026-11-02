# VAYUDAKSH Codebase Structure & Modularity Guidelines

## 1. Core Architectural Guidelines

To ensure maintainability, rapid debugging, and zero code bloat during live demonstrations, the codebase strictly adheres to the following principles:

1. **Single Responsibility Principle (SRP)**: Each file has exactly one clear responsibility (e.g., vision detection, HUD overlay rendering, map visualization, WebSocket management).
2. **File Size Limit (< 150–200 Lines)**: No single file should exceed 200 lines. Monolithic spaghetti components are decomposed into focused sub-components and custom hooks/services.
3. **Clean Decoupling**: Backend vision algorithms operate as independent engines with standardized input/output interfaces (`FrameData -> DetectionResult`). The frontend consumes these via standardized WebSocket contracts.
4. **Zero Unnecessary Dependencies**: Vanilla CSS tokens, native Web Speech API for voice, native Canvas/SVG for high-speed HUD & map rendering, OpenCV DNN for fast CPU inference.

---

## 2. Directory Tree & File Inventory

```
/Users/apple/.gemini/antigravity/scratch/vayudaksh-system/
├── backend/
│   ├── main.py                     # [~140 lines] FastAPI server, CORS, WebSocket hub, MJPEG stream endpoint
│   ├── config.py                   # [~40 lines]  Global settings (ports, thresholds, camera sources, manifest)
│   ├── vision/
│   │   ├── __init__.py             # [~10 lines]  Vision module exports
│   │   ├── detector.py             # [~110 lines] Master vision pipeline coordinator (combines all sub-engines)
│   │   ├── yolo_engine.py          # [~130 lines] Real-time YOLOv8/v11 inference (Box, Person, Safety assets)
│   │   ├── marker_engine.py        # [~120 lines] AprilTag 36h11 & ArUco detector (Shelf A1, A2, B1, B2)
│   │   ├── inventory_engine.py     # [~90 lines]  Dynamic box counting & manifest discrepancy tracker
│   │   ├── damage_engine.py        # [~90 lines]  Package damage & defect classifier (red tag / crush)
│   │   ├── safety_engine.py        # [~80 lines]  Safety equipment compliance auditor (Extinguisher, Exit)
│   │   └── synthetic_feed.py       # [~160 lines] Autonomous indoor drone flight simulation frame generator
│   ├── telemetry/
│   │   ├── __init__.py             # [~5 lines]   Telemetry module exports
│   │   ├── drone_telemetry.py      # [~110 lines] Flight dynamics state (Alt, Spd, Pitch, Roll, Yaw, Battery)
│   │   └── mission_manager.py      # [~100 lines] Mission state machine (Standby, Navigating, Inspecting, Report)
│   ├── reporting/
│   │   ├── __init__.py             # [~5 lines]   Reporting module exports
│   │   └── report_generator.py     # [~140 lines] ReportLab PDF generator & AI executive summary compiler
│   ├── companion/
│   │   ├── vayudaksh_pi_streamer.py# [~90 lines]  Raspberry Pi Zero 2 W Camera Module V3 streamer
│   │   └── PI_SETUP_GUIDE.md       # Hardware wiring, libcamera, and deployment guide
│   └── utils/
│       ├── __init__.py             # [~5 lines]   Utils module exports
│       ├── draw_hud.py             # [~110 lines] OpenCV HUD annotation rendering on server frames
│       └── marker_generator.py     # [~90 lines]  Generates printable AprilTag & safety sign PNGs/PDF
├── frontend/
│   ├── index.html                  # [~25 lines]  HTML shell with fonts & title
│   ├── package.json                # [~30 lines]  React 18 + Vite dependencies
│   ├── vite.config.js              # [~20 lines]  Vite bundler config & API proxy
│   └── src/
│       ├── main.jsx                # [~15 lines]  React DOM root
│       ├── App.jsx                 # [~130 lines] Main Command Center orchestrator
│       ├── constants.js            # [~50 lines]  Demo stages, shelf manifests, color tokens
│       ├── hooks/
│       │   ├── useTelemetry.js     # [~80 lines]  Custom hook for WebSocket telemetry & state
│       │   ├── useVoiceAnnouncer.js# [~60 lines]  Custom hook for Web Speech API text-to-speech
│       │   └── useDemoStepper.js   # [~70 lines]  Custom hook for Stage 1-8 demo timeline
│       ├── components/
│       │   ├── Header.jsx          # [~90 lines]  Top bar: Brand, Status, Actions, Audio Toggle
│       │   ├── VideoHUD/
│       │   │   ├── VideoHUD.jsx    # [~100 lines] Video container, source switcher & HUD overlays
│       │   │   ├── ArtificialHorizon.jsx # [~70 lines] Pitch ladder, roll indicator & waterline
│       │   │   └── TelemetryTapes.jsx    # [~60 lines] Altitude & speed tapes with bar graphs
│       │   ├── WarehouseMap/
│       │   │   ├── WarehouseMap.jsx# [~120 lines] 2D Digital Twin floorplan with drone & FOV cone
│       │   │   └── ShelfMarker.jsx # [~50 lines]  Individual shelf graphic with status glow
│       │   ├── Inventory/
│       │   │   ├── InventoryMatrix.jsx # [~90 lines] Shelf stock table with counts & mismatch tags
│       │   │   └── SafetyCompliance.jsx# [~80 lines] Fire Extinguisher, Exit, PPE audit gauges
│       │   ├── AlertLog.jsx        # [~80 lines]  Live terminal-style anomaly event stream
│       │   ├── DemoFlowController.jsx # [~110 lines] 8-stage judge presentation bottom bar
│       │   └── Modals/
│       │       ├── ExecutiveReportModal.jsx # [~120 lines] AI Summary dialog & PDF download CTA
│       │       └── MarkerTestModal.jsx      # [~80 lines] Digital AprilTag viewer for mobile scan
│       ├── styles/
│       │   ├── index.css           # [~150 lines] Base dark theme, layout grid, glassmorphism
│       │   ├── hud.css             # [~120 lines] Flight HUD tapes, horizon, scanning crosshairs
│       │   └── animations.css      # [~60 lines]  Pulsing radar, glowing borders, laser beams
│       └── services/
│           ├── websocket.js        # [~70 lines]  Resilient WebSocket client with auto-reconnect
│           └── api.js              # [~60 lines]  FastAPI REST endpoints wrapper
├── docs/
│   ├── ARCHITECTURE.md             # High-level architecture & dataflow
│   ├── SYSTEM_DESIGN.md            # Vision algorithms, detection pipeline & schemas
│   ├── UI_SPEC.md                  # Detailed design tokens, layout & HUD specifications
│   ├── PROJECT_STRUCTURE.md        # File sizing, modularity rules & responsibilities
│   ├── DEMO_GUIDE.md               # 4-5 minute judge presentation script & test protocol
│   └── PI_SETUP_GUIDE.md           # Pi Zero 2 W + Camera Module V3 setup instructions
├── markers/                        # Generated printable AprilTag PNGs & PDF assets
├── run_demo.sh                     # [~35 lines] One-click runner script
└── README.md                       # Comprehensive project guide
```

---

## 3. Module Boundaries & Data Contracts

### 3.1 Backend Vision Contract (`DetectionResult`)
Every vision engine output conforms to this structure:
```json
{
  "active_shelf": "Shelf A1",
  "shelf_confidence": 0.99,
  "objects": [
    {"class": "box", "confidence": 0.96, "bbox": [120, 140, 260, 310]},
    {"class": "person", "confidence": 0.98, "bbox": [400, 80, 520, 420]}
  ],
  "box_count": 10,
  "expected_box_count": 10,
  "is_mismatch": false,
  "damaged_boxes": 0,
  "safety_status": {
    "fire_extinguisher": true,
    "emergency_exit": true,
    "ppe_compliant": true
  },
  "alerts": []
}
```

### 3.2 Backend Telemetry Contract (`TelemetryState`)
```json
{
  "mission_status": "AUTO_INSPECT",
  "flight_mode": "INDOOR_NAV",
  "mission_time_sec": 142,
  "altitude_m": 1.85,
  "speed_mps": 0.45,
  "pitch_deg": 2.1,
  "roll_deg": -1.4,
  "yaw_deg": 88.0,
  "battery_pct": 87,
  "battery_voltage": 11.8,
  "optical_flow_quality": 99,
  "gps_denied": true,
  "drone_position": {"x": 28.5, "y": 62.0}
}
```

---

## 4. Line Count Budget & Refactoring Rules

- **Target Average**: 80–120 lines per file.
- **Maximum Ceiling**: 180 lines per file.
- If a component exceeds 180 lines:
  1. Extract sub-components into a dedicated subfolder (e.g. `VideoHUD/` contains `ArtificialHorizon.jsx` and `TelemetryTapes.jsx`).
  2. Extract data processing into custom hooks (e.g. `useTelemetry.js`, `useVoiceAnnouncer.js`).
  3. Extract static definitions and manifests into `constants.js` or `config.py`.
