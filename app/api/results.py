from fastapi import APIRouter

router = APIRouter()

@router.get("/results/{job_id}")
def get_result(job_id: str):
    # Mock example
    return {"job_id": job_id, "result": "mock result available"}
