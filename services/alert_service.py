"""
Drone Security Analyst Agent
Module: alert_service.py
Purpose: Generate human-readable alerts from analyzed drone frame events.
"""

def generate_alert(event: dict) -> None:
    level     = event.get("alert", "none")
    obj       = event.get("object", "unknown object")
    location  = event.get("location", "unknown location")
    time      = event.get("time", "unknown time")
    event_type = event.get("event_type", "")

    if level == "alert":
        print(f"[ALERT] {event_type.upper()} - {obj} at {location} at {time}")
    elif level == "warning":
        print(f"[WARNING] {event_type.upper()} - {obj} at {location} at {time}")
    # ignore "info" and "none"