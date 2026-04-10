import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form
from config import UPLOAD_DIR
from services.docx_parser import parse_docx
from services.html_builder import build_email_html
from services.supabase_service import save_message

router = APIRouter()


@router.post("/upload")
async def upload_docx(
    file: UploadFile = File(...),
    message_type: str = Form("parsha"),
):
    """Upload DOCX, parse it, generate HTML email, save to Supabase, return preview."""
    # Save uploaded file
    file_id = str(uuid.uuid4())[:8]
    filename = file.filename or "document.docx"
    save_path = os.path.join(UPLOAD_DIR, f"{file_id}_{filename}")

    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    # Parse DOCX
    parsed = parse_docx(save_path)

    # Build HTML
    html = build_email_html(parsed, message_type=message_type)

    # Suggest subject
    parsha_name = parsed.get("parsha_name", "")
    subject_suggestion = f"אור הפרשה: {parsed.get('subtitle', '')}" if parsed.get("subtitle") else ""

    # Save to Supabase
    db_row = {}
    try:
        db_row = save_message({
            "parsha_name": parsha_name or "ללא שם",
            "message_type": message_type,
            "subject": subject_suggestion,
            "html_content": html,
            "dedication": parsed.get("dedication", ""),
            "docx_filename": filename,
        })
    except Exception:
        pass

    message_id = db_row.get("id", file_id)

    return {
        "message_id": message_id,
        "html_content": html,
        "parsha_name": parsha_name,
        "subject_suggestion": subject_suggestion,
        "dedication": parsed.get("dedication", ""),
        "docx_filename": filename,
    }
