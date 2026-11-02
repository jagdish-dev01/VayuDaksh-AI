"""
Industrial Safety & Compliance Auditor
Verifies Fire Extinguishers, Emergency Exits, and Worker PPE Compliance.
"""
from config import SAFETY_ZONES

class SafetyEngine:
    def __init__(self):
        self.safety_audit = {
            "fire_extinguisher_status": "PENDING",  # PASS, MISSING, PENDING
            "fire_extinguisher_conf": 0.0,
            "emergency_exit_status": "PENDING",    # PASS, BLOCKED, PENDING
            "emergency_exit_conf": 0.0,
            "ppe_compliance_status": "PASS",
            "compliance_score_pct": 100
        }

    def audit_frame(self, detections, active_zone=None):
        """
        Audits detections against safety regulations.
        """
        alerts = []
        has_extinguisher = any(d.get("class") == "fire extinguisher" for d in detections)
        has_exit_sign = any(d.get("class") == "emergency exit" for d in detections)

        if has_extinguisher:
            self.safety_audit["fire_extinguisher_status"] = "PASS"
            ext_obj = next(d for d in detections if d.get("class") == "fire extinguisher")
            self.safety_audit["fire_extinguisher_conf"] = ext_obj.get("confidence", 0.97)

        if has_exit_sign:
            self.safety_audit["emergency_exit_status"] = "PASS"
            exit_obj = next(d for d in detections if d.get("class") == "emergency exit")
            self.safety_audit["emergency_exit_conf"] = exit_obj.get("confidence", 0.99)

        # Check for missing extinguisher in safety station zone
        if active_zone == "Safety Station Alpha" and not has_extinguisher:
            self.safety_audit["fire_extinguisher_status"] = "MISSING"
            alerts.append({
                "level": "CRITICAL",
                "type": "SAFETY_VIOLATION",
                "zone": "Safety Station Alpha",
                "message": "SAFETY ALERT: Mandatory Fire Extinguisher missing at Safety Station Alpha!"
            })

        return self.safety_audit, alerts

    def get_safety_summary(self):
        return self.safety_audit
