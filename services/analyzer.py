import re

# -------------------------------
# Keywords
# -------------------------------
OBJECT_KEYWORDS = {
    "person": ["person", "man", "woman"],
    "car": ["car", "vehicle", "suv"],
    "truck": ["truck", "f150", "pickup"] # Added F150 for the assignment spec
}

COLOR_KEYWORDS = ["red", "blue", "white", "black"]

LOCATION_KEYWORDS = {
    "gate": ["gate"],
    "fence": ["fence"],
    "road": ["road", "highway"],
    "garage": ["garage", "parking"]
}

EVENT_KEYWORDS = {
    "parked": ["parked"],
    "loitering": ["loitering", "standing", "waiting", "leaning"],
    "speeding": ["speeding", "fast", "driving", "moving", "riding"]
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
        
        # --- PRIORITY 1: HIGH SEVERITY (ALERTS) ---
        if obj == "person" and event == "loitering":
            return {"event_type": "loitering", "severity": "high"}

        if obj == "person" and location == "fence":
            return {"event_type": "intrusion_risk", "severity": "high"}

        # --- PRIORITY 2: MEDIUM SEVERITY (WARNINGS) ---
        if obj in ("car", "truck") and event == "speeding":
            return {"event_type": "speeding", "severity": "medium"}

        if obj in ("car", "truck") and location:
            repeat_count = sum(
                1 for h in history
                if h.get("object") == obj and h.get("location") == location
            )
            if repeat_count >= 1:
                return {"event_type": "repeated_vehicle", "severity": "medium"}

        return {"event_type": "none", "severity": "none"}

    def analyze_frame(self, description: str, telemetry: dict, history: list) -> dict:
        """Ties extraction and detection together for the main loop"""
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
            "location": telemetry.get("location") or entities.get("location"),
            "object": entities.get("object"),
            "color": entities.get("color"),
            "event": entities.get("event"),
            "alert": severity_to_alert[event_info["severity"]],
            "event_type": event_info["event_type"],
            "severity": event_info["severity"]
        }