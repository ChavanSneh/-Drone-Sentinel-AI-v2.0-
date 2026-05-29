# simulator/simulator.py

from datetime import datetime, timezone

def get_simulated_frames():
    """Generates synthetic flight telemetry data with fully automatic live timestamps."""
    
    # Automatically get the exact current time in standard ISO format
    current_iso_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return [
        {
            "time": current_iso_time,  # 🤖 100% Automatic!
            "location": "gate",
            "description": "a silver car parked near the entrance entry gate"
        },
        {
            "time": current_iso_time,  # 🤖 100% Automatic!
            "location": "fence",
            "description": "a individual person wearing a white shirt standing near the perimeter boundary wall"
        },
        {
            "time": current_iso_time,  # 🤖 100% Automatic!
            "location": "fence",
            "description": "a blue and white truck idling right beside the security wall fence"
        },
        {
            "time": current_iso_time,  # 🤖 100% Automatic!
            "location": "road",
            "image": "data/images/car.jpg" 
        }
    ]