# 🚁 Drone Security Analyst Agent (v1.0)

An advanced AI-powered prototype that transforms raw drone telemetry and visual data into actionable security intelligence. Unlike standard motion detectors, this agent uses a **Vision-Language Model (VLM)** and **Persistent Memory** to understand intent and recognize historical patterns.

---

## 🧠 Overview
This system simulates a real-time drone monitoring pipeline by combining:
- **Perception:** Salesforce/BLIP VLM for deep scene understanding.
- **Reasoning:** A heuristic engine that ranks threats by severity.
- **Memory:** Dual-layer persistence (Short-term Python history + Long-term SQLite).
- **Intelligence:** Automated frequency analysis to identify recurring security risks.

---

## 🏗️ Architecture
The system follows a modular **Perception-Reasoning-Memory** pipeline.



1. **Drone Frame (Image)** → Input via simulated feed.
2. **VLM (BLIP)** → Translates pixels into a natural language description.
3. **Analyzer** → Performs Entity Extraction (Object, Color, Location, Event).
4. **Logic Engine** → Applies security rules to determine Threat Level.
5. **Storage** → Persistent logging in **SQLite** and **JSON**.
6. **Alert Service** → Real-time console notifications based on severity.

---

## 🚀 Key Features

### 1. Visual Understanding (VLM)
Uses the **BLIP** model to generate descriptive narratives rather than simple labels.
- *Input:* Image of a white truck at the gate.
- *Output:* "a white truck parked in front of a gate."

### 2. Stateful Intelligence (Memory)
- **Short-Term Context:** Recognizes behavioral shifts within a single mission (e.g., a person moving from the road to the fence).
- **Long-Term Persistence:** Uses **SQLite** to "remember" objects across different days.

### 3. Automated Pattern Recognition
Fulfills the "Identify objects entered twice" requirement by running a frequency query:
- `ALERT: white truck detected 3 times! (Pattern Identified)`

---

## ⚠️ Threat Detection Rules
| Scenario | Event Type | Severity |
| :--- | :--- | :--- |
| Person loitering | loitering | **High** |
| Person at fence | intrusion_risk | **High** |
| Vehicle speeding | speeding | **Medium** |
| Repeated vehicle | repeated_vehicle | **Medium** |

---

## 🛠️ Tech Stack & AI Tools

### **Core Stack**
- **Python 3.10+**
- **Hugging Face Transformers** (BLIP Model)
- **SQLite** (Relational Indexing)
- **Regex-based NLP** (Entity Extraction)

### **AI-Assisted Development**
As encouraged by the assignment, this project leveraged a multi-LLM workflow (**Claude, Gemini, and ChatGPT**) to:
- Architect the modular service-oriented structure.
- Debug complex VLM inference edge cases.
- Expedite the integration of a relational database for historical indexing.

---

## ▶️ How to Run

### 1. Install Dependencies
```bash
pip install transformers pillow torch
2. Execute the System
Bash
python main.py
3. Testing Persistence
Run the script twice. On the second run, the system will demonstrate its Memory by flagging recurring threats stored in drone_security.db.

---

## 🧠 Design Decisions: Why BLIP?
# I chose BLIP over CLIP because security analysis requires descriptive context. While CLIP is effective for classification, BLIP provides the linguistic detail necessary to differentiate between a "parked truck" and a "speeding truck," which is vital for accurate threat assessment.

## 👨‍💻 Author
# Sneh Chavan AI Engineer Candidate