import subprocess
import os
import asyncio
from config import CLAUDE_BINARY, SYSTEM_DIR


async def ask_claude(prompt: str) -> str:
    """Run Claude Code binary as subprocess and return response."""
    if not CLAUDE_BINARY:
        return "שגיאה: לא נמצא Claude Code binary"

    env = {k: v for k, v in os.environ.items()}
    env.pop("CLAUDE_CODE", None)

    def _run():
        result = subprocess.run(
            [CLAUDE_BINARY, "-p", prompt, "--output-format", "text",
             "--allowedTools", "Read,Write,Edit"],
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
            cwd=SYSTEM_DIR,
        )
        if result.returncode != 0:
            return f"שגיאה מקלוד: {result.stderr[:500]}"
        return result.stdout.strip()

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _run)
