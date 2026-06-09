"""Gradio dashboard for the TriVana exoplanet classifier.

This is the friendly upload-and-predict UI. It reuses the SAME inference code
as the FastAPI service (app.services.ml_client), so both share one model and
one feature pipeline — no duplicated logic.

Run from the repository root:
    python -m app.gradio_app

Then open the local URL it prints (default http://127.0.0.1:7860).
"""
import pandas as pd
import gradio as gr

from app.services.ml_client import predict_from_dataframe


def analyze(file):
    if file is None:
        return "⚠️ Please upload a light-curve CSV first.", {}
    try:
        df = pd.read_csv(file.name)
        result = predict_from_dataframe(df)
    except Exception as e:  # noqa: BLE001
        return f"❌ Error: {e}", {}

    summary = (
        f"{result['interpretation']}\n"
        f"Probability of exoplanet: {result['exoplanet_probability']} "
        f"(class {result['predicted_class']})"
    )
    return summary, result["features"]


iface = gr.Interface(
    fn=analyze,
    inputs=gr.File(label="Upload light-curve CSV (must contain a 'flux' column)"),
    outputs=[
        gr.Textbox(label="Prediction"),
        gr.JSON(label="Extracted features"),
    ],
    title="🚀 TriVana — Exoplanet Detector",
    description=(
        "Upload a Kepler light-curve CSV and the LightGBM model predicts the "
        "probability that it contains an exoplanet."
    ),
)

if __name__ == "__main__":
    iface.launch()
