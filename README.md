# 🚁 Drone Sentinel AI (v2.0)

An advanced Autonomous AI Orchestration Engine that transforms raw drone visual data into structured, actionable security intelligence.

Version 2.0 introduces a Distributed Architecture, separating high-compute Edge Vision from Ground Station Control for a production-ready simulation with self-contained hardware state management.

---

## 🏗️ System Architecture: The "Air-to-Ground" Handshake

This project is architected as a modular, service-oriented ecosystem designed for real-world robotics deployment.

### 1. The Drone (Edge Intelligence)
* **Perception (`vlm.py`):** Uses the Salesforce/BLIP Vision-Language Model to narrate the environment in real-time.
* **Resiliency Layer:** Implemented Pre-Flight Guardrails that verify file integrity before inference, preventing system crashes during intermittent or corrupted data streams.
* **Reasoning (`analyzer.py`):** A custom heuristic state machine engine that extracts entities, dynamically tracks hardware levels, and ranks threats by severity matrix rankings.

### 2. The Ground Station (Control & Memory)
* **Simulation Suite (`simulator.py`):** Generates a high-fidelity synthetic environment to stress-test the AI's logic.
* **Relational Memory (`database.py`):** Powered by SQLite for long-term indexing. v2.0 utilizes JSON Serialization to store complex object lists, ensuring 100% data integrity for multi-object detections.

### 3. Black Box Recorder (`drone.log`)
A professional logging framework that records every system event, error, hardware metric variation, and sighting for post-flight forensic auditing.

---

## 🚀 Key Features & v2.0 Updates

### 🔋 Autonomous Hardware Simulation & Time-Delta State Machine
Drone Sentinel 2.0 maps to a high-end commercial surveillance profile (similar to a 1,000 Wh enterprise setup with an effective 45-minute operational limit). 
Instead of relying on static mock metrics, the core engine features an autonomous **Time-Delta Battery Depletion** function. It calculates the exact elapsed time between frames via incoming ISO timestamps and dynamically drains the battery level at an operational cruise rate of **2.5% per minute**.

### 🚨 Priority-0 Emergency Fail-Safe
The reasoning core features a hard-coded master circuit breaker. If the time-delta tracker calculates that the drone's internal charge has dropped to **20% or lower**, the engine overrides all lower-level entity threat detections, cancels current perimeter checks, logs a high-severity hardware warning, and immediately returns the specialized emergency response action.

### 💾 High-Integrity Data Persistence
We migrated from fragile comma-separated strings to **Safe JSON Serialization**.
* **The Problem:** Traditional string structures break if an AI description contains a literal comma (e.g., `"a car, blue, and a truck"`).
* **The Solution:** Utilizing `json.dumps()` ensures that complex multi-object arrays and environmental colors are stored and retrieved as clean structured objects with 100% precision.

### 🔇 Intelligent Signal-to-Noise Management
Implemented a **Nuclear Silence** logging strategy. Deep background telemetry and initialization clutter from secondary AI libraries (*Hugging Face, HTTPX, PyTorch, Transformers*) are suppressed at the kernel level. This keeps the operator's console beautifully clean, displaying only mission-critical flight events and security matches.

### 📈 Stateful Pattern Recognition
By indexing sightings in a persistent database across operational sequences, the agent recognizes recurring threats across different flight paths. 
* *Example Sighting Alert:* `WARNING: White truck detected 3 times this week (Pattern Identified).`

---

## ⚠️ Threat Detection Matrix

The core engine uses regex word-boundary parsing (`\b`) to cross-reference extracted VLM descriptions against specialized matrices, resolving actions by priority levels:

| Priority | Scenario | Event Type | Severity | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Priority 0** | **Low Juice Critical Threshold** | `critical_battery_emergency_landing` | **HIGH** | Immediate Landing Override |
| **Priority 1** | Asset Blockage / Jammed | `object_stuck_at_[location]` | **HIGH** | Operator Alert & DB Log |
| **Priority 1** | Secure Boundary Intrusion | `unauthorized_[location]_access` | **HIGH** | Operator Alert & DB Log |
| **Priority 2** | Persistent Vehicle Suspect | `repeated_vehicle_at_[location]` | **MEDIUM** | System Warning |
| **Priority 2** | Vehicle Speeding Vector | `speeding_vehicle_detected` | **MEDIUM** | System Warning |
| **Priority 3** | Routine Patrol Sightings | `observing_[object]` / `monitoring_[location]`| **LOW** | Stream Info Update |

---

## 🧪 How to Test the Engine Locally

Drone Sentinel 2.0 includes an automated simulation test bench (`run_test.py`) to verify vision parsing, time-delta battery decay, and threat-escalation loops instantly.

### 1. Execute the Pipeline Runner
Execute the test script in your VS Code or system terminal to spin up the mock architecture:

python run_test.py
