import sqlite3
import os
import json
from typing import List, Dict

# --- Step 1: Secure the Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "drone_security.db")
LOG_FILE = os.path.join(BASE_DIR, "drone_missions.jsonl") # Updated to .jsonl to prevent IDE errors

# --- Step 2: Initialize Table ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ⚠️ TEMPORARY line to wipe legacy format mismatch rows
    cursor.execute("DROP TABLE IF EXISTS events;")

    # We keep 'IF NOT EXISTS' so we don't wipe history on every drone restart
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            location TEXT,
            object TEXT,
            color TEXT,
            event TEXT,
            alert TEXT,
            event_type TEXT,
            severity TEXT
        )
    """)
    conn.commit()
    conn.close()

# --- Step 3: Standard Helpers ---
def _row_to_dict(row):
    return {
        "id": row[0], "time": row[1], "location": row[2],
        "object": row[3], "color": row[4], "event": row[5],
        "alert": row[6], "event_type": row[7], "severity": row[8],
    }

def insert_event(event: Dict):
    """Expects 'flattened' strings for object, color, and event."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (time, location, object, color, event, alert, event_type, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("time"), 
        event.get("location"), 
        event.get("object"), # String representation for DB consistency
        event.get("color"), 
        event.get("event"), 
        event.get("alert"),
        event.get("event_type"), 
        event.get("severity"),
    ))
    conn.commit()
    conn.close()

def query_by_object(object_type: str) -> List[Dict]:
    """Parses stored JSON object list to find matching objects."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()

    matched = []
    for row in rows:
        raw_object = row[3] or "[]"
        try:
            object_list = json.loads(raw_object)
        except (json.JSONDecodeError, TypeError):
            object_list = [raw_object]

        if any(object_type.lower() == str(item).lower() or object_type.lower() in str(item).lower() for item in object_list):
            matched.append(_row_to_dict(row))

    return matched

def query_all() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_dict(row) for row in rows]

# --- Step 4: The Frequency Engine ---
def get_repeated_threats(threshold=2):
    """Identifies patterns of objects appearing multiple times."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We group by object and color to find specific recurring 'targets'
    query = """
    SELECT object, IFNULL(color, 'unknown'), COUNT(*) as frequency 
    FROM events 
    WHERE object != 'none' AND object != '[]'
    GROUP BY object, IFNULL(color, 'unknown') 
    HAVING frequency >= ?
    ORDER BY frequency DESC
    """
    
    cursor.execute(query, (threshold,))
    repeats = cursor.fetchall() 
    conn.close()
    return repeats

# --- Step 5: JSON Logging for Forensics (Unified and Patched) ---
def log_to_json(event: dict):
    """
    Appends the structured mission analysis result directly into a 
    persistent .jsonl log file for post-flight forensic auditing.
    """
    # Safely ensure the target directory structure exists if parsing sub-directories
    folder_path = os.path.dirname(LOG_FILE)
    if folder_path:
        os.makedirs(folder_path, exist_ok=True)
        
    # Map all telemetry fields cleanly
    log_entry = {
        "time": event.get("time"),
        "location": event.get("location"),
        "object": event.get("object"),
        "color": event.get("color"),
        "event": event.get("event"),
        "battery_level": event.get("battery_level"),
        "estimated_time_remaining_mins": event.get("estimated_time_remaining_mins"),
        "alert": event.get("alert"),
        "event_type": event.get("event_type"),
        "severity": event.get("severity")
    }
    
    try:
        # Append data to the file without destroying historical logs
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"❌ Logger Error: Failed writing to JSON log file: {e}")