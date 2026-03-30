# main.py
from services.analyzer import Analyzer
from services.database import init_db, insert_event, log_to_json, get_repeated_threats 
from services.alert_service import generate_alert
from services.query_service import show_by_object, show_all_events
from simulator.simulator import get_simulated_frames
from services.vlm import VLM

def main():
    print("--- Initializing Drone Security System ---")
    init_db()

    analyzer = Analyzer()
    vlm = VLM()

    frames = get_simulated_frames()
    history = []

    print("\n--- Processing Frames ---\n")

    for frame in frames:
        # -------------------------------
        # Step 1: Get description (AI Vision)
        # -------------------------------
        try:
            if "image" in frame:
                # Use the VLM to 'see' the image
                description = vlm.generate_description(frame["image"])
            else:
                # Fallback to provided description if no image path exists
                description = frame.get("description", "unknown scene")
        except Exception as e:
            print(f"[VLM ERROR] {e}")
            description = frame.get("description", "unknown scene")

        print(f"\n--- New Frame Detected ---")
        print(f"AI Description: {description}")

        # -------------------------------
        # Step 2: Analyze (Turning Text into Structured Data)
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
        # Step 3: Store & Log
        # -------------------------------
        # We 'flatten' the lists to strings for the DB (e.g., ['car'] -> "car")
        db_ready_result = result.copy()
        db_ready_result["object"] = ", ".join(result["object"]) if result["object"] else "none"
        db_ready_result["color"] = ", ".join(result["color"]) if result["color"] else "none"
        db_ready_result["event"] = ", ".join(result["event"]) if result["event"] else "none"

        insert_event(db_ready_result)
        log_to_json(result) # JSON can handle the original lists

        # -------------------------------
        # Step 4: Alerting & Context Update
        # -------------------------------
        generate_alert(result)
        history.append(result)

        print(f"Result: {result['event_type']} | Severity: {result['severity']}")

    print("\n--- Processing Complete: Running Frequency Analysis ---")

    # -------------------------------
    # Step 5: Queries (Fulfilling Requirements)
    # -------------------------------
    
    print("\n--- QUERY: TRUCK EVENTS ---")
    show_by_object("truck")

    print("\n--- QUERY: ALL EVENTS ---")
    show_all_events()

    # Requirement: "Identify objects entered twice today"
    print("\n--- QUERY: REPEATED THREATS (Pattern Recognition) ---")
    repeats = get_repeated_threats(threshold=2)
    
    if repeats:
     for obj, color, count in repeats:
        # If color is "none" or "unknown", just don't print it
        color_str = f"{color} " if color not in ["none", "unknown", None] else ""
        print(f"ALERT: {color_str}{obj} detected {count} times today! (Pattern Identified)")

if __name__ == "__main__":
    main()