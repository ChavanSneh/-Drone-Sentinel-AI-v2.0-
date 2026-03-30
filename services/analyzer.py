import re

# -------------------------------
# Keywords (Expanded for better AI matching)
# -------------------------------
OBJECT_KEYWORDS = {
    "person": ["person", "man", "woman", "individual", "pedestrian"],
    "car": ["car", "vehicle", "suv", "sedan", "auto"],
    "truck": ["truck", "f150", "pickup", "lorry", "semi"]
}

COLOR_KEYWORDS = ["red", "blue", "white", "black", "silver", "grey"]

LOCATION_KEYWORDS = {
    "gate": ["gate", "entrance", "entry"],
    "fence": ["fence", "perimeter", "boundary"],
    "road": ["road", "highway", "street", "driveway", "lane"],
    "garage": ["garage", "parking", "carport"]
}

EVENT_KEYWORDS = {
    "parked": ["parked", "stationary", "stopped"],
    "loitering": ["loitering", "standing", "waiting", "leaning", "idling"],
    "speeding": ["speeding", "fast", "driving quickly", "racing", "moving fast"]
}

class Analyzer:
    def extract_entities(self, description: str) -> dict:
        text = description.lower()

        def match(keywords_dict):
            for key, words in keywords_dict.items():
                for w in words:
                    if re.search(r"\b" + re.escape(w) + r"\b", text):
                        return key
            return None

        def match_color():
            for c in COLOR_KEYWORDS:
                if re.search(r"\b" + c + r"\b", text):
                    return c
            return None

        return {
            "object": match(OBJECT_KEYWORDS),
            "color": match_color(),
            "location": match(LOCATION_KEYWORDS),
            "event": match(EVENT_KEYWORDS),
        }

    def detect_event(self, entities: dict, history: list) -> dict:
        obj = entities.get("object")
        event = entities.get("event")
        location = entities.get("location")
        
        # 1. DYNAMIC HIGH SEVERITY (ALERTS)
        if obj == "person":
            # If AI sees a person at a sensitive location it detected
            if location in ["fence", "gate", "garage"]:
                return {"event_type": f"unauthorized_{location}_access", "severity": "high"}
            
            # If AI identifies loitering behavior
            if event == "loitering":
                return {"event_type": "suspicious_loitering", "severity": "high"}

        # 2. MEDIUM SEVERITY (WARNINGS)
        if obj in ("car", "truck"):
            if event == "speeding":
                return {"event_type": "speeding_vehicle", "severity": "medium"}

            if location:
                repeat_count = sum(
                    1 for h in history 
                    if h.get("object") == obj and h.get("location") == location
                )
                if repeat_count >= 1:
                    return {"event_type": "repeated_vehicle_sighting", "severity": "medium"}

        # 3. LOW SEVERITY (INFO)
        # Updates whenever AI sees something, even if not a threat
        if obj or location:
            return {"event_type": "general_observation", "severity": "low"}

        return {"event_type": "none", "severity": "none"}

    def analyze_frame(self, description: str, telemetry: dict, history: list) -> dict:
        """Ties extraction and detection together"""
        entities = self.extract_entities(description)
        event_info = self.detect_event(entities, history)

        severity_to_alert = {
            "none": "none",
            "low": "info",
            "medium": "warning",
            "high": "alert"
        }

        return {
            "time": telemetry.get("time"),
            # AI logic first: if VLM sees a location, use it. 
            # Only use telemetry as a fallback.
            "location": entities.get("location") or telemetry.get("location"),
            "object": entities.get("object"),
            "color": entities.get("color"),
            "event": entities.get("event"),
            "alert": severity_to_alert[event_info["severity"]],
            "event_type": event_info["event_type"],
            "severity": event_info["severity"]
        }