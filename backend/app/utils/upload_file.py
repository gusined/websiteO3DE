import os
import uuid
from fastapi import UploadFile, HTTPException
from app.config import settings

class FileUploadService:
    def init(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_file(self, file: UploadFile) -> dict:
        file_extension = file.filename.split('.')[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "filename": filename,
            "file_path": file_path,
            "file_size": len(content),
            "mime_type": file.content_type
        }
    
    def delete_file(self, file_path: str):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

file_upload_service = FileUploadService()