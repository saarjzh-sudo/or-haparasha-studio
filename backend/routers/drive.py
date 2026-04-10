import os
from fastapi import APIRouter, UploadFile, File, Form
from config import UPLOAD_DIR
from services.drive_service import upload_to_drive

router = APIRouter()


@router.post("/upload-to-drive")
async def upload_file_to_drive(
    file: UploadFile = File(...),
    folder_name: str = Form("אור הפרשה"),
):
    """Upload a file to Google Drive and return the shareable link."""
    # Save file temporarily
    save_path = os.path.join(UPLOAD_DIR, file.filename or "upload.pdf")
    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    try:
        result = upload_to_drive(save_path, folder_name=folder_name)
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(save_path):
            os.remove(save_path)
