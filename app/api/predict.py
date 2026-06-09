"""Prediction endpoints.

- POST /predict        synchronous: upload a light-curve CSV, get the result back
                       immediately (this is what the frontend calls).
- POST /predict/async  fire-and-forget: returns a job_id; poll GET /results/{job_id}.
"""
import uuid

from fastapi import APIRouter, BackgroundTasks, File, UploadFile
from fastapi.responses import JSONResponse

from app.api.results import JOBS
from app.services.ml_client import predict_from_csv

router = APIRouter()


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Run real LightGBM inference on an uploaded light-curve CSV."""
    try:
        result = predict_from_csv(file.file)
        return JSONResponse(content=result)
    except ValueError as e:
        # Bad input (missing column, empty flux, ...). Return 200 with an
        # `error` field so the frontend can surface the message directly.
        return JSONResponse(content={"error": str(e)}, status_code=200)
    except Exception as e:  # noqa: BLE001 - surface unexpected failures as 500
        return JSONResponse(content={"error": f"Prediction failed: {e}"}, status_code=500)


def _run_job(job_id: str, file_path: str):
    JOBS[job_id] = {"status": "running"}
    try:
        result = predict_from_csv(file_path)
        JOBS[job_id] = {"status": "done", "result": result}
    except Exception as e:  # noqa: BLE001
        JOBS[job_id] = {"status": "error", "error": str(e)}


@router.post("/predict/async")
async def predict_async(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Queue a prediction job. Read the saved file then process in the background."""
    from app.services.storage import save_temp_file

    file_path, _ = save_temp_file(file)
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued"}
    background_tasks.add_task(_run_job, job_id, file_path)
    return {"job_id": job_id, "status": "queued"}
