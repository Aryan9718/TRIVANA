from fastapi import APIRouter, BackgroundTasks
import uuid
from app.services.ml_client import mock_predict

router = APIRouter()

def run_prediction_job(job_id: str):
    result = mock_predict()
    print(f"[Job {job_id}] Result:", result)

@router.post("/predict")
async def predict(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(run_prediction_job, job_id)
    return {"job_id": job_id, "status": "started"}
