import os

# --- SYSTEM MODES ---
IS_SIMULATION = True  # Toggle this to False when connecting to a real camera
DEBUG_MODE = True     # Controls the "Nuclear Silence" logging level

# --- PATHS & DIRECTORIES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_SOURCE = os.path.join(BASE_DIR, "data/images")
DB_PATH = os.path.join(BASE_DIR, "drone_security.db")
LOG_FILE = os.path.join(BASE_DIR, "drone.log")

# --- VLM MODEL SETTINGS ---
MODEL_ID = "Salesforce/blip-image-captioning-base"
DEVICE = "cpu"  # Change to "cuda" if you have an NVIDIA GPU

# --- SECURITY LOGIC ---
REPEATED_THRESHOLD = 3   # Alert if an object is seen 3+ times
SEVERITY_MAPPING = {
    "truck": "Medium",
    "person": "Medium",
    "fence_climbing": "High",
    "stuck": "High"
}

# --- LOGGING CONFIG ---
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
SILENCED_LIBRARIES = ["transformers", "httpx", "huggingface_hub"]