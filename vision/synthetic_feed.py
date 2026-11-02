"""
Autonomous Drone Flight & Photorealistic Vision Simulator
Integrates PhotorealisticWarehouseRenderer for authentic 3D warehouse inspection footage.
"""
import time
import math
import cv2
import numpy as np
from vision.photorealistic_renderer import PhotorealisticWarehouseRenderer

class SyntheticDroneFeed:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.start_time = time.time()
        self.renderer = PhotorealisticWarehouseRenderer(width, height)
        
        self.flight_waypoints = [
            {"time": 0, "stage": 1, "shelf": None, "desc": "Takeoff & Pre-Flight Hangar Calibration", "pos": (10, 82)},
            {"time": 10, "stage": 2, "shelf": "Aisle Alpha", "desc": "Aisle Alpha Optical Navigation", "pos": (20, 55)},
            {"time": 22, "stage": 3, "shelf": "Aisle Alpha (AI)", "desc": "YOLO Multi-Class Object Detection", "pos": (25, 45)},
            {"time": 36, "stage": 4, "shelf": "Shelf A1", "boxes": 10, "damaged": 0, "desc": "Shelf A1 Autonomous Count", "pos": (22, 35)},
            {"time": 60, "stage": 5, "shelf": "Shelf A2", "boxes": 8, "damaged": 0, "desc": "Shelf A2 Autonomous Count", "pos": (44, 35)},
            {"time": 88, "stage": 6, "shelf": "Shelf B2", "boxes": 9, "damaged": 1, "desc": "Shelf B2 Defect Flagging", "pos": (84, 65)},
            {"time": 122, "stage": 7, "shelf": "Safety Station Alpha", "safety": True, "desc": "Safety Compliance Audit", "pos": (90, 45)},
            {"time": 150, "stage": 8, "shelf": None, "desc": "Mission Complete - Return to Base", "pos": (10, 82)},
        ]
        
        self.tag_waypoints = [
            {"time": 0, "stage": 1, "shelf": None, "desc": "Takeoff & Hover", "pos": (10, 82)},
            {"time": 8, "stage": 2, "shelf": "Global Scan", "boxes": 15, "damaged": 0, "desc": "Global Tag Scan", "pos": (25, 45)},
            {"time": 30, "stage": 3, "shelf": None, "desc": "Mission Complete", "pos": (10, 82)}
        ]

    def get_current_waypoint(self, elapsed, tracking_mode="ai"):
        waypoints = self.tag_waypoints if tracking_mode == "tags" else self.flight_waypoints
        current = waypoints[0]
        for wp in waypoints:
            if elapsed >= wp["time"]:
                current = wp
            else:
                break
        return current

    def generate_frame(self, elapsed_sec=None, tracking_mode="ai"):
        if elapsed_sec is None:
            elapsed_sec = time.time() - self.start_time

        # In STANDBY mode (before user clicks Start Mission), remain stationary on launchpad
        if elapsed_sec <= 0.0:
            frame, detections = self.renderer.render_launchpad_standby()
            return frame, detections, self.get_current_waypoint(0, tracking_mode)

        wp = self.get_current_waypoint(elapsed_sec, tracking_mode)
        active_shelf = wp.get("shelf")
        stage = wp.get("stage", 1)


        # 1. Dispatch to photorealistic scene renderer
        if active_shelf and ("Shelf" in active_shelf or active_shelf == "Global Scan"):
            is_defect = (active_shelf == "Shelf B2" or wp.get("damaged", 0) > 0)
            frame, detections = self.renderer.render_shelf_inspection(active_shelf, elapsed_sec, is_defect=is_defect)
        elif stage == 3:
            frame, detections = self.renderer.render_warehouse_aisle(elapsed_sec, show_worker=True)
        elif active_shelf == "Safety Station Alpha" or stage == 7:
            frame, detections = self.renderer.render_safety_station(elapsed_sec)
        else:
            # Stages 1, 2, 8: Aisle flight & takeoff
            frame, detections = self.renderer.render_warehouse_aisle(elapsed_sec, show_worker=False)

        # 2. Add realistic subtle drone optical stabilization micro-motion
        dx = int(math.sin(elapsed_sec * 2.0) * 1.0)
        dy = int(math.cos(elapsed_sec * 1.5) * 0.8)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        frame = cv2.warpAffine(frame, M, (self.width, self.height))

        return frame, detections, wp
