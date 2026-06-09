import os
import uuid

from app.core import config


def save_temp_file(upload_file):
    """Persist an UploadFile to the temp dir; return (path, file_id)."""
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(config.TEMP_DIR, f"{file_id}_{upload_file.filename}")
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path, file_id
