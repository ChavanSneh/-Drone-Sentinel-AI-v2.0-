# Drone Sentinel AI (v2.0)

An advanced Autonomous AI Orchestration Engine that transforms raw drone visual data into structured, actionable security intelligence.

Version 2.0 introduces a **Distributed Architecture**, separating high-compute Edge Vision from Ground Station Control for a production-ready simulation with self-contained hardware state management, high-speed telemetry logging, and robust path security.

---

## System Architecture: The "Air-to-Ground" Handshake

This project is architected as a modular, service-oriented ecosystem designed for real-world robotics deployment.

### 1. The Drone (Edge Intelligence)
* **Perception (`vlm.py`):** Uses the `Salesforce/BLIP` Vision-Language Model to narrate the environment in real-time.
* **Resiliency Layer:** Implemented Pre-Flight Guardrails that verify file integrity before inference, preventing system crashes during intermittent or corrupted data streams.
* **Reasoning (`analyzer.py`):** A custom heuristic state machine engine that extracts entities, dynamically tracks hardware levels, and ranks threats by severity matrix rankings.

### 2. The Ground Station (Control & Memory)
* **Simulation Suite (`simulator.py`):** Generates a high-fidelity synthetic environment to stress-test the AI's logic.
* **Relational Memory (`services/database.py`):** Powered by SQLite for long-term indexing. It utilizes strict text-mapping logic to keep relational query execution consistent while isolating raw telemetry arrays.

### 3. Black Box Forensic Recorder (`drone_missions.jsonl`)
* A streamlined, lightning-fast **Newline-Delimited JSON (NDJSON)** logging engine that streams frame analysis data directly to the disk, guaranteeing atomic file operations without memory bloating or structural parse errors.

---

## Key Features & v2.0 Updates

### 🔋 Autonomous Hardware Simulation & Time-Delta State Machine
Drone Sentinel 2.0 maps to a high-end commercial surveillance profile (similar to a 1,000 Wh enterprise setup with an effective 32-minute operational limit). Instead of relying on static mock metrics, the core engine features an autonomous **Time-Delta Battery Depletion** function. It calculates the exact elapsed time between frames via incoming ISO timestamps and dynamically drains the battery level down to fractional floats at runtime.

### 🚨 Priority-0 Emergency Fail-Safe
The reasoning core features a hard-coded master circuit breaker. If the time-delta tracker calculates that the drone's internal charge has dropped to **20% or lower**, the engine overrides all lower-level entity threat detections, cancels current perimeter checks, logs a high-severity hardware warning, and immediately triggers an emergency return-to-base landing action.

### 💾 Newline-Delimited JSON (`.jsonl`) Forensic Storage
We migrated from traditional JSON array structures (`[]`) to high-speed **NDJSON Lines** for post-flight forensic auditing.
* **The Problem:** Reading a massive standard JSON file into memory, appending an event, and rewriting the entire file (`"w"` mode) crashes if it encounters malformed formatting, while drastically increasing disk I/O bottlenecks.
* **The Solution:** Utilizing high-speed append-only (`"a"`) stream writing. Every flight frame creates a clean, independent JSON row object ending in a newline (`\n`). This ensures zero memory overhead, fast write execution, and a complete history log that grows across sequential missions without deleting previous flight data.

### 🗺️ Dynamic Path Security & Fail-Safe Directories
To prevent runtime environment path crashes across different operating systems, the storage architecture features an automated environment path wrapper:
* **Dynamic Roots:** Automatically maps `BASE_DIR` dynamically from the execution origin to target internal assets precisely.
* **Safe-Directory Creation:** Features a wrapper that cleanly verifies if nested parent directory paths exist before initiating file handles, preventing empty-string directory initialization errors.

### 📈 Stateful Pattern Recognition
By indexing sightings in a persistent database across operational sequences, the agent automatically surfaces recurring threats across different flight paths. 
* *Note:* Database schemas are hardened to prevent schema contamination between historical raw-text telemetry arrays and incoming JSON Lines models.

---

## Threat Detection Matrix

The core engine uses regex word-boundary parsing (`\b`) to cross-reference extracted VLM descriptions against specialized matrices, resolving actions by priority levels:

| Priority | Scenario | Event Type | Severity | Action |
| :--- | :--- | :--- | :--- | :--- |
| **Priority 0** | Low Juice Critical Threshold | `critical_battery_emergency_landing` | **HIGH** | Immediate Landing Override |
| **Priority 1** | Asset Blockage / Jammed | `object_stuck_at_[location]` | **HIGH** | Operator Alert & DB Log |
| **Priority 1** | Secure Boundary Intrusion | `unauthorized_[location]_access` | **HIGH** | Operator Alert & DB Log |
| **Priority 2** | Persistent Vehicle Suspect | `repeated_vehicle_at_[location]` | **MEDIUM** | System Warning |
| **Priority 2** | Vehicle Speeding Vectors | `speeding_vehicle_detected` | **MEDIUM** | System Warning |
| **Priority 3** | Routine Patrol Sightings | `observing_[object]` / `monitoring_[location]` | **LOW** | Stream Info Update |

---

## How to Test the Engine Locally

Drone Sentinel 2.0 includes an automated simulation test bench (`run_test.py`) to verify vision parsing, time-delta battery decay, and threat-escalation loops instantly without loading heavy visual machine learning models.

### 1. Run the Sandbox Engine Test Stand
To isolate the logic analyzer from the physical VLM image models and hardware dependencies, execute the test bench file:

python run_test.py

### 2. Execute the Full Telemetry Pipeline
To launch the full operational architecture including the VLM environment processing and live telemetry pipeline:

python main.py
