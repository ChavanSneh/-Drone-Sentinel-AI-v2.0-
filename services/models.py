# services/models.py

from typing import TypedDict, List, Optional

# Instead of a heavy class, we use a TypedDict. 
# This helps with autocomplete in your IDE without adding unnecessary code.

class DroneEvent(TypedDict):
    time: str
    location: str
    object: List[str]
    color: List[str]
    event: List[str]
    alert: str
    event_type: str
    severity: str