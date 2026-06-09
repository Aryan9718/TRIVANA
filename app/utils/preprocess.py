"""Feature extraction for light-curve CSVs.

The LightGBM model was trained on 10 summary statistics of a star's flux
time-series. These must be produced in the exact order the StandardScaler
expects (see FEATURE_NAMES).
"""
import numpy as np
import pandas as pd

# Order matters: this matches scaler.feature_names_in_.
FEATURE_NAMES = [
    "flux_mean",
    "flux_std",
    "flux_median",
    "flux_min",
    "flux_max",
    "flux_skew",
    "flux_kurt",
    "dip_max",
    "dip_mean",
    "dip_std",
]


def extract_features(df: pd.DataFrame) -> dict:
    """Compute the 10 model features from a light-curve dataframe.

    The dataframe must contain a ``flux`` column (an optional ``flux_err``
    column is accepted but currently unused).
    """
    if "flux" not in df.columns:
        raise ValueError(
            "CSV must contain a 'flux' column. Got columns: "
            + ", ".join(map(str, df.columns))
        )

    flux = pd.to_numeric(df["flux"], errors="coerce").dropna().values
    if flux.size == 0:
        raise ValueError("'flux' column contains no numeric values.")

    flux_series = pd.Series(flux)
    flux_mean = float(np.mean(flux))

    # "Dip" = how far flux drops below its mean; transits show up as dips.
    flux_diff = flux_mean - flux

    features = {
        "flux_mean": flux_mean,
        "flux_std": float(np.std(flux)),
        "flux_median": float(np.median(flux)),
        "flux_min": float(np.min(flux)),
        "flux_max": float(np.max(flux)),
        "flux_skew": float(flux_series.skew()),
        "flux_kurt": float(flux_series.kurt()),
        "dip_max": float(np.max(flux_diff)),
        "dip_mean": float(np.mean(flux_diff)),
        "dip_std": float(np.std(flux_diff)),
    }
    return features
