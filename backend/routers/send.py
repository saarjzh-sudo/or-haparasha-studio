from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services.smoove_service import send_campaign, get_lists
from services.supabase_service import log_send, update_message

router = APIRouter()


class TestSendRequest(BaseModel):
    subject: str
    html_content: str
    message_id: str = ""


class LiveSendRequest(BaseModel):
    subject: str
    html_content: str
    list_ids: List[int]
    message_id: str = ""


@router.post("/send/test")
async def send_test(req: TestSendRequest):
    """Send test email to טסט1 list."""
    result = send_campaign(
        subject=req.subject,
        html=req.html_content,
        list_ids=[1124084],  # טסט1
        send_now=True,
    )

    # Log to Supabase
    if req.message_id and result.get("id"):
        try:
            log_send(req.message_id, "test", [1124084], str(result["id"]))
            update_message(req.message_id, {"status": "test_sent"})
        except Exception:
            pass

    return result


@router.post("/send/live")
async def send_live(req: LiveSendRequest):
    """Send to real lists. Requires explicit list_ids."""
    if not req.list_ids:
        return {"error": "list_ids required"}

    result = send_campaign(
        subject=req.subject,
        html=req.html_content,
        list_ids=req.list_ids,
        send_now=True,
    )

    # Log to Supabase
    if req.message_id and result.get("id"):
        try:
            log_send(req.message_id, "live", req.list_ids, str(result["id"]))
            update_message(req.message_id, {"status": "sent"})
        except Exception:
            pass

    return result


@router.get("/lists")
async def list_smoove_lists():
    """Fetch available Smoove mailing lists."""
    return get_lists()
