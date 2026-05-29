import json
from services.analyzer import Analyzer

def test_engine():
    print("🚀 Loading Drone Sentinel 2.0 Test Bench...")
    
    try:
        with open("test_payload.json", "r") as f:
            mock_data = json.load(f)
        print(f"📦 Simulating incoming feed from: {mock_data['drone_id']}")
    except FileNotFoundError:
        print("❌ Error: test_payload.json not found!")
        return
    
    print("⚙️ Initializing Analyzer Engine...")
    
    try:
        engine = Analyzer()
        # Format visual data from payload
        visual_frame_string = f"Scene: {mock_data['raw_vision_summary']['scene_type']}. Detected: {', '.join(mock_data['raw_vision_summary']['detected_objects'])}."
        telemetry_data = mock_data["telemetry"]
        mock_history = [] 
        
        print("⚙️ Feeding variables into .analyze_frame() positionally...")
        
        # Run pipeline
        result = engine.analyze_frame(
            visual_frame_string, 
            telemetry_data, 
            mock_history
        )
        
        print("\n✅ --- ENGINE OUTPUT RESULT ---")
        print(json.dumps(result, indent=4) if isinstance(result, (dict, list)) else result)
        print("--------------------------------\n")
            
    except Exception as e:
        print(f"\n❌ Engine encountered an error: {e}\n")

if __name__ == "__main__":
    test_engine()