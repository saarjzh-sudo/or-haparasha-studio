"""Supabase service — CRUD for ohp_messages, ohp_chat_messages, ohp_send_logs."""

from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_message(data: dict) -> dict:
    """Insert or update an ohp_messages row."""
    result = supabase.table("ohp_messages").insert(data).execute()
    return result.data[0] if result.data else {}


def update_message(message_id: str, data: dict) -> dict:
    """Update an existing message."""
    result = supabase.table("ohp_messages").update(data).eq("id", message_id).execute()
    return result.data[0] if result.data else {}


def get_message(message_id: str) -> dict:
    """Get a single message by ID."""
    result = supabase.table("ohp_messages").select("*").eq("id", message_id).single().execute()
    return result.data or {}


def list_messages(limit: int = 50) -> list:
    """List all messages, newest first."""
    result = (
        supabase.table("ohp_messages")
        .select("id, parsha_name, message_type, subject, status, created_at, docx_filename")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


def save_chat_message(message_id: str, role: str, content: str) -> dict:
    """Save a chat message."""
    result = supabase.table("ohp_chat_messages").insert({
        "message_id": message_id,
        "role": role,
        "content": content,
    }).execute()
    return result.data[0] if result.data else {}


def get_chat_history(message_id: str) -> list:
    """Get chat history for a message."""
    result = (
        supabase.table("ohp_chat_messages")
        .select("*")
        .eq("message_id", message_id)
        .order("created_at")
        .execute()
    )
    return result.data or []


def log_send(message_id: str, send_type: str, list_ids: list, campaign_id: str = "") -> dict:
    """Log a send event."""
    result = supabase.table("ohp_send_logs").insert({
        "message_id": message_id,
        "send_type": send_type,
        "list_ids": list_ids,
        "campaign_id": campaign_id,
    }).execute()
    return result.data[0] if result.data else {}
