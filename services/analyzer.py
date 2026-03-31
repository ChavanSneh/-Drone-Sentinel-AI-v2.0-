import re

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
        """Determines event type and severity based on AI-extracted entities."""
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
            # Speeding detection
            if "speeding" in event_list:
                return {"event_type": "speeding_vehicle_detected", "severity": "medium"}

            # Unauthorized parking detection
            if "parked" in event_list and location_list:
                return {"event_type": f"vehicle_parked_at_{location_list[0]}", "severity": "medium"}

            # History-based repeat sighting detection
            if location_list:
                repeat_count = sum(
                    1 for h in history
                    if any(v in h.get("object", []) for v in vehicle_keywords)
                    and any(l in h.get("location", []) for l in location_list)
                )
                if repeat_count >= 1:
                    loc_name = location_list[0]
                    return {"event_type": f"repeated_vehicle_at_{loc_name}", "severity": "medium"}

            # Proximity to secure perimeter locations is higher-risk
            if any(loc in ["fence", "gate", "garage"] for loc in location_list):
                return {"event_type": "vehicle_near_secure_perimeter", "severity": "medium"}

        # --- PRIORITY 3: LOW SEVERITY (INFO) ---
        if obj_list:
            primary_obj = obj_list[0]
            loc_suffix = f"_at_{location_list[0]}" if location_list else ""
            return {"event_type": f"observing_{primary_obj}{loc_suffix}", "severity": "low"}

        if location_list:
            return {"event_type": f"monitoring_{location_list[0]}", "severity": "low"}

        # Final fallback
        return {"event_type": "no_activity_detected", "severity": "none"}

    def analyze_frame(self, description: str, telemetry: dict, history: list) -> dict:
        """Main entry point for frame analysis."""
        entities = self.extract_entities(description)
        event_info = self.detect_event(entities, history)

        severity_to_alert = {
            "none": "none",
            "low": "info",
            "medium": "warning",
            "high": "alert"
        }

        # AI Vision is prioritized over static Telemetry for the 'location' field
        return {
            "time": telemetry.get("time"),
            "location": entities.get("location")[0] if entities.get("location") else telemetry.get("location"),
            "object": entities.get("object"),
            "color": entities.get("color"),
            "event": entities.get("event"),
            "alert": severity_to_alert[event_info["severity"]],
            "event_type": event_info["event_type"],
            "severity": event_info["severity"]
        }