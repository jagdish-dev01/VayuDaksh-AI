# VAYUDAKSH Command Center — UI / UX Specification

## 1. Design Philosophy & Aesthetic Vision

The **VAYUDAKSH Ground Control Station (GCS)** is designed to evoke the high-tech aesthetics of **DJI Enterprise, Tesla Autopilot, Boston Dynamics, and SpaceX Mission Control**. 

### Key Principles:
- **Aerospace / Cyber-Industrial Aesthetic**: High-contrast dark mode with glowing neon cyan, emerald green, warning crimson, and caution amber accents.
- **Glassmorphism with Depth**: Multi-layered semi-transparent dark glass containers (`backdrop-filter: blur(16px)`), subtle 1px border glows, and soft drop shadows.
- **Zero Clutter, High Information Density**: Critical mission metrics, live video with augmented reality HUD, interactive 2D digital twin map, and real-time inventory telemetry are instantly visible without overwhelming the operator.
- **Dynamic Interaction & Micro-Animations**: Smooth pulsing waypoint markers, animated artificial horizon, scanning laser crosshairs, live counter transitions, and alert flash animations.

---

## 2. Design Tokens & Color Palette

```css
:root {
  /* Backgrounds */
  --bg-space: #060911;
  --bg-surface: #0a0f1d;
  --bg-surface-elevated: #111a30;
  --bg-glass: rgba(13, 22, 44, 0.75);
  --bg-glass-card: rgba(18, 28, 56, 0.65);
  
  /* Borders & Glows */
  --border-subtle: rgba(0, 240, 255, 0.15);
  --border-active: rgba(0, 240, 255, 0.6);
  --glow-cyan: 0 0 20px rgba(0, 240, 255, 0.35);
  --glow-crimson: 0 0 20px rgba(255, 51, 102, 0.45);
  --glow-green: 0 0 25px rgba(0, 255, 136, 0.35);
  
  /* Brand & Accent Colors */
  --cyan-bright: #00f0ff;
  --cyan-dim: #0099aa;
  --green-neon: #00ff88;
  --green-dim: #009955;
  --crimson-alert: #ff3366;
  --amber-warning: #ffaa00;
  --purple-accent: #a855f7;
  
  /* Typography Colors */
  --text-primary: #f0f6fc;
  --text-secondary: #94a3b8;
  --text-muted: #64748b;
  --text-highlight: #38bdf8;
  
  /* Fonts */
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Roboto Mono', monospace;
  --font-display: 'Inter', 'Outfit', -apple-system, sans-serif;
}
```

---

## 3. Screen Layout Grid & Component Hierarchy

The dashboard utilizes a responsive 3-column aerospace command layout:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│  HEADER: VAYUDAKSH LOGO | MISSION: WAREHOUSE INSPECTION | STATUS: AUTO_INSPECT | CONTROLS | CLOCK │
├──────────────────────────────────────────────────────┬───────────────────────────────────────────┤
│                                                      │  TOP RIGHT: 2D DIGITAL TWIN WAREHOUSE MAP  │
│                                                      │  • Aisle A & B Shelves (A1, A2, B1, B2)   │
│  LEFT PANEL: LIVE DRONE VIDEO & AEROSPACE HUD        │  • Live Drone Position & Field-of-View    │
│                                                      │  • Active Waypoint Path Trail             │
│  • High-Res Annotated Stream (Pi / Drone / Sim)      ├───────────────────────────────────────────┤
│  • Augmented Reality Bounding Boxes & Confidence %   │  MID RIGHT: INVENTORY MATRIX & SAFETY     │
│  • Artificial Horizon (Pitch / Roll / Yaw)           │  • Shelf Inventory Count vs Manifest      │
│  • Altitude Tape (Laser Rangefinder) & Speed Tape    │  • Damaged Item Indicators                │
│  • Optical Flow Lock & Battery Gauge                 │  • Fire Extinguisher & Exit Sign Radar    │
│  • Stream Source Switcher & Overlay Toggles          ├───────────────────────────────────────────┤
│                                                      │  BOTTOM RIGHT: REAL-TIME ANOMALY LOG      │
│                                                      │  • Timestamped Alerts with Audio Cues     │
├──────────────────────────────────────────────────────┴───────────────────────────────────────────┤
│  FOOTER: 8-STAGE INTERACTIVE GUIDED DEMO STEPPER (STAGES 1–8 FOR JUDGES) + EXECUTIVE REPORT CTA  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Detailed Component Specifications

### 4.1 Header (`Header.jsx`)
- **Left**: Glowing VAYUDAKSH eagle-drone emblem + title: `VAYUDAKSH // AUTONOMOUS INDOOR INSPECTION SYSTEM`.
- **Center**: Active Mission Pill (`STANDBY` [Gray] -> `INSPECTION ACTIVE` [Pulsing Blue] -> `ANOMALY DETECTED` [Crimson] -> `COMPLETED` [Emerald Green]) + Elapsed Mission Timer (`02:34`).
- **Right**:
  - Voice Annunciator Toggle (`VOICE: ON/OFF` with speaker wave icon).
  - Video Source Selector (`SIMULATED FLIGHT`, `LIVE WEBCAM`, `PI ZERO 2 W`).
  - Action Buttons: `START MISSION`, `RETURN TO LAUNCH (RTL)`, `EMERGENCY LAND`, `AI SUMMARY REPORT`.

### 4.2 Live Video & Aerospace HUD (`VideoHUD.jsx`)
- **Viewport Frame**: High-resolution video stream with dark cyber-corner brackets (`┌ ┐ └ ┘`).
- **Artificial Horizon**: Center pitch-ladder and roll-indicator with cyan waterline.
- **Left Tape**: Laser Rangefinder Altitude indicator (`ALT: 1.84m` with bar graph).
- **Right Tape**: Optical Flow Ground Speed indicator (`SPD: 0.42 m/s`).
- **Top Overlay**: Camera FPS (`30.0 FPS`), Latency (`18ms`), Optical Flow Lock (`LOCK 99%`), Link RSSI (`-42 dBm`), GPS-Denied Mode (`GPS-DENIED / INDOOR ODOMETRY ACTIVE`).
- **Bottom HUD Bar**: Detected Shelf ID (`ACTIVE SHELF: SHELF A1`), Current Box Count (`DETECTED: 10 BOXES`), Active Target Mode.
- **Controls Bar**: Checkbox toggles for `YOLO BBoxes`, `AprilTag Grids`, `Damage Overlay`, `HUD Overlays`.

### 4.3 2D Interactive Digital Twin Warehouse Map (`WarehouseMap.jsx`)
- **Visual Style**: Clean architectural schematic grid representing the indoor facility.
- **Shelves**:
  - `Shelf A1` & `Shelf A2` (Aisle A).
  - `Shelf B1` & `Shelf B2` (Aisle B).
  - Safety Station 1 (Fire Extinguisher & First Aid).
  - Emergency Exit North.
  - Drone Docking Base Station (Home/Landing pad).
- **Interactive Drone Avatar**:
  - Rotates dynamically matching drone yaw.
  - Casts an animated field-of-view (FOV) cone illuminating the inspected shelf.
  - Leaves a glowing cyan breadcrumb flight trail.
  - Active inspected shelf glows with an emerald or crimson outline based on status.

### 4.4 Inventory Matrix & Safety Status (`InventoryMatrix.jsx` & `SafetyCompliance.jsx`)
- **Inventory Matrix Table**:
  - Columns: `Shelf ID`, `Target Item`, `Expected`, `Detected Count`, `Health Status`, `Action`.
  - Shelf A1: `Boxes` | `10` | `10` | `✓ MATCH (100%)` | Normal
  - Shelf A2: `Boxes` | `8` | `8` | `✓ MATCH (100%)` | Normal
  - Shelf B1: `Boxes` | `12` | `12` | `✓ MATCH (100%)` | Normal
  - Shelf B2: `Boxes` | `10` | `9` | `⚠ MISMATCH (-1)` | `1 DAMAGED PACKAGE`
- **Safety Compliance Radar**:
  - Fire Extinguisher: `[PASS ✓]` (98% Confidence)
  - Emergency Exit Signs: `[PASS ✓]` (99% Clear)
  - PPE Compliance: `[PASS ✓]` (Worker Helmets/Vests detected)

### 4.5 Live Anomaly & Alert Log (`AlertLog.jsx`)
- Terminal-style live stream of detected events.
- Color-coded severity badges:
  - `[INFO]` Cyan: `Shelf A1 localized via AprilTag 36h11 (ID: 0)`
  - `[SUCCESS]` Green: `Shelf A1 inventory verified: 10/10 items`
  - `[WARNING]` Amber: `Inventory count discrepancy at Shelf B2: Expected 10, Counted 9`
  - `[CRITICAL]` Red: `Damaged package detected at Shelf B2 (Red Tag / Structural Defect)`
- Clicking any alert highlights the shelf on the 2D map and snapshots the evidence frame.

### 4.6 8-Stage Interactive Guided Demo Stepper (`DemoFlowController.jsx`)
- Fixed bottom controller enabling the presenter to trigger or advance through the 8 stages of the judge pitch:
  1. `1. Mission Assignment` (Set up warehouse mission, drone in standby)
  2. `2. Live Stream` (Pi Camera feed & flight HUD online)
  3. `3. AI YOLO Detections` (Person, Box, Fire Extinguisher, Laptop)
  4. `4. AprilTag Localization` (Tags A1 -> B2 spatial navigation)
  5. `5. Inventory Counting` (10 boxes counted -> 9 boxes mismatch alert)
  6. `6. Damage Detection` (Green normal vs Red damaged package flagged)
  7. `7. Safety Audit` (Fire extinguisher presence & emergency exit check)
  8. `8. AI Executive Report` (Display AI summary & download PDF)

### 4.7 Executive AI Summary & PDF Modal (`ExecutiveReportModal.jsx`)
- High-impact modal that presents the inspection as an **Enterprise AI Product**:
  - **Mission Summary**: Completed in `2 min 34 sec` | Area: `Zone Alpha Warehouse`
  - **Warehouse Coverage**: `95.8%`
  - **Total Inventory Verified**: `39 / 40 Boxes` (97.5% integrity)
  - **Defective / Damaged Packages**: `1 item flagged at Shelf B2`
  - **Safety Compliance Audit**: `PASS (All fire extinguishers & exits clear)`
  - **AI Actionable Recommendations**:
    1. *Replace damaged package at Shelf B2 (Defect ID: #DMG-882).*
    2. *Restock missing inventory unit at Shelf B2 (Deficit: 1 box).*
    3. *Schedule re-inspection for Aisle B after restocking.*
  - **Export Options**: `Download Signed PDF Report`, `Export JSON Telemetry`, `Close`.

---

## 5. Accessibility & Performance Considerations

- **Keyboard Shortcuts**: `Space` (Start/Pause Mission), `1-8` (Jump to Demo Stage), `R` (Open Report), `M` (Mute Voice), `Esc` (Close Modal).
- **Reduced Motion Support**: `@media (prefers-reduced-motion: reduce)` disables background pulsing and continuous rotating effects.
- **High Contrast**: Text contrast ratios exceed WCAG AA standards (4.5:1 for body text, 3:1 for large headers).
- **Zero Heavy External Dependencies**: No Tailwind, no bulky 3D engine overhead. Fast, lightweight 60 FPS performance.
