import json
import os
import subprocess
from typing import List
from config import SMOOVE_API_KEY

BASE_URL = "https://rest.smoove.io/v1"
HEADERS = {
    "Authorization": f"Bearer {SMOOVE_API_KEY}",
    "Content-Type": "application/json; charset=utf-8",
}

IS_VERCEL = bool(os.environ.get("VERCEL"))


def _post_requests(url: str, payload: dict) -> dict:
    """Use requests library (works on Vercel with Python 3.12)."""
    import requests
    import urllib3
    urllib3.disable_warnings()
    resp = requests.post(
        url, headers=HEADERS,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        verify=False, timeout=30,
    )
    try:
        return resp.json()
    except Exception:
        return {"error": resp.text, "status_code": resp.status_code}


def _post_curl(url: str, payload: dict) -> dict:
    """Use curl subprocess (for local Python 3.14 SSL workaround)."""
    payload_json = json.dumps(payload, ensure_ascii=False)
    result = subprocess.run(
        ["curl", "-s", "-k", "-X", "POST", url,
         "-H", f"Authorization: Bearer {SMOOVE_API_KEY}",
         "-H", "Content-Type: application/json; charset=utf-8",
         "-d", payload_json],
        capture_output=True, text=True, timeout=30,
    )
    try:
        return json.loads(result.stdout)
    except Exception:
        return {"error": result.stdout or result.stderr, "status_code": -1}


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

    if IS_VERCEL:
        return _post_requests(url, payload)
    return _post_curl(url, payload)


def get_lists() -> list:
    """Fetch all Smoove mailing lists."""
    if IS_VERCEL:
        import requests
        import urllib3
        urllib3.disable_warnings()
        resp = requests.get(f"{BASE_URL}/Lists", headers=HEADERS, verify=False, timeout=15)
        try:
            return resp.json()
        except Exception:
            return []
    else:
        result = subprocess.run(
            ["curl", "-s", "-k", f"{BASE_URL}/Lists",
             "-H", f"Authorization: Bearer {SMOOVE_API_KEY}",
             "-H", "Content-Type: application/json; charset=utf-8"],
            capture_output=True, text=True, timeout=15,
        )
        try:
            return json.loads(result.stdout)
        except Exception:
            return []
