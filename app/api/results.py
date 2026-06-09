"""Job result lookup, backed by a real in-memory store (replaces the old mock).

Note: JOBS lives in process memory, so it resets on restart and is not shared
across workers. Fine for a single-process hackathon deployment; swap for Redis
or a DB if you scale out.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter()

# job_id -> {"status": queued|running|done|error, "result"/"error": ...}
JOBS: dict[str, dict] = {}


@router.get("/results/{job_id}")
def get_result(job_id: str):
    job = JOBS.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Unknown job_id")
    return {"job_id": job_id, **job}
