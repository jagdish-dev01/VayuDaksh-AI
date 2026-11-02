"""
Master Vision Pipeline Coordinator
Synchronizes YOLO, AprilTag localization, Inventory counting, Damage, and Safety engines.
"""
import time
import cv2
from vision.yolo_engine import YOLOEngine
from vision.marker_engine import MarkerEngine
from vision.inventory_engine import InventoryEngine
from vision.damage_engine import DamageEngine
from vision.safety_engine import SafetyEngine
from vision.synthetic_feed import SyntheticDroneFeed
from utils.draw_hud import draw_hud_annotations

class VisionDetector:
    def __init__(self):
        self.yolo = YOLOEngine()
        self.marker = MarkerEngine()
        self.inventory = InventoryEngine()
        self.damage = DamageEngine()
        self.safety = SafetyEngine()
        self.sim_feed = SyntheticDroneFeed()
        self.last_alerts = []

    def sync_stage(self, stage_num):
        """Immediately synchronizes all sub-engines with the chosen stage."""
        self.inventory.sync_stage(stage_num)

    def process_frame(self, frame=None, source_type="simulated", elapsed_sec=0, tracking_mode="ai"):
        custom_boxes = None
        current_wp = None

        # 1. Acquire frame based on source
        if source_type == "simulated":
            frame, custom_boxes, current_wp = self.sim_feed.generate_frame(elapsed_sec, tracking_mode)
        elif frame is None:
            frame, _ = self.sim_feed.renderer.render_camera_offline(source_type)
            custom_boxes = []
            current_wp = None

        # 2. Marker Detection (AprilTag 36h11 & ArUco)
        markers = self.marker.detect_markers(frame)
        
        if source_type == "simulated" and tracking_mode == "tags" and custom_boxes:
            base_id = 100
            for b in custom_boxes:
                if b.get("class") in ["box", "damaged box", "package"]:
                    base_id += 1
                    x1, y1, x2, y2 = b["bbox"]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    tag_w = min(40, (x2 - x1) // 2)
                    tx1, ty1 = cx - tag_w//2, cy - tag_w//2
                    tx2, ty2 = cx + tag_w//2, cy + tag_w//2
                    
                    # Draw a high-contrast QR code placeholder on the frame
                    cv2.rectangle(frame, (tx1, ty1), (tx2, ty2), (255, 255, 255), -1)
                    cv2.rectangle(frame, (tx1+4, ty1+4), (tx2-4, ty2-4), (0, 0, 0), -1)
                    cv2.rectangle(frame, (tx1+8, ty1+8), (tx2-8, ty2-8), (255, 255, 255), -1)
                    
                    markers.append({
                        "id": str(base_id),
                        "shelf": f"Box: {base_id}",
                        "corners": [[tx1, ty1], [tx2, ty1], [tx2, ty2], [tx1, ty2]],
                        "center": [cx, cy],
                        "estimated_dist_m": 1.2,
                        "type": "QRCode"
                    })

        active_shelf = self.marker.get_active_shelf()
        if not active_shelf and current_wp:
            active_shelf = current_wp.get("shelf")

        # 3. YOLO Object Detection
        detections = self.yolo.detect(frame, custom_boxes=custom_boxes)

        # 4. Damaged Package Inspection
        damaged_boxes, damage_alert = self.damage.inspect_frame(frame, detections, active_shelf)
        if damaged_boxes:
            detections = [d for d in detections if d.get("class") not in ["box", "package"] or not d.get("is_damaged")]
            detections.extend(damaged_boxes)

        # Apply Tracking Mode Logic
        if tracking_mode == "tags":
            for m in markers:
                self.inventory.register_tag(m["id"])
            
            # The currently visible count in the camera frame
            visible_count = len(markers)
            
            # Create synthetic detections for the tags so they draw on HUD
            tag_detections = []
            for m in markers:
                import numpy as np
                pts = np.array(m["corners"])
                x_min, y_min = np.min(pts, axis=0)
                x_max, y_max = np.max(pts, axis=0)
                tag_detections.append({
                    "class": f"Tag {m['id']}",
                    "confidence": 0.99,
                    "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)],
                    "color": (255, 255, 0) # Cyan/Yellowish
                })
            detections = tag_detections
            active_shelf = "Global Scan" # Override shelf context
            shelf_update = self.inventory.update_shelf_count("Global Scan", visible_count, 0)
            box_count = len(self.inventory.get_registered_tags()) # keep result payload tracking total registered
        else:
            # 5. Box Inventory Counting (AI Mode)
            box_count = sum(1 for d in detections if d.get("class") in ["box", "package", "damaged box"])
            shelf_update = None
            if active_shelf and "Shelf" in active_shelf:
                shelf_update = self.inventory.update_shelf_count(active_shelf, box_count, len(damaged_boxes))

        # 6. Safety Compliance Audit
        safety_status, safety_alerts = self.safety.audit_frame(detections, active_shelf)

        # 7. Collect Alerts
        alerts = []
        if damage_alert:
            alerts.append(damage_alert)
        if shelf_update and shelf_update.get("alert"):
            alerts.append(shelf_update["alert"])
        alerts.extend(safety_alerts)
        self.last_alerts = alerts

        # 8. Render Augmented Reality Annotations
        annotated_frame = draw_hud_annotations(frame, detections, active_shelf)

        # Compile Result Contract
        result = {
            "timestamp": time.time(),
            "active_shelf": active_shelf,
            "markers": markers,
            "registered_tags": self.inventory.get_registered_tags(),
            "detections": detections,
            "box_count": box_count,
            "damaged_count": len(damaged_boxes),
            "inventory_summary": self.inventory.get_summary(),
            "shelf_records": self.inventory.get_all_records(),
            "safety_status": safety_status,
            "alerts": alerts,
            "waypoint": current_wp
        }

        return annotated_frame, result
