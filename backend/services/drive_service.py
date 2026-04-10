import json
import subprocess
import os
from config import CLAUDE_BINARY, SYSTEM_DIR


def upload_to_drive(file_path: str, folder_name: str = "אור הפרשה") -> dict:
    """Upload a file to Google Drive using Claude CLI with MCP tools.

    Uses the Claude binary with the Google Suite MCP plugin to upload
    the file and return a shareable link.
    """
    if not CLAUDE_BINARY:
        return {"error": "Claude binary not found"}

    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    filename = os.path.basename(file_path)

    prompt = f"""Upload the file at '{file_path}' to Google Drive in the folder '/{folder_name}'.
The file name should be '{filename}'.
After uploading, return ONLY a JSON object with these fields:
- "id": the Google Drive file ID
- "link": the shareable view link (https://drive.google.com/file/d/ID/view?usp=sharing)
- "name": the file name
Return ONLY the JSON, nothing else."""

    try:
        result = subprocess.run(
            [
                CLAUDE_BINARY,
                "-p", prompt,
                "--output-format", "text",
                "--allowedTools",
                "mcp__plugin_google-suite_gdrive__uploadFile,mcp__plugin_google-suite_gdrive__shareFile",
            ],
            capture_output=True, text=True, timeout=60,
            cwd=SYSTEM_DIR,
        )

        output = result.stdout.strip()

        # Try to parse JSON from the output
        try:
            # Find JSON in the output
            start = output.find("{")
            end = output.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(output[start:end])
                return data
        except json.JSONDecodeError:
            pass

        return {"output": output, "link": ""}

    except subprocess.TimeoutExpired:
        return {"error": "Upload timed out"}
    except Exception as e:
        return {"error": str(e)}
