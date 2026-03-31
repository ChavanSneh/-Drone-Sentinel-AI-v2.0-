# tests/test_cases.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.analyzer import Analyzer


def run_tests():
    analyzer = Analyzer()
    history = []

    test_cases = [
        {
            "desc": "Blue truck at gate",
            "expected_first_object": "trucks",
            "expected_severity": "medium",
            "expected_event": "vehicle_near_secure_perimeter",
        },
        {
            "desc": "Person standing near fence",
            "expected_first_object": "person",
            "expected_severity": "high",
            "expected_event": "unauthorized_fence_access",
        },
        {
            "desc": "Red car speeding",
            "expected_first_object": "cars",
            "expected_severity": "medium",
            "expected_event": "speeding_vehicle_detected",
        },
    ]

    for test in test_cases:
        result = analyzer.analyze_frame(
            description=test["desc"],
            telemetry={"time": "00:00", "location": "test"},
            history=history
        )
        history.append(result)

        assert result["object"], f"No object extracted for: {test['desc']}"
        assert result["object"][0] == test["expected_first_object"], (
            f"Object mismatch: expected {test['expected_first_object']}, got {result['object'][0]}"
        )
        assert result["severity"] == test["expected_severity"], (
            f"Severity mismatch: expected {test['expected_severity']}, got {result['severity']}"
        )
        assert result["event_type"] == test["expected_event"], (
            f"Event mismatch: expected {test['expected_event']}, got {result['event_type']}"
        )

    print("All analyzer tests passed.")


if __name__ == "__main__":
    run_tests()