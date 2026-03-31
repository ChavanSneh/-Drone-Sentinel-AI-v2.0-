import logging
import os
import json
import config

# Use the config to silence logs
for lib in config.SILENCED_LIBRARIES:
    logging.getLogger(lib).setLevel(logging.ERROR)

def main():
    vlm = VLM(model_id=config.MODEL_ID, device=config.DEVICE)
    # ... use config.IMAGE_SOURCE, config.DB_PATH, etc.

# 1. SHUT DOWN LIBRARY LOGGING (Do this before importing transformers/VLM)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)

# 2. OPTIONAL: Tell Hugging Face to stop checking for updates every time
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from services.analyzer import Analyzer
from services.database import init_db, insert_event, log_to_json, get_repeated_threats 
from services.alert_service import generate_alert
from services.query_service import show_by_object, show_all_events
from simulator.simulator import get_simulated_frames
from services.vlm import VLM

# 3. CONFIGURE YOUR LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("drone.log"),
        logging.StreamHandler()
    ]
)

def main():

    logging.info("--- Initializing Drone Security System ---")
    init_db()

    analyzer = Analyzer()
    vlm = VLM()

    frames = get_simulated_frames()
    history = []

    logging.info("--- Starting Frame Processing Flow ---")

    for frame in frames:
        # -------------------------------
        # Step 1: AI Perception (VLM)
        # -------------------------------
        try:
            if "image" in frame:
                description = vlm.generate_description(frame["image"])
            else:
                description = frame.get("description", "unknown scene")
            
            # Handle potential error strings returned by VLM
            if "error" in description:
                logging.error(f"Vision failure: {description}")
        except Exception as e:
            logging.error(f"Unexpected VLM crash: {e}")
            description = "observation failure"

            # This hides the 404/Connection logs from Hugging Face
            logging.getLogger("transformers").setLevel(logging.ERROR)
            logging.getLogger("httpx").setLevel(logging.ERROR)
            logging.basicConfig(...) # Keep your existing config here

            # --- ADD THESE LINES TO HIDE THE NOISE ---
            logging.getLogger("transformers").setLevel(logging.ERROR)
            logging.getLogger("httpx").setLevel(logging.ERROR)

        # -------------------------------
        # Step 2: Reasoning (NLP Analysis)
        # -------------------------------
        result = analyzer.analyze_frame(
            description=description,
            telemetry={
                "time": frame.get("time"),
                "location": frame.get("location")
            },
            history=history
        )

        # -------------------------------
        # Step 3: Persistence (Data Integrity)
        # -------------------------------
        
        # PRO-FIX: Use JSON serialization instead of comma-joining
        # This prevents the "comma collision" bug Copilot mentioned
        db_ready_result = result.copy()
        db_ready_result["object"] = json.dumps(result["object"])
        db_ready_result["color"] = json.dumps(result["color"])
        db_ready_result["event"] = json.dumps(result["event"])

        try:
            insert_event(db_ready_result)
            log_to_json(result)
        except Exception as e:
            logging.error(f"Database insertion failed: {e}")

        # -------------------------------
        # Step 4: Execution (Alerts & Context)
        # -------------------------------
        generate_alert(result)
        history.append(result)
        
        # Log the result to the console and file
        logging.info(f"Processed Frame: {result['event_type']} | Severity: {result['severity']}")

    # -------------------------------
    # Step 5: Intelligence Queries
    # -------------------------------
    print("\n" + "="*40)
    print("ANALYSIS REPORT")
    print("="*40)

    print("\n--- QUERY: TRUCK EVENTS ---")
    show_by_object("trucks") # Updated to match your new plural labels

    print("\n--- QUERY: ALL EVENTS ---")
    show_all_events()

    print("\n--- QUERY: REPEATED THREATS (Pattern Recognition) ---")
    repeats = get_repeated_threats(threshold=2)
    
    if repeats:
        for obj, color, count in repeats:
            # Clean up JSON strings if they come back from the DB
            obj_name = obj.strip('"[]') 
            color_str = f"{color} " if color not in ["none", "unknown", None] else ""
            logging.warning(f"PATTERN IDENTIFIED: {color_str}{obj_name} detected {count} times!")
    else:
        print("No repeated threats identified in this session.")

if __name__ == "__main__":
    main()