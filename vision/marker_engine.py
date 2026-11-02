"""
AprilTag 36h11 and ArUco Marker Localization Engine
Detects markers for Shelf A1, A2, B1, B2 and estimates spatial position.
"""
import cv2
import numpy as np
from config import TAG_SHELF_MAP

class MarkerEngine:
    def __init__(self):
        self.dict_apriltag = self._get_dictionary(cv2.aruco.DICT_APRILTAG_36h11 if hasattr(cv2.aruco, 'DICT_APRILTAG_36h11') else cv2.aruco.DICT_4X4_50)
        self.dict_aruco = self._get_dictionary(cv2.aruco.DICT_4X4_50)
        self.detector_params = self._get_detector_params()
        self.active_shelf = None
        self.shelf_confidence = 0.0
        self.last_detection_time = 0

    def _get_dictionary(self, dict_type):
        try:
            return cv2.aruco.getPredefinedDictionary(dict_type)
        except Exception:
            return cv2.aruco.Dictionary_get(dict_type) if hasattr(cv2.aruco, 'Dictionary_get') else None

    def _get_detector_params(self):
        try:
            return cv2.aruco.DetectorParameters()
        except Exception:
            return cv2.aruco.DetectorParameters_create() if hasattr(cv2.aruco, 'DetectorParameters_create') else None

    def detect_markers(self, frame):
        """
        Detects AprilTags / ArUco markers AND standard QR Codes in the frame.
        """
        if frame is None:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detected_markers = []

        # 1. Detect Standard QR Codes
        try:
            qr_detector = cv2.QRCodeDetector()
            retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(frame)
            if retval and points is not None:
                for i, text in enumerate(decoded_info):
                    pts = points[i].astype(int)
                    center_x = int(np.mean(pts[:, 0]))
                    center_y = int(np.mean(pts[:, 1]))
                    box_width = np.linalg.norm(pts[0] - pts[1])
                    dist_est = round(float(120.0 / max(box_width, 1.0)), 2)
                    
                    # If QR code has text, use it as ID, else use hash or index
                    tag_id = text if text else f"QR-{i}"
                    
                    # Check if it matches a shelf by some convention, else default
                    shelf_name = TAG_SHELF_MAP.get(tag_id, f"Shelf #{tag_id}") if text.isdigit() else f"Box: {tag_id}"
                    if text.isdigit() and int(text) in TAG_SHELF_MAP:
                         self.active_shelf = TAG_SHELF_MAP[int(text)]
                         
                    detected_markers.append({
                        "id": tag_id,
                        "shelf": shelf_name,
                        "corners": pts.tolist(),
                        "center": [center_x, center_y],
                        "estimated_dist_m": dist_est,
                        "type": "QRCode"
                    })
        except Exception as e:
            pass

        # 2. Detect AprilTags / ArUco
        for aruco_dict in [self.dict_apriltag, self.dict_aruco]:
            if aruco_dict is None:
                continue
            try:
                if hasattr(cv2.aruco, 'ArucoDetector'):
                    detector = cv2.aruco.ArucoDetector(aruco_dict, self.detector_params)
                    corners, ids, _ = detector.detectMarkers(gray)
                else:
                    corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=self.detector_params)

                if ids is not None and len(ids) > 0:
                    for i, tag_id in enumerate(ids.flatten()):
                        pts = corners[i][0].astype(int)
                        center_x = int(np.mean(pts[:, 0]))
                        center_y = int(np.mean(pts[:, 1]))
                        box_width = np.linalg.norm(pts[0] - pts[1])
                        dist_est = round(float(120.0 / max(box_width, 1.0)), 2)
                        
                        shelf_name = TAG_SHELF_MAP.get(int(tag_id), f"Shelf #{tag_id}")
                        self.active_shelf = shelf_name
                        self.shelf_confidence = 0.99
                        
                        detected_markers.append({
                            "id": int(tag_id),
                            "shelf": shelf_name,
                            "corners": pts.tolist(),
                            "center": [center_x, center_y],
                            "estimated_dist_m": dist_est,
                            "type": "AprilTag"
                        })
                    break
            except Exception as e:
                pass

        return detected_markers

    def get_active_shelf(self):
        return self.active_shelf
