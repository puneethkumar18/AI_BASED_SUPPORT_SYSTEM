import uuid
import shutil

from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIRS = Path("uploads")

class FileServices:

    ALLOWED_TYPES = {
        "image/png",
        "image/jpeg",
        "application/pdf",
        "text/plain",
        "application/zip"
    }

    MAX_SIZE = 10*1024*1024

    @staticmethod
    def save_file(file: UploadFile):
        if file.content_type not in FileServices.ALLOWED_TYPES:
            raise ValueError("Unsupported file type.")
        
        extension = Path(file.filename).suffix
        filename = f"{uuid.uuid4()}{extension}"

        UPLOAD_DIRS.mkdir(
            exist_ok=True
        )

        file_path = UPLOAD_DIRS / filename

        with open(file_path,"wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {
            "stored_filename": filename,
            "file_path": str(file_path)
        }