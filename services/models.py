# services/models.py

class DroneEvent:
    def __init__(self, data: dict):
        self.time = data.get("time")
        self.location = data.get("location")
        self.object = data.get("object")
        self.color = data.get("color")
        self.event = data.get("event")
        self.alert = data.get("alert")
        self.event_type = data.get("event_type")
        self.severity = data.get("severity")

    def to_dict(self):
        return {
            "time": self.time,
            "location": self.location,
            "object": self.object,
            "color": self.color,
            "event": self.event,
            "alert": self.alert,
            "event_type": self.event_type,
            "severity": self.severity,
        }