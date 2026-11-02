"""
High-Fidelity Photorealistic Warehouse Scene Generator & Drone Camera Simulator
Renders authentic 3D industrial warehouse scenes with realistic lighting, textures,
drop shadows, metallic steel racks, corrugated shipping boxes, and clear human-readable HUD.
"""
import math
import cv2
import numpy as np

def create_cardboard_texture(w, h, base_color=(75, 135, 195), grain_strength=10):
    """Generates realistic corrugated Kraft cardboard texture with fiber grain and subtle gradients."""
    img = np.full((h, w, 3), base_color, dtype=np.uint8)
    noise = np.random.randint(-grain_strength, grain_strength, (h, w), dtype=np.int16)
    for c in range(3):
        channel = img[:, :, c].astype(np.int16) + noise
        img[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)
    
    # Add subtle vertical corrugation fluting
    for x in range(0, w, 6):
        cv2.line(img, (x, 0), (x, h), (max(0, base_color[0]-8), max(0, base_color[1]-8), max(0, base_color[2]-8)), 1)
        
    # Top-to-bottom ambient shading
    for y in range(h):
        shade = 1.0 - (y / h) * 0.18
        img[y, :] = np.clip(img[y, :].astype(np.float32) * shade, 0, 255).astype(np.uint8)
    return img

class PhotorealisticWarehouseRenderer:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self._init_warehouse_backgrounds()

    def _init_warehouse_backgrounds(self):
        """Pre-computes rich atmospheric warehouse background plates."""
        pass

    def render_warehouse_aisle(self, elapsed_sec, show_worker=False):
        """Renders authentic 3D warehouse corridor with perspective depth, lighting, and moving floor."""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        horizon_y = 200
        vanish_x = 320

        # 1. Atmospheric Ceiling & Background Wall
        for y in range(horizon_y):
            ratio = y / horizon_y
            b = int(25 + 20 * ratio)
            g = int(30 + 22 * ratio)
            r = int(35 + 25 * ratio)
            frame[y, :] = (b, g, r)

        # 2. Polished Concrete Epoxy Warehouse Floor
        for y in range(horizon_y, self.height):
            ratio = (y - horizon_y) / (self.height - horizon_y)
            b = int(45 + 35 * ratio)
            g = int(50 + 38 * ratio)
            r = int(55 + 40 * ratio)
            frame[y, :] = (b, g, r)

        # High-bay warehouse ceiling truss beams
        for tx in range(60, self.width, 130):
            cv2.line(frame, (tx, 0), (vanish_x, horizon_y - 20), (55, 65, 75), 2)

        # High-bay LED floodlights on ceiling
        light_scroll = (elapsed_sec * 60) % 120
        for bz in [-40, 40, 120]:
            ly = int(bz + light_scroll)
            if 10 < ly < horizon_y - 20:
                cv2.ellipse(frame, (vanish_x, ly), (90, 18), 0, 0, 360, (70, 80, 95), -1)
                cv2.circle(frame, (vanish_x, ly), 6, (240, 250, 255), -1)

        # 3. Yellow OSHA Safety Walkway Lines (Receding in 3D Perspective)
        cv2.line(frame, (vanish_x - 30, horizon_y), (40, self.height), (0, 240, 255), 4, cv2.LINE_AA)
        cv2.line(frame, (vanish_x + 30, horizon_y), (600, self.height), (0, 240, 255), 4, cv2.LINE_AA)

        # Moving floor expansion joints
        floor_flow = (elapsed_sec * 90) % 45
        for d in range(10, 240, 28):
            dist = d + floor_flow
            if dist > 235: continue
            py = int(horizon_y + (dist / 240.0)**1.5 * (self.height - horizon_y))
            if py >= self.height: continue
            spread = int(30 + (py - horizon_y) * 1.3)
            x1, x2 = max(0, vanish_x - spread), min(self.width, vanish_x + spread)
            cv2.line(frame, (x1, py), (x2, py), (70, 78, 85), 1, cv2.LINE_AA)

        # 4. Multi-Tier Industrial Pallet Racks on Left and Right Sides
        for side in [-1, 1]:
            x_start = 0 if side == -1 else self.width - 130
            w_rack = 130
            # Upright steel blue pillars
            cv2.rectangle(frame, (x_start, horizon_y - 90), (x_start + w_rack, self.height), (35, 45, 55), -1)
            # Orange horizontal beams
            for beam_y in [horizon_y - 30, horizon_y + 40, horizon_y + 130, horizon_y + 220]:
                if beam_y < self.height:
                    cv2.rectangle(frame, (x_start, beam_y), (x_start + w_rack, beam_y + 14), (20, 115, 225), -1)
                    cv2.rectangle(frame, (x_start, beam_y), (x_start + w_rack, beam_y + 14), (40, 150, 255), 1)

            # Cardboard boxes on side racks
            for by in [horizon_y - 22, horizon_y + 48, horizon_y + 138]:
                if by + 50 < self.height:
                    for bx in range(x_start + 10, x_start + w_rack - 30, 42):
                        cv2.rectangle(frame, (bx, by), (bx + 36, by + 40), (60, 120, 175), -1)
                        cv2.rectangle(frame, (bx + 4, by + 6), (bx + 24, by + 18), (240, 240, 240), -1)

        detections = []

        # 5. Optional Worker in Aisle (Stage 3)
        if show_worker:
            bob = math.sin(elapsed_sec * 3.5) * 3.0
            wx, wy = 380, int(150 + bob)
            # Worker Body & Hi-Vis Orange Vest
            cv2.rectangle(frame, (wx + 10, wy + 90), (wx + 26, wy + 190), (40, 45, 55), -1) # Left leg
            cv2.rectangle(frame, (wx + 32, wy + 90), (wx + 48, wy + 190), (40, 45, 55), -1) # Right leg
            cv2.rectangle(frame, (wx, wy + 25), (wx + 58, wy + 95), (10, 130, 255), -1) # Orange vest
            cv2.rectangle(frame, (wx + 6, wy + 45), (wx + 52, wy + 65), (230, 240, 255), -1) # Reflective stripe
            # Head & Yellow Safety Hardhat
            cv2.circle(frame, (wx + 29, wy + 10), 15, (170, 190, 210), -1)
            cv2.ellipse(frame, (wx + 29, wy + 4), (18, 9), 0, 0, 180, (0, 240, 255), -1)
            detections.append({"class": "person", "confidence": 0.96, "bbox": [wx, wy, wx + 58, wy + 190]})

            # Pallet Staging Boxes in Aisle
            cv2.rectangle(frame, (80, 270), (220, 390), (65, 125, 180), -1)
            cv2.rectangle(frame, (80, 270), (220, 390), (85, 145, 200), 2)
            cv2.rectangle(frame, (100, 290), (160, 330), (245, 245, 245), -1)
            detections.append({"class": "box", "confidence": 0.98, "bbox": [80, 270, 220, 390]})

        return frame, detections

    def render_shelf_inspection(self, shelf_name, elapsed_sec, is_defect=False):
        """
        Renders photorealistic 3D warehouse shelving view with textured corrugated boxes,
        realistic shipping barcodes, steel uprights, and smooth laser scan inspection.
        """
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # 1. Background Warehouse Aisle (Slightly blurred for realistic camera depth-of-field)
        for y in range(self.height):
            ratio = y / self.height
            v = int(28 + 20 * ratio)
            frame[y, :] = (v, v + 2, v + 5)

        # Subtle distant rack silhouettes in background
        cv2.rectangle(frame, (120, 40), (520, 440), (35, 40, 48), -1)

        # 2. Heavy-Duty Industrial Pallet Racking (Foreground 3D Steel)
        # Left Steel Column (Cobalt Blue with realistic bevel highlight)
        cv2.rectangle(frame, (18, 0), (52, self.height), (125, 60, 15), -1)
        cv2.rectangle(frame, (18, 0), (24, self.height), (175, 95, 30), -1) # Highlight
        cv2.rectangle(frame, (46, 0), (52, self.height), (85, 40, 10), -1)  # Shadow
        # Right Steel Column
        cv2.rectangle(frame, (588, 0), (622, self.height), (125, 60, 15), -1)
        cv2.rectangle(frame, (588, 0), (594, self.height), (175, 95, 30), -1)
        cv2.rectangle(frame, (616, 0), (622, self.height), (85, 40, 10), -1)

        # Upright Teardrop Punch Slots
        for py in range(25, self.height - 10, 28):
            cv2.circle(frame, (35, py), 4, (20, 25, 32), -1)
            cv2.circle(frame, (605, py), 4, (20, 25, 32), -1)

        # 3. Horizontal Safety Orange Load Beams (Tier 1 & Tier 2)
        beam_y1 = 210
        beam_y2 = 410

        # Tier 1 Beam (Middle)
        cv2.rectangle(frame, (18, beam_y1), (622, beam_y1 + 18), (15, 105, 220), -1)
        cv2.rectangle(frame, (18, beam_y1), (622, beam_y1 + 4), (40, 150, 255), -1) # Top bevel
        cv2.rectangle(frame, (18, beam_y1 + 14), (622, beam_y1 + 18), (10, 70, 160), -1) # Bottom shadow

        # Tier 2 Beam (Bottom)
        cv2.rectangle(frame, (18, beam_y2), (622, beam_y2 + 18), (15, 105, 220), -1)
        cv2.rectangle(frame, (18, beam_y2), (622, beam_y2 + 4), (40, 150, 255), -1)
        cv2.rectangle(frame, (18, beam_y2 + 14), (622, beam_y2 + 18), (10, 70, 160), -1)

        # Drop shadow beneath beams
        cv2.rectangle(frame, (18, beam_y1 + 18), (622, beam_y1 + 26), (15, 18, 22), -1)
        cv2.rectangle(frame, (18, beam_y2 + 18), (622, beam_y2 + 26), (15, 18, 22), -1)

        # 4. Realistic Shelf Barcode Label & AprilTag Plate on Left Column
        tag_plate_y = 65
        cv2.rectangle(frame, (12, tag_plate_y), (58, tag_plate_y + 55), (245, 245, 245), -1)
        cv2.rectangle(frame, (12, tag_plate_y), (58, tag_plate_y + 55), (20, 20, 20), 2)
        # Mini AprilTag Pattern
        cv2.rectangle(frame, (18, tag_plate_y + 6), (52, tag_plate_y + 40), (0, 0, 0), -1)
        cv2.rectangle(frame, (24, tag_plate_y + 12), (46, tag_plate_y + 34), (255, 255, 255), -1)
        cv2.rectangle(frame, (28, tag_plate_y + 16), (42, tag_plate_y + 30), (0, 0, 0), -1)
        cv2.putText(frame, shelf_name[-2:], (23, tag_plate_y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (10, 10, 10), 1)

        # 5. Smooth Drone Laser Scan Progression (Sinusoidal Ease-in-out)
        sweep_phase = (math.sin(elapsed_sec * 1.1) + 1.0) / 2.0
        laser_x = int(70 + sweep_phase * 480)

        detections = []


        # 6. Render Realistic Kraft Cardboard Cartons on Shelves
        # Tier 1 Boxes (Row 1 on middle beam)
        box_configs_t1 = [
            {"sku": "SKU-A101", "w": 78, "h": 68},
            {"sku": "SKU-A102", "w": 82, "h": 72},
            {"sku": "SKU-A103", "w": 76, "h": 65},
            {"sku": "SKU-A104", "w": 84, "h": 70},
            {"sku": "SKU-A105", "w": 80, "h": 68, "defect": is_defect},
            {"sku": "SKU-A106", "w": 78, "h": 66},
        ]

        curr_x = 62
        for idx, cfg in enumerate(box_configs_t1):
            bw, bh = cfg["w"], cfg["h"]
            bx = curr_x
            by = beam_y1 - bh
            has_defect = cfg.get("defect", False)

            # Check scanning state
            is_scanned = (laser_x >= (bx + bw // 2))
            is_active = (bx <= laser_x <= bx + bw)

            # Draw box body with Kraft texture
            base_col = (45, 60, 175) if has_defect else (68, 128, 188)
            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), base_col, -1)
            # Top bevel & shading
            cv2.line(frame, (bx, by), (bx + bw, by), (base_col[0] + 30, base_col[1] + 30, base_col[2] + 30), 2)
            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (30, 45, 60), 1)

            # Sealing Tape
            cv2.rectangle(frame, (bx, by + bh // 2 - 4), (bx + bw, by + bh // 2 + 4), (45, 95, 145), -1)

            # White Shipping Label with Real Barcode
            lbl_w = min(bw - 16, 52)
            lbl_h = min(bh // 2 - 2, 22)
            cv2.rectangle(frame, (bx + 8, by + 8), (bx + 8 + lbl_w, by + 8 + lbl_h), (248, 248, 248), -1)
            
            # Realistic barcode stripes
            for lx in range(bx + 12, bx + 8 + lbl_w - 6, 3):
                cv2.line(frame, (lx, by + 11), (lx, by + 8 + lbl_h - 4), (15, 15, 15), 1)

            # SKU Label Text
            cv2.putText(frame, cfg["sku"], (bx + 8, by + bh - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (240, 245, 255), 1, cv2.LINE_AA)

            # Defect Crush Markings (if damaged)
            if has_defect:
                # Jagged crush impact polygon
                crush_pts = np.array([[bx + bw - 26, by + 6], [bx + bw - 38, by + 28], [bx + bw - 18, by + 45], [bx + bw - 28, by + bh - 6]], np.int32)
                cv2.polylines(frame, [crush_pts], False, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.circle(frame, (bx + bw - 12, by + 14), 9, (0, 0, 230), -1)
                cv2.putText(frame, "!", (bx + bw - 16, by + 18), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 2, cv2.LINE_AA)

            # Record Detection
            if is_scanned or is_active:
                detections.append({
                    "class": "damaged box" if has_defect else "box",
                    "confidence": 0.98 if is_active else 0.95,
                    "bbox": [bx, by, bx + bw, by + bh],
                    "is_damaged": has_defect
                })

            curr_x += bw + 6

        # Tier 2 Boxes (Row 2 on bottom beam)
        box_configs_t2 = [
            {"sku": "SKU-B201", "w": 86, "h": 72},
            {"sku": "SKU-B202", "w": 84, "h": 70},
            {"sku": "SKU-B203", "w": 88, "h": 74},
            {"sku": "SKU-B204", "w": 82, "h": 68},
        ]

        curr_x = 75
        for idx, cfg in enumerate(box_configs_t2):
            bw, bh = cfg["w"], cfg["h"]
            bx = curr_x
            by = beam_y2 - bh

            is_scanned = (laser_x >= (bx + bw // 2))
            is_active = (bx <= laser_x <= bx + bw)

            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (68, 128, 188), -1)
            cv2.line(frame, (bx, by), (bx + bw, by), (98, 158, 218), 2)
            cv2.rectangle(frame, (bx, by), (bx + bw, by + bh), (30, 45, 60), 1)
            cv2.rectangle(frame, (bx, by + bh // 2 - 4), (bx + bw, by + bh // 2 + 4), (45, 95, 145), -1)

            # Label
            cv2.rectangle(frame, (bx + 8, by + 8), (bx + 54, by + 28), (248, 248, 248), -1)
            for lx in range(bx + 12, bx + 50, 3):
                cv2.line(frame, (lx, by + 11), (lx, by + 25), (15, 15, 15), 1)
            cv2.putText(frame, cfg["sku"], (bx + 8, by + bh - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (240, 245, 255), 1, cv2.LINE_AA)

            if is_scanned or is_active:
                detections.append({
                    "class": "box",
                    "confidence": 0.98 if is_active else 0.95,
                    "bbox": [bx, by, bx + bw, by + bh],
                    "is_damaged": False
                })

            curr_x += bw + 14

        # 7. Sleek LiDAR Laser Scan Beam
        is_in_defect_zone = (is_defect and 380 <= laser_x <= 480)
        laser_color = (0, 0, 255) if is_in_defect_zone else (0, 240, 255)

        # Laser vertical beam with soft glowing aura
        cv2.line(frame, (laser_x, 90), (laser_x, 410), laser_color, 2, cv2.LINE_AA)
        cv2.circle(frame, (laser_x, beam_y1 - 35), 4, laser_color, -1)
        cv2.circle(frame, (laser_x, beam_y2 - 35), 4, laser_color, -1)

        # Elegant Laser Status Pill
        scan_text = "DAMAGED BOX FOUND" if is_in_defect_zone else f"Counting: {len(detections)}/10"
        cv2.rectangle(frame, (laser_x - 42, 95), (laser_x + 58, 114), (15, 20, 30), -1)
        cv2.rectangle(frame, (laser_x - 42, 95), (laser_x + 58, 114), laser_color, 1)
        cv2.putText(frame, scan_text, (laser_x - 38, 108), cv2.FONT_HERSHEY_SIMPLEX, 0.30, laser_color, 1, cv2.LINE_AA)

        return frame, detections

    def render_safety_station(self, elapsed_sec):
        """Renders authentic 3D safety compliance station with real fire extinguisher & emergency exit."""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Ambient warehouse back wall
        for y in range(self.height):
            v = int(32 + 16 * (y / self.height))
            frame[y, :] = (v, v + 2, v + 5)

        # Safety Equipment Mounting Backboard
        cv2.rectangle(frame, (140, 60), (610, 420), (22, 28, 38), -1)
        cv2.rectangle(frame, (140, 60), (610, 420), (55, 70, 90), 2)
        cv2.rectangle(frame, (145, 65), (605, 415), (15, 18, 24), 1)

        # Red Fire Extinguisher Sign
        cv2.rectangle(frame, (170, 80), (350, 130), (15, 20, 200), -1)
        cv2.rectangle(frame, (170, 80), (350, 130), (255, 255, 255), 2)
        cv2.putText(frame, "FIRE EXTINGUISHER", (182, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 2, cv2.LINE_AA)

        # 3D Cylinder with Metallic Shading
        cx1, cx2 = 230, 290
        cy1, cy2 = 175, 360
        for x in range(cx1, cx2):
            ratio = (x - cx1) / (cx2 - cx1)
            r = int(180 + 75 * math.sin(ratio * math.pi))
            frame[cy1:cy2, x] = (15, 20, r)

        cv2.circle(frame, ((cx1 + cx2) // 2, cy1), (cx2 - cx1) // 2, (15, 20, 220), -1)
        # Pressure Gauge
        cv2.circle(frame, ((cx1 + cx2) // 2, cy1 - 20), 12, (190, 200, 210), -1)
        cv2.circle(frame, ((cx1 + cx2) // 2, cy1 - 20), 8, (255, 255, 255), -1)
        cv2.line(frame, ((cx1 + cx2) // 2, cy1 - 20), ((cx1 + cx2) // 2 + 5, cy1 - 24), (0, 180, 0), 2) # Green needle
        # Nozzle & Hose
        cv2.line(frame, ((cx1 + cx2) // 2, cy1 - 20), (cx2 + 15, cy1 + 30), (30, 30, 30), 4)

        # Emergency Exit Sign (Glowing Green)
        cv2.rectangle(frame, (390, 80), (575, 130), (20, 160, 45), -1)
        cv2.rectangle(frame, (390, 80), (575, 130), (255, 255, 255), 2)
        cv2.putText(frame, "EMERGENCY EXIT", (404, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 2, cv2.LINE_AA)

        # Verified Banner
        cv2.rectangle(frame, (220, 385), (530, 415), (15, 35, 20), -1)
        cv2.rectangle(frame, (220, 385), (530, 415), (0, 255, 136), 1)
        cv2.putText(frame, "SAFETY CHECK: 100% OK", (255, 405), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 136), 1, cv2.LINE_AA)

        detections = [
            {"class": "fire extinguisher", "confidence": 0.99, "bbox": [215, 140, 315, 370]},
            {"class": "emergency exit", "confidence": 0.99, "bbox": [390, 80, 575, 130]}
        ]
        return frame, detections

    def render_launchpad_standby(self):
        """Renders stationary launchpad base in hangar with drone resting at docking station."""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Polished Hangar Epoxy Floor
        for y in range(self.height):
            v = int(38 + 18 * (y / self.height))
            frame[y, :] = (v, v + 2, v + 4)

        # Launchpad Outer Safety Ring
        center = (320, 220)
        cv2.circle(frame, center, 140, (30, 35, 45), -1)
        cv2.circle(frame, center, 140, (0, 240, 255), 3)
        cv2.circle(frame, center, 120, (20, 25, 35), -1)
        cv2.circle(frame, center, 120, (255, 255, 255), 1)

        # Yellow Hazard Chevrons on ring
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = int(center[0] + 122 * math.cos(rad))
            y1 = int(center[1] + 122 * math.sin(rad))
            x2 = int(center[0] + 138 * math.cos(rad))
            y2 = int(center[1] + 138 * math.sin(rad))
            cv2.line(frame, (x1, y1), (x2, y2), (0, 240, 255), 3)

        # Center [ H ] Helipad Landing Decal
        cv2.putText(frame, "H", (center[0] - 25, center[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 2.8, (255, 255, 255), 6, cv2.LINE_AA)

        # Drone Docking Alignment Crosshairs
        cv2.line(frame, (center[0] - 160, center[1]), (center[0] + 160, center[1]), (0, 240, 255), 1)
        cv2.line(frame, (center[0], center[1] - 160), (center[0], center[1] + 160), (0, 240, 255), 1)

        # Ready Status Beacon Box
        cv2.rectangle(frame, (120, 410), (520, 455), (15, 20, 30), -1)
        cv2.rectangle(frame, (120, 410), (520, 455), (0, 255, 136), 1)
        cv2.circle(frame, (145, 432), 6, (0, 255, 136), -1)
        cv2.putText(frame, "DRONE READY - CLICK 'START MISSION'", (170, 437), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 1, cv2.LINE_AA)

        return frame, []

    def render_camera_offline(self, source_name="webcam"):
        """Renders clear status screen when physical camera device is connecting or offline."""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for y in range(self.height):
            v = int(20 + 15 * (y / self.height))
            frame[y, :] = (v, v + 2, v + 5)

        # Center Card
        cv2.rectangle(frame, (100, 140), (540, 340), (22, 28, 38), -1)
        cv2.rectangle(frame, (100, 140), (540, 340), (0, 240, 255), 1)

        if source_name == "webcam":
            title = "WEBCAM CONNECTING / ACTIVE"
            sub1 = "Reading laptop camera (Device Index 0)..."
            sub2 = "Point camera at shelf AprilTags (0, 1, 2, 3) or boxes"
        else:
            title = "DRONE CAMERA (PI STREAM)"
            sub1 = "Searching for WiFi stream at 192.168.1.100:8080..."
            sub2 = "Connect Raspberry Pi / ESP32-CAM to warehouse network"

        cv2.putText(frame, title, (130, 195), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (0, 240, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, sub1, (130, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, sub2, (130, 275), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (180, 200, 220), 1, cv2.LINE_AA)

        return frame, []


