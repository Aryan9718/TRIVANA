import os
import uuid

TEMP_DIR = "app/logs"

def save_temp_file(upload_file):
    os.makedirs(TEMP_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}_{upload_file.filename}")
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path, file_id
