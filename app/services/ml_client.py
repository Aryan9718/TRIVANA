"""Real ML inference: load the LightGBM model + scaler once and run predictions.

This replaces the previous mock_predict() placeholder.
"""
import threading

import joblib
import pandas as pd

from app.core import config
from app.utils.preprocess import FEATURE_NAMES, extract_features

_model = None
_scaler = None
_lock = threading.Lock()


def _load():
    """Lazily load model + scaler the first time a prediction is requested."""
    global _model, _scaler
    if _model is None or _scaler is None:
        with _lock:
            if _model is None:
                _model = joblib.load(config.MODEL_PATH)
            if _scaler is None:
                _scaler = joblib.load(config.SCALER_PATH)
    return _model, _scaler


def predict_from_dataframe(df: pd.DataFrame) -> dict:
    """Run the full pipeline on a light-curve dataframe and return a result dict.

    Response shape matches what the frontend (analyze.js) expects:
        predicted_class, exoplanet_probability, interpretation
    plus the extracted features for transparency.
    """
    model, scaler = _load()

    features = extract_features(df)
    # Build a single-row frame with the column names the scaler was fit on,
    # so feature order is guaranteed and sklearn emits no name-mismatch warning.
    X = pd.DataFrame([[features[name] for name in FEATURE_NAMES]], columns=FEATURE_NAMES)
    X_scaled = scaler.transform(X)

    prob = float(model.predict_proba(X_scaled)[0][1])
    predicted_class = int(prob >= config.PROB_THRESHOLD)

    return {
        "predicted_class": predicted_class,
        "exoplanet_probability": f"{prob:.4f}",
        "probability": prob,
        "interpretation": "Likely Exoplanet" if predicted_class == 1 else "Not an Exoplanet",
        "features": features,
    }


def predict_from_csv(file_like) -> dict:
    """Read a CSV (path or file-like object) and predict."""
    df = pd.read_csv(file_like)
    return predict_from_dataframe(df)
