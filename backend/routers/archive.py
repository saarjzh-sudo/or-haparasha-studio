from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.supabase_service import (
    list_messages, get_message, update_message, get_chat_history,
)

router = APIRouter()


class UpdateMessageRequest(BaseModel):
    subject: Optional[str] = None
    status: Optional[str] = None
    pdf_url: Optional[str] = None
    moreshet_url: Optional[str] = None
    html_content: Optional[str] = None


@router.get("/messages")
async def get_messages():
    """List all messages, newest first."""
    return list_messages()


@router.get("/messages/{message_id}")
async def get_single_message(message_id: str):
    """Get a single message with full HTML."""
    return get_message(message_id)


@router.put("/messages/{message_id}")
async def update_single_message(message_id: str, req: UpdateMessageRequest):
    """Update message fields."""
    data = {k: v for k, v in req.model_dump().items() if v is not None}
    if not data:
        return {"error": "no fields to update"}
    return update_message(message_id, data)


@router.get("/messages/{message_id}/chat")
async def get_message_chat(message_id: str):
    """Get chat history for a message."""
    return get_chat_history(message_id)
