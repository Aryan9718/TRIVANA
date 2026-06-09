"""Application configuration.

Values can be overridden via environment variables, e.g. set MODEL_PATH or
API_KEY before launching uvicorn.
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent          # .../app
MODELS_DIR = BASE_DIR / "models"

# Model artifacts (LightGBM classifier + its StandardScaler)
MODEL_PATH = os.getenv("MODEL_PATH", str(MODELS_DIR / "lgb_exoplanet_model.pkl"))
SCALER_PATH = os.getenv("SCALER_PATH", str(MODELS_DIR / "scaler.pkl"))

# Where uploaded files are temporarily stored
TEMP_DIR = os.getenv("TEMP_DIR", str(BASE_DIR / "logs"))

# CORS: which origins may call the API. "*" is fine for a hackathon/static
# frontend; tighten for production.
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Decision threshold for calling a light curve an exoplanet.
PROB_THRESHOLD = float(os.getenv("PROB_THRESHOLD", "0.5"))
