import re
from datetime import datetime

# -------------------------------
# Keywords (Expanded for better AI matching)
# -------------------------------
OBJECT_KEYWORDS = {
    "person": ["person", "man", "woman", "individual", "pedestrian", "group", "people"],
    "people": ["person", "man", "woman", "individual", "pedestrian", "group", "people"],
    "cars": ["car", "cars", "vehicle", "vehicles", "suv", "sedan", "auto"],
    "trucks": ["truck", "trucks", "f150", "pickup", "lorry", "lorries", "semi"]
}

COLOR_KEYWORDS = ["red", "blue", "white", "black", "silver", "grey", "yellow", "green", "unknown"]

LOCATION_KEYWORDS = {
    "gate": ["gate", "entrance", "entry", "exit"],
    "fence": ["fence", "perimeter", "boundary", "wall"],
    "road": ["road", "highway", "street", "driveway", "lane", "alley", "parking lot"],
    "garage": ["garage", "parking", "carport", "shed"]
}

EVENT_KEYWORDS = {
    "parked": ["parked", "stationary", "stopped", "idle"],
    "loitering": ["loitering", "standing", "waiting", "leaning", "idling", "hanging around"],
    "speeding": ["speeding", "fast", "driving quickly", "racing", "moving fast"],
    "stuck": ["stuck", "trapped", "immobile", "blocked", "jammed", "stalled"] 
}

class Analyzer:
    def __init__(self, start_battery=100.0, depletion_rate_per_min=2.5):
        """Initializes the engine with tracking states."""
        self.current_battery = start_battery
        self.rate = depletion_rate_per_min
        self.last_timestamp = None

    def track_hardware_state(self, current_time_str: str) -> float:
        """Calculates battery depletion based on the time difference between frames."""
        try:
            # Clean ISO string formatting for Python's datetime parser
            clean_time_str = current_time_str.replace("Z", "+00:00")
            current_time = datetime.fromisoformat(clean_time_str)
        except ValueError:
            # Fallback if timestamp string format is unexpected
            return self.current_battery

        # If it's the very first frame tracked, initialize the baseline timestamp
        if self.last_timestamp is None:
            self.last_timestamp = current_time
            return self.current_battery

        # Compute elapsed time delta
        elapsed_seconds = (current_time - self.last_timestamp).total_seconds()
        elapsed_minutes = elapsed_seconds / 60.0

        if elapsed_minutes > 0:
            battery_used = elapsed_minutes * self.rate
            self.current_battery = max(0.0, self.current_battery - battery_used)
            self.last_timestamp = current_time

        return round(self.current_battery, 2)

    def extract_matches(self, text: str, keyword_dict: dict) -> list:
        """Helper to find all matching category labels in the text."""
        text = text.lower()
        return [
            label
            for label, words in keyword_dict.items()
            if any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in words)
        ]

    def extract_entities(self, description: str) -> dict:
        """Parses the VLM description into structured lists."""
        text = description.lower()
        return {
            "object": self.extract_matches(text, OBJECT_KEYWORDS),
            "color": self.extract_matches(text, {c: [c] for c in COLOR_KEYWORDS}),
            "location": self.extract_matches(text, LOCATION_KEYWORDS),
            "event": self.extract_matches(text, EVENT_KEYWORDS),
        }

    def detect_event(self, entities: dict, history: list) -> dict:
        """Determines event type and severity based on AI-extracted entities and hardware states."""
        
        # --- PRIORITY 0: CRITICAL HARDWARE FAIL-SAFES ---
        if self.current_battery <= 20.0:
            return {
                "event_type": "critical_battery_emergency_landing", 
                "severity": "high"
            }

        obj_list = entities.get("object") or []
        event_list = entities.get("event") or []
        location_list = entities.get("location") or []

        # --- PRIORITY 1: HIGH SEVERITY (ALERTS) ---
        
        # Priority Check: AI detected something is STUCK
        if "stuck" in event_list:
            loc_name = location_list[0] if location_list else "unknown_location"
            return {"event_type": f"object_stuck_at_{loc_name}", "severity": "high"}

        # Security Check: Unauthorized person activity
        if any(person_label in obj_list for person_label in ("person", "people", "individual")):
            if any(loc in ["fence", "gate", "garage"] for loc in location_list):
                return {"event_type": f"unauthorized_{location_list[0]}_access", "severity": "high"}
            if "loitering" in event_list:
                return {"event_type": "suspicious_loitering", "severity": "high"}

        # --- PRIORITY 2: MEDIUM SEVERITY (WARNINGS) ---
        vehicle_keywords = {"car", "cars", "truck", "trucks"}
        if any(vehicle in obj_list for vehicle in vehicle_keywords):
            if "speeding" in event_list:
                return {"event_type": "speeding_vehicle_detected", "severity": "medium"}

            if "parked" in event_list and location_list:
                return {"event_type": f"vehicle_parked_at_{location_list[0]}", "severity": "medium"}

            if location_list:
                repeat_count = sum(
                    1 for h in history
                    if any(v in h.get("object", []) for v in vehicle_keywords)
                    and any(l in h.get("location", []) for l in location_list)
                )
                if repeat_count >= 1:
                    loc_name = location_list[0]
                    return {"event_type": f"repeated_vehicle_at_{loc_name}", "severity": "medium"}

            if any(loc in ["fence", "gate", "garage"] for loc in location_list):
                return {"event_type": "vehicle_near_secure_perimeter", "severity": "medium"}

        # --- PRIORITY 3: LOW SEVERITY (INFO) ---
        if obj_list:
            primary_obj = obj_list[0]
            loc_suffix = f"_at_{location_list[0]}" if location_list else ""
            return {"event_type": f"observing_{primary_obj}{loc_suffix}", "severity": "low"}

        if location_list:
            return {"event_type": f"monitoring_{location_list[0]}", "severity": "low"}

        return {"event_type": "no_activity_detected", "severity": "none"}

    def analyze_frame(self, description: str, telemetry: dict, history: list) -> dict:
        """Main entry point for frame analysis."""
        
        # 1. Update internal battery state using the frame's time before processing rules
        frame_time = telemetry.get("time")
        if frame_time:
            self.track_hardware_state(frame_time)
            
        # 2. Extract entities and run event checking
        entities = self.extract_entities(description)
        event_info = self.detect_event(entities, history)

        severity_to_alert = {
            "none": "none",
            "low": "info",
            "medium": "warning",
            "high": "alert"
        }

        return {
            "time": frame_time,
            "location": entities.get("location")[0] if entities.get("location") else telemetry.get("location"),
            "object": entities.get("object"),
            "color": entities.get("color"),
            "event": entities.get("event"),
            "battery_level": self.current_battery,  # Returns the updated calculated battery
            "alert": severity_to_alert[event_info["severity"]],
            "event_type": event_info["event_type"],
            "severity": event_info["severity"]
        }