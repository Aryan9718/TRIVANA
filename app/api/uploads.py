from fastapi import APIRouter, UploadFile, File

from app.services.storage import save_temp_file

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path, file_id = save_temp_file(file)
    return {"file_id": file_id, "file_path": path}
