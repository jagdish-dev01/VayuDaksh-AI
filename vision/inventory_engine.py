"""
Dynamic Shelf Inventory Counter & Discrepancy Engine
Counts packages per shelf and detects discrepancies against warehouse manifest.
"""
from collections import deque
from config import WAREHOUSE_MANIFEST

class InventoryEngine:
    def __init__(self):
        self.shelf_records = {}
        self.count_history = {shelf: deque(maxlen=8) for shelf in WAREHOUSE_MANIFEST}
        self.global_tags = {}
        self.init_manifest()

    def init_manifest(self):
        """Initializes records with default manifest."""
        self.global_tags = {}
        for shelf, data in WAREHOUSE_MANIFEST.items():
            self.shelf_records[shelf] = {
                "shelf_id": shelf,
                "zone": data["zone"],
                "category": data["category"],
                "expected_count": data["expected_boxes"],
                "detected_count": 0,
                "status": "PENDING",  # PENDING, VERIFIED, MISMATCH
                "discrepancy": 0,
                "damaged_count": 0,
                "last_inspected": None
            }

    def sync_stage(self, stage_num):
        """Pre-populates inventory records based on completed stage progress."""
        self.init_manifest()
        if stage_num >= 4:
            self.shelf_records["Shelf A1"]["detected_count"] = 10
            self.shelf_records["Shelf A1"]["status"] = "VERIFIED"
        if stage_num >= 5:
            self.shelf_records["Shelf A2"]["detected_count"] = 8
            self.shelf_records["Shelf A2"]["status"] = "VERIFIED"
        if stage_num >= 6:
            self.shelf_records["Shelf B1"]["detected_count"] = 12
            self.shelf_records["Shelf B1"]["status"] = "VERIFIED"
            self.shelf_records["Shelf B2"]["detected_count"] = 9
            self.shelf_records["Shelf B2"]["status"] = "MISMATCH"
            self.shelf_records["Shelf B2"]["discrepancy"] = -1
            self.shelf_records["Shelf B2"]["damaged_count"] = 1

    def update_shelf_count(self, shelf_id, raw_count, damaged_count=0):
        if not shelf_id:
            return None

        # Dynamically create shelf record for new IDs (e.g., Global Scan)
        if shelf_id not in self.shelf_records:
            self.shelf_records[shelf_id] = {
                "shelf_id": shelf_id,
                "zone": "Unknown",
                "category": "Scanned",
                "expected_count": 0,
                "detected_count": 0,
                "status": "PENDING",
                "discrepancy": 0,
                "damaged_count": 0,
                "last_inspected": None
            }
            from collections import deque
            if shelf_id not in self.count_history:
                self.count_history[shelf_id] = deque(maxlen=8)

        if shelf_id == "Global Scan":
            self.shelf_records[shelf_id]["expected_count"] = len(self.global_tags)

        self.count_history[shelf_id].append(raw_count)
        stable_count = int(sorted(self.count_history[shelf_id])[len(self.count_history[shelf_id]) // 2])
        
        expected = self.shelf_records[shelf_id]["expected_count"]
        discrepancy = stable_count - expected
        status = "VERIFIED" if (discrepancy == 0 and damaged_count == 0) else "MISMATCH"

        self.shelf_records[shelf_id]["detected_count"] = stable_count
        self.shelf_records[shelf_id]["discrepancy"] = discrepancy
        self.shelf_records[shelf_id]["status"] = status
        self.shelf_records[shelf_id]["damaged_count"] = damaged_count

        alert = None
        if status == "MISMATCH" and (stable_count > 0 or expected > 0):
            if discrepancy < 0:
                deficit = abs(discrepancy)
                alert = {
                    "level": "WARNING",
                    "type": "INVENTORY_MISMATCH",
                    "shelf": shelf_id,
                    "message": f"Missing Boxes! Expected {expected}, but only {stable_count} are visible in camera."
                }
            elif discrepancy > 0:
                surplus = discrepancy
                alert = {
                    "level": "WARNING",
                    "type": "INVENTORY_MISMATCH",
                    "shelf": shelf_id,
                    "message": f"Extra Boxes! Expected {expected}, Detected {stable_count} (Surplus: +{surplus})"
                }

        return {
            "shelf_record": self.shelf_records[shelf_id],
            "alert": alert
        }

    def get_all_records(self):
        return self.shelf_records

    def register_tag(self, tag_id):
        import time
        if tag_id not in self.global_tags:
            self.global_tags[tag_id] = {
                "id": tag_id,
                "first_seen": time.time()
            }
        return self.global_tags[tag_id]

    def get_registered_tags(self):
        return list(self.global_tags.values())

    def get_summary(self):
        total_expected = sum(r["expected_count"] for r in self.shelf_records.values())
        total_detected = sum(r["detected_count"] for r in self.shelf_records.values())
        total_damaged = sum(r["damaged_count"] for r in self.shelf_records.values())
        verified_shelves = sum(1 for r in self.shelf_records.values() if r["status"] == "VERIFIED")
        
        return {
            "total_shelves": len(self.shelf_records),
            "verified_shelves": verified_shelves,
            "total_expected_boxes": total_expected,
            "total_detected_boxes": total_detected,
            "total_damaged_boxes": total_damaged,
            "accuracy_pct": round((total_detected / max(total_expected, 1)) * 100, 1)
        }
