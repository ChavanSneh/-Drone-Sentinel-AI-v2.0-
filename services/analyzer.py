# services/analyzer.py

import re

# -------------------------------
# Keywords
# -------------------------------

OBJECT_KEYWORDS = {
    "person": ["person", "man", "woman"],
    "car": ["car", "vehicle", "suv"],
    "truck": ["truck"]
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


# -------------------------------
# Analyzer Class
# -------------------------------

class Analyzer:

    # -------------------------------
    # Extract Entities
    # -------------------------------
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

    # -------------------------------
    # Detect Events (FINAL LOGIC)
    # -------------------------------
    def detect_event(self, entities: dict, history: list) -> dict:
        obj = entities.get("object")
        event = entities.get("event")
        color = entities.get("color")
        location = entities.get("location")

        # Default
        result = {"event_type": "none", "severity": "none"}

        # -------------------------------
        # Rule 1: Loitering (HIGH)
        # -------------------------------
        if obj == "person" and event == "loitering":
            return {"event_type": "loitering", "severity": "high"}

        # -------------------------------
        # Rule 2: Speeding (MEDIUM)
        # -------------------------------
        if obj in ("car", "truck") and event == "speeding":
            return {"event_type": "speeding", "severity": "medium"}

        # -------------------------------
        # Rule 3: Repeated Vehicle (MEDIUM)
        # Same type at same location
        # -------------------------------
        if obj in ("car", "truck"):
            repeat_count = sum(
                1 for h in history
                if h.get("object") == obj
                and h.get("location") == location
            )
            if repeat_count >= 1:
                return {"event_type": "repeated_vehicle", "severity": "medium"}

        # -------------------------------
        # Rule 4: Multiple Vehicle Activity (MEDIUM)
        # Many vehicles at same location
        # -------------------------------
        if obj in ("car", "truck"):
            vehicle_count = sum(
                1 for h in history
                if h.get("object") in ("car", "truck")
                and h.get("location") == location
            )
            if vehicle_count >= 2:
                return {"event_type": "multiple_vehicle_activity", "severity": "medium"}

        return result
    
        # -------------------------------
        # Rule 5: Loitering (HIGH)
        # -------------------------------
        if obj == "person" and "fence" in location:
            return {"event_type": "intrusion_risk", "severity": "high"}

    # -------------------------------
    # Main Function
    # -------------------------------
    def analyze_frame(self, description: str, telemetry: dict, history: list) -> dict:
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
            # ✅ FIXED: prioritize telemetry location
            "location": telemetry.get("location") or entities.get("location"),
            "object": entities.get("object"),
            "color": entities.get("color"),
            "event": entities.get("event"),
            "alert": severity_to_alert[event_info["severity"]],
            "event_type": event_info["event_type"],
            "severity": event_info["severity"]
        }