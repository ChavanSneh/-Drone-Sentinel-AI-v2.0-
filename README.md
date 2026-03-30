# 🚁 Drone Security Analyst Agent (v2.0)

An advanced **AI-powered orchestration engine** that transforms raw drone visual data into structured security intelligence. Unlike standard motion detectors, this agent utilizes a **Vision-Language Model (VLM)** and **Persistent Relational Memory** to understand intent, detect anomalies, and recognize historical behavioral patterns.

---

## 🧠 System Overview

This system simulates a real-time drone monitoring pipeline by combining three core pillars of **AI Engineering**:

* **Perception:** Utilizing `Salesforce/BLIP` VLM for deep scene understanding and natural language narration.
* **Reasoning:** A heuristic engine that performs **Entity Extraction** and ranks threats by severity based on environmental context.
* **Memory:** Dual-layer persistence using short-term Python history and long-term **SQLite** relational indexing.

---

## 🏗️ Architecture & Logic Flow

The system follows a modular **Perception-Reasoning-Memory** pipeline:

1.  **Visual Input:** Simulated drone frames (Images or raw VLM descriptions).
2.  **VLM Inference:** Translates pixels into high-context natural language narratives.
3.  **NLP Analyzer:** Extracts structured entities (Objects, Colors, Locations, Events) using **Normalized Keyword Mapping**.
4.  **Logic Engine:** Compares current sightings against historical data to escalate threat levels dynamically.
5.  **Relational Storage:** Persistent logging in **SQLite** and **JSON** for long-term pattern recognition.

---

## 🚀 Key Features

### 1. Visual Narrative Processing (VLM)
Uses the **BLIP** model to generate descriptive context rather than simple labels.
* **Input:** Image of semi-trucks in a parking lot.
* **Output:** `"a row of semi trucks parked in a parking lot"`

### 2. Data Normalization Strategy
The system handles "messy" AI input by mapping linguistic variations (e.g., *"semi," "lorry,"* or *"trucks"*) to a consistent **Relational Key** (`trucks`). This ensures 100% accuracy in database queries and frequency counts.

### 3. Stateful Behavioral Intelligence
* **Short-Term Context:** Recognizes shifts within a single mission (e.g., a vehicle moving from a road to being **"stuck"** at a gate).
* **Pattern Recognition:** Identifies objects entering the perimeter multiple times across different days or sessions.
    > **Example Alert:** `trucks detected 5 times today! (Pattern Identified)`

---

## ⚠️ Threat Detection Matrix

| Scenario | Event Type | Severity | Alert Level |
| :--- | :--- | :--- | :--- |
| **Object Trapped/Blocked** | `object_stuck_at_[location]` | **High** | Alert |
| **Unauthorized Access** | `unauthorized_fence_access` | **High** | Alert |
| **Repeated Sighting** | `repeated_vehicle_at_road` | **Medium** | Warning |
| **Active Patrol** | `monitoring_road` | **Low** | Info |

---

## 🛠️ Tech Stack

### Core Technologies
* **Language:** Python 3.10+
* **Vision:** Hugging Face Transformers (`BLIP-base`)
* **Database:** SQLite3 (Relational Indexing)
* **NLP:** Regex-based Entity Extraction

### AI-Assisted Development
This project leveraged a multi-LLM workflow (**Gemini, ChatGPT, and Claude**) to architect the service-oriented structure, debug complex VLM inference edge cases, and optimize relational database queries.

---

## ▶️ Installation & Usage

### 1. Install Dependencies

pip install transformers pillow torch

2. Execute the System

python main.py

3. Test Persistence

Run the script multiple times. The system will demonstrate its Relational Memory by flagging recurring threats stored in drone_security.db, even after the script is restarted.
---

## 👨‍💻 Author

# Sneh Chavan

# AI Product Engineer | Specializing in Rapid Prototyping & AI Orchestration
