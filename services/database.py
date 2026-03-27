import sqlite3
import os
import json
from typing import List, Dict

# --- Step 1: Secure the Path ---
# This ensures the database is created in the project root, not inside 'services'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "drone_security.db")

def log_to_json(event: dict):
    file_path = os.path.join(BASE_DIR, "data", "logs.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except:
            data = []

    data.append(event)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# --- Step 2: Initialize without 'Amnesia' ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # REMOVED: cursor.execute("DROP TABLE IF EXISTS events") 
    # We want to keep data so "Frequency" analysis works over time! 

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
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO events (time, location, object, color, event, alert, event_type, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event.get("time"), event.get("location"), event.get("object"),
        event.get("color"), event.get("event"), event.get("alert"),
        event.get("event_type"), event.get("severity"),
    ))
    conn.commit()
    conn.close()

def query_by_object(object_type: str) -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE object = ?", (object_type,))
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_dict(row) for row in rows]

def query_all() -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()
    conn.close()
    return [_row_to_dict(row) for row in rows]

# --- Step 4: The Frequency Engine ---
def get_repeated_threats(threshold=2):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # We use IFNULL to make sure 'None' values from VLM are treated as 'unknown'
    # This ensures ('truck', None) and ('truck', None) are counted together.
    query = """
    SELECT object, IFNULL(color, 'unknown'), COUNT(*) as frequency 
    FROM events 
    GROUP BY object, IFNULL(color, 'unknown') 
    HAVING frequency >= ?
    """
    
    cursor.execute(query, (threshold,))
    repeats = cursor.fetchall() 
    conn.close()
    return repeats