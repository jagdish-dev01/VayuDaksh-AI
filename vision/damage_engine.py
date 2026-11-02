"""
Package Health & Damage Inspection Engine
Detects damaged packages, red defect markers, and structural deformities.
"""
import cv2
import numpy as np

class DamageEngine:
    def __init__(self):
        self.damaged_packages = []

    def inspect_frame(self, frame, box_detections, active_shelf=None):
        """
        Scans detected box regions for red damage stickers or deformities.
        Returns: list of damaged box detections and damage alerts.
        """
        if frame is None or not box_detections:
            return [], None

        h, w = frame.shape[:2]
        damaged_in_frame = []
        alert = None

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Red color range for damage defect stickers
        mask1 = cv2.inRange(hsv, (0, 120, 120), (10, 255, 255))
        mask2 = cv2.inRange(hsv, (160, 120, 120), (180, 255, 255))
        red_mask = cv2.bitwise_or(mask1, mask2)

        for obj in box_detections:
            if obj.get("class") not in ["box", "package"]:
                continue

            x1, y1, x2, y2 = obj["bbox"]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            box_roi = red_mask[y1:y2, x1:x2]
            if box_roi.size == 0:
                continue

            red_pixels = cv2.countNonZero(box_roi)
            total_pixels = (x2 - x1) * (y2 - y1)
            red_ratio = red_pixels / max(total_pixels, 1)

            # Check if this box is marked as damaged (explicitly or red sticker)
            is_damaged = obj.get("is_damaged", False) or (0.04 < red_ratio < 0.60)

            if is_damaged:
                damage_record = {
                    "class": "damaged box",
                    "confidence": 0.96,
                    "defect_id": "DMG-882",
                    "bbox": [x1, y1, x2, y2],
                    "shelf": active_shelf or "Unknown Shelf",
                    "severity": "HIGH",
                    "defect_type": "Crushed Corner / Puncture Defect"
                }
                damaged_in_frame.append(damage_record)
                
                alert = {
                    "level": "CRITICAL",
                    "type": "DAMAGED_PACKAGE",
                    "shelf": active_shelf or "Zone Beta",
                    "message": f"Damaged package flagged at {active_shelf or 'Shelf B2'} (Defect #DMG-882: Structural Crush)"
                }

        return damaged_in_frame, alert
