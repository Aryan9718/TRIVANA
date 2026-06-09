# 🚀 TriVana — Exoplanet Detection Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118-green)](https://fastapi.tiangolo.com/)

A web platform that detects exoplanets from Kepler light-curve data using machine
learning and visualizes them as interactive 3D worlds. Built for the
**NASA Space Apps Challenge – Noida 2025** (Team TriVana, lead: Abhinav Singh).

---

## 🌌 What it does

- **Demo Mode** — look up a Kepler ID and get an instant 3D orbital visualization.
- **Explore Mode** — upload a light-curve CSV; a LightGBM classifier predicts the
  probability that it contains an exoplanet, and the result drives the 3D scene.

---

## 🧠 The model

A `LightGBM` binary classifier (`exoplanet` / `not exoplanet`) trained on 10
summary features of a star's flux time-series:

```
flux_mean, flux_std, flux_median, flux_min, flux_max,
flux_skew, flux_kurt, dip_max, dip_mean, dip_std
```

Features are standardized with a fitted `StandardScaler` before inference. Both
artifacts live in `app/models/`.

> An experimental CNN (`app/models/best_model.h5`) also exists but is **not wired
> into the API** — it requires TensorFlow and a different preprocessing path.

---

## 🗂 Project structure

```
trivana--backend/
├── app/                     # ← consolidated FastAPI backend (run this)
│   ├── main.py              #   app entry point + CORS + routers
│   ├── api/                 #   route handlers (predict, upload, results)
│   ├── services/            #   ml_client (inference), storage
│   ├── utils/preprocess.py  #   light-curve feature extraction
│   ├── core/config.py       #   paths & settings (env-overridable)
│   ├── models/              #   lgb_exoplanet_model.pkl, scaler.pkl
│   └── requirements.txt
├── TriVana-1/               # frontend (HTML/CSS/JS, React via CDN) + assets
└── TriVana-2/               # data, notebooks, original model-training scripts
```

---

## ▶️ Running the backend

```bash
cd app
python -m venv venv
venv\Scripts\activate          # Windows  (use: source venv/bin/activate on macOS/Linux)
pip install -r requirements.txt

# from the repository root:
cd ..
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for interactive API docs.

### Endpoints

| Method | Path                  | Description                                            |
|--------|-----------------------|--------------------------------------------------------|
| POST   | `/predict`            | Upload a light-curve CSV → prediction (synchronous)    |
| POST   | `/predict/async`      | Queue a prediction job → `{job_id}`                    |
| GET    | `/results/{job_id}`   | Fetch an async job's result                            |
| POST   | `/upload`             | Store a file, get an id back                           |
| GET    | `/health`             | Liveness probe                                          |

**Example**

```bash
curl -X POST http://127.0.0.1:8000/predict -F "file=@lightcurve.csv"
```

```json
{
  "predicted_class": 1,
  "exoplanet_probability": "0.8731",
  "probability": 0.8731,
  "interpretation": "Likely Exoplanet",
  "features": { "flux_mean": 1.0, "...": "..." }
}
```

The CSV must contain a `flux` column (an optional `flux_err` column is accepted).

---

## 🖥 Frontend

The frontend in `TriVana-1/` is static (HTML/CSS/JS with React loaded from a CDN —
no build step). Serve it with any static server, e.g.:

```bash
cd TriVana-1
python -m http.server 5500
```

Point its prediction URL (in `analyze.js`) at your running backend
(`http://127.0.0.1:8000/predict`).

---

## 👥 Team

Team TriVana — Team Lead: Abhinav Singh.
Developed for the NASA Space Apps Challenge – Noida 2025.
