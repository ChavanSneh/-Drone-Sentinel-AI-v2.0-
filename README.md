## 🚁 Drone Security Analyst Agent

# An AI-powered prototype that analyzes drone telemetry and visual data to detect security-relevant events such as loitering, speeding, and suspicious vehicle activity.

# ---

## 🧠 Overview

# This system simulates a real-time drone monitoring pipeline by combining:

# - 🖼️ Vision-Language Model (VLM) for scene understanding
# - 🧾 Text-based semantic analysis for structured extraction
# - ⚙️ Rule-based reasoning engine for threat detection
# - 💾 Persistence layer for logging and querying events
# - 🚨 Alert system for real-time notifications

# The goal is to demonstrate how AI + system design can be used for intelligent surveillance.

# ---

## 🏗️ Architecture

# Drone Frame (Image)
#         ↓
# VLM (BLIP Image Captioning)
#         ↓
# Generated Description (Text)
#         ↓
# Analyzer (Entity Extraction + Rules)
#         ↓
# Event Classification (Threat Level)
#         ↓
# Storage (SQLite + JSON Logs)
#         ↓
# Alert Service (Console Output)

# ---

## ⚙️ Tech Stack

# - Python
# - Hugging Face Transformers (BLIP model)
# - SQLite (event storage)
# - JSON (logging)
# - Regex-based NLP (entity extraction)

# ---

## 📂 Project Structure

# drone_agent/
# │
# ├── main.py
# ├── config.py
# │
# ├── services/
# │   ├── analyzer.py
# │   ├── database.py
# │   ├── alert_service.py
# │   ├── query_service.py
# │   └── vlm.py
# │
# ├── simulator/
# │   └── simulator.py
# │
# ├── data/
# │   ├── images/
# │   └── logs.json
# │
# └── tests/
#    └── test_cases.py

# ---

## 🚀 Features

# 🔍 1. Visual Understanding (VLM)

- # Uses BLIP model to generate natural language descriptions from images
- # Example:
#   Input Image → "a man standing in front of a fence"

# ---

# 🧠 2. Entity Extraction

# Extracts structured data from text:

# {
#   "object": "person",
#   "location": "fence",
#   "event": "loitering"
# }

# ---

# ⚠️ 3. Threat Detection Rules

# Scenario| Event Type| Severity
# Person loitering| loitering| High
# Vehicle speeding| speeding| Medium
# Repeated vehicle| repeated_vehicle| Medium
# Multiple vehicles| multiple_vehicle_activity| Medium

# ---

# 💾 4. Storage Layer

# - SQLite DB → structured event storage
# - logs.json → raw event logging

# ---

# 🚨 5. Alert System

# Console-based alerts:

# [ALERT] LOITERING - person at fence at 00:03
# [WARNING] SPEEDING - car at road at 00:12

# ---

# 🔎 6. Query System

# - Query by object (e.g., trucks)
# - View all events

---

## ▶️ How to Run

# 1. Install dependencies

# pip install transformers pillow torch

# ---

# 2. Run the system

# python main.py

# ---

# 3. Output Example

# Generated Description: a man standing in front of a fence

# [ALERT] LOITERING - person at fence at 00:03
# [WARNING] SPEEDING - car at road at 00:12

# ---

## 🧠 Design Decisions

# 🔹 VLM + Rule Hybrid Approach

# Instead of relying purely on AI, the system:

# - Uses VLM for perception
# - Uses rules for deterministic decision-making

# ---

# 🔹 Context-Aware Detection

# Maintains history of previous frames to detect:

# - Repeated vehicles
# - Behavioral patterns

# ---

# 🔹 Robustness

# - Fallback to text descriptions if image processing fails
# - Handles incomplete or noisy VLM outputs

# ---

## 🔮 Future Improvements

# - Object tracking (DeepSORT)
# - Real-time streaming (Kafka / WebSockets)
# - Advanced LLM reasoning (LangChain agents)
# - Geofencing integration
# - Multi-camera support

# ---

## 📌 Summary

# This project demonstrates how to build a modular AI system that integrates:

# - Vision
# - Language
# - Logic
# - Memory

# to simulate a real-world drone surveillance intelligence pipeline.

# ---

## 👨‍💻 Author

# Sneh Chavan

# ---

## 🚀 Final Note

## This is not just a script — it's a prototype of an intelligent monitoring system designed with scalability and modularity in mind.