import json
import subprocess
from typing import List
from config import SMOOVE_API_KEY

BASE_URL = "https://rest.smoove.io/v1"


def send_campaign(subject: str, html: str, list_ids: List[int], send_now: bool = True) -> dict:
    """Create and optionally send a Smoove campaign."""
    url = f"{BASE_URL}/Campaigns"
    if send_now:
        url += "?sendnow=true"

    payload = {
        "subject": subject,
        "body": html,
        "toListsById": list_ids,
        "customUnsubscribeMode": "None",
    }

    payload_json = json.dumps(payload, ensure_ascii=False)

    result = subprocess.run(
        [
            "curl", "-s", "-k",
            "-X", "POST",
            url,
            "-H", f"Authorization: Bearer {SMOOVE_API_KEY}",
            "-H", "Content-Type: application/json; charset=utf-8",
            "-d", payload_json,
        ],
        capture_output=True, text=True, timeout=30,
    )

    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": result.stdout or result.stderr, "status_code": -1}


def get_lists() -> list:
    """Fetch all Smoove mailing lists."""
    result = subprocess.run(
        [
            "curl", "-s", "-k",
            f"{BASE_URL}/Lists",
            "-H", f"Authorization: Bearer {SMOOVE_API_KEY}",
            "-H", "Content-Type: application/json; charset=utf-8",
        ],
        capture_output=True, text=True, timeout=15,
    )

    try:
        return json.loads(result.stdout)
    except Exception:
        return []
