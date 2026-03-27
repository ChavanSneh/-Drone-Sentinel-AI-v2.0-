# main.py

from services.analyzer import Analyzer
# Added get_repeated_threats to the imports
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
        # Step 1: Get description (VLM or fallback)
        # -------------------------------
        try:
            if "image" in frame:
                description = vlm.generate_description(frame["image"])
            else:
                description = frame.get("description", "unknown scene")
        except Exception as e:
            print(f"[VLM ERROR] {e}")
            description = frame.get("description", "unknown scene")

        print(f"\nFrame: {frame}")
        print(f"Generated Description: {description}")

        # -------------------------------
        # Step 2: Analyze
        # -------------------------------
        result = analyzer.analyze_frame(
            description=description,
            telemetry={
                "time": frame["time"],
                "location": frame["location"]
            },
            history=history
        )

        print(result)

        # -------------------------------
        # Step 3: Store
        # -------------------------------
        insert_event(result)
        log_to_json(result)

        # -------------------------------
        # Step 4: Alert
        # -------------------------------
        generate_alert(result)

        # -------------------------------
        # Step 5: Update context
        # -------------------------------
        history.append(result)

    print("\n--- All Events Stored ---")

    # -------------------------------
    # Step 6: Queries & Frequency Analysis
    # -------------------------------
    
    # Requirement: "show all truck events" [cite: 37]
    print("\n--- QUERY: TRUCK EVENTS ---")
    show_by_object("truck")

    print("\n--- QUERY: ALL EVENTS ---")
    show_all_events()

    # Requirement: "identify objects entered twice today" 
    print("\n--- QUERY: REPEATED THREATS (Frequency Analysis) ---")
    repeats = get_repeated_threats(threshold=2)
    
    if repeats:
        for obj, color, count in repeats:
            print(f"ALERT: {color} {obj} detected {count} times! (Pattern Identified)")
    else:
        print("No repeated threats detected.")

if __name__ == "__main__":
    main()