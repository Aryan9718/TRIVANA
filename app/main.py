"""TriVana backend — single consolidated FastAPI service.

Run with:  uvicorn app.main:app --reload

Exposes the real LightGBM exoplanet classifier (no mocks):
    POST /predict          synchronous inference on a light-curve CSV
    POST /predict/async    queue a job, poll /results/{job_id}
    POST /upload           store a file, get an id back
    GET  /results/{job_id} fetch an async job's result
    GET  /health           liveness probe
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import predict, results, uploads
from app.core import config

app = FastAPI(title="TriVana Exoplanet Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, tags=["predict"])
app.include_router(uploads.router, tags=["uploads"])
app.include_router(results.router, tags=["results"])


@app.get("/")
def root():
    return {"service": "TriVana Exoplanet Detection API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
