# tests/test_cases.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.analyzer import Analyzer


def run_tests():
    analyzer = Analyzer()
    history = []

    test_inputs = [
        {"desc": "Blue truck at gate", "expected": "truck"},
        {"desc": "Person standing near fence", "expected": "person"},
        {"desc": "Red car speeding", "expected": "car"},
    ]

    print("\n--- RUNNING TESTS ---")

    for test in test_inputs:
        result = analyzer.analyze_frame(
            description=test["desc"],
            telemetry={"time": "00:00", "location": "test"},
            history=history
        )
        history.append(result)

        print(f"Input: {test['desc']}")
        print(f"Detected: {result['object']} | Expected: {test['expected']}")
        print("---")