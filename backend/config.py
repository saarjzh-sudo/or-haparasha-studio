import os
import glob

def find_claude_binary():
    """Auto-detect the latest Claude Code binary."""
    pattern = "/Users/saarj/Library/Application Support/Claude/claude-code/*/claude.app/Contents/MacOS/claude"
    matches = sorted(glob.glob(pattern))
    return matches[-1] if matches else None

CLAUDE_BINARY = os.environ.get("CLAUDE_BINARY") or find_claude_binary()
SYSTEM_DIR = "/Users/saarj/Downloads/saar-workspace/the-system-v8"

SMOOVE_API_KEY = os.environ.get("SMOOVE_API_KEY", "4c57342a-f3ad-42a0-aa4e-728c3b4947f2")
SMOOVE_TEST_LIST = 1124084

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://pzvmwfexeiruelwiujxn.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB6dm13ZmV4ZWlydWVsd2l1anhuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU1NTM1NzUsImV4cCI6MjA5MTEyOTU3NX0.U5agLkf6jfLUg7UjfdnTJfavUsx-dyzxs2fxJgWAp8o")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Logo URLs
LOGO_STANDING = "https://i.imgur.com/YQo8ubd.png"
LOGO_HORIZONTAL = "https://i.imgur.com/txtmtqa.png"
LEGACY_LINK = "https://beit-midrash-legacy.lovable.app"
