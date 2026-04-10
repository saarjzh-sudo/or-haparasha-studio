import os
from fastapi import APIRouter
from pydantic import BaseModel
from services.claude_service import ask_claude
from services.supabase_service import save_chat_message, update_message

router = APIRouter()


class ChatRequest(BaseModel):
    message_id: str
    user_message: str
    current_html: str


@router.post("/chat")
async def chat_with_claude(req: ChatRequest):
    """Send correction request to Claude, get updated HTML."""
    # Write current HTML to temp file for Claude to edit
    tmp_path = f"/tmp/ohp_{req.message_id}.html"
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(req.current_html)

    prompt = f"""אתה עורך מיילים של בית מדרש למלמדים.
הנה קובץ HTML של מייל נוכחי: {tmp_path}

המשתמש מבקש את התיקון הבא:
{req.user_message}

כללים:
- תקן רק את מה שהתבקש. לא יותר.
- אסור לשנות מילות תוכן שלא התבקשו
- אסור לשפר ניסוחים "בדרך"
- אסור לשנות מבנה HTML שעובד
- קרא את הקובץ, ערוך אותו עם Edit, וסיים.
- ענה בקצרה מה שינית.
"""

    response = await ask_claude(prompt)

    # Read back the potentially modified HTML
    updated_html = req.current_html
    if os.path.exists(tmp_path):
        with open(tmp_path, "r", encoding="utf-8") as f:
            updated_html = f.read()
        os.remove(tmp_path)

    # Save chat messages and updated HTML to Supabase
    try:
        save_chat_message(req.message_id, "user", req.user_message)
        save_chat_message(req.message_id, "assistant", response)
        update_message(req.message_id, {"html_content": updated_html})
    except Exception:
        pass

    return {
        "assistant_message": response,
        "updated_html": updated_html,
    }
