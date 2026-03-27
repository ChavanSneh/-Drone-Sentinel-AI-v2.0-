import sqlite3
from typing import List, Dict
import json

def log_to_json(event: dict):
    import json
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "logs.json")

    # Create folder if not exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    # Read existing data
    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []

    data.append(event)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Database file name
DB_NAME = "drone_security.db"


# -------------------------------
# Helper: Convert row → dict
# -------------------------------
def _row_to_dict(row):
    return {
        "id": row[0],
        "time": row[1],
        "location": row[2],
        "object": row[3],
        "color": row[4],
        "event": row[5],
        "alert": row[6],
        "event_type": row[7],
        "severity": row[8],
    }


# -------------------------------
# Initialize DB
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS events")

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


# -------------------------------
# Insert Event (SAFE VERSION)
# -------------------------------
def insert_event(event: Dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (time, location, object, color, event, alert, event_type, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("time"),
        event.get("location"),
        event.get("object"),
        event.get("color"),
        event.get("event"),
        event.get("alert"),
        event.get("event_type"),
        event.get("severity"),
    ))

    conn.commit()
    conn.close()


# -------------------------------
# Query by object
# -------------------------------
def query_by_object(object_type: str) -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events WHERE object = ?", (object_type,))
    rows = cursor.fetchall()

    conn.close()

    return [_row_to_dict(row) for row in rows]


# -------------------------------
# Query all events
# -------------------------------
def query_all() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()

    conn.close()

    return [_row_to_dict(row) for row in rows]