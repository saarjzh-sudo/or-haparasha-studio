import zipfile
import xml.etree.ElementTree as ET
import subprocess
import json
import os


def extract_images(docx_path: str) -> dict:
    """Extract images from DOCX ZIP and upload to imgur. Returns {rId: imgur_url}."""
    result = {}

    with zipfile.ZipFile(docx_path) as z:
        # Parse relationships to find image rIds
        try:
            rels_xml = z.read("word/_rels/document.xml.rels")
        except KeyError:
            return result

        root = ET.fromstring(rels_xml)
        img_rels = {}
        for r in root:
            if "image" in r.get("Type", "").lower():
                img_rels[r.get("Id")] = r.get("Target")

        for rid, target in img_rels.items():
            img_path = f"word/{target}"
            try:
                img_bytes = z.read(img_path)
            except KeyError:
                continue

            # Save temp and upload to imgur
            ext = os.path.splitext(target)[1] or ".png"
            tmp = f"/tmp/ohp_{rid}{ext}"
            with open(tmp, "wb") as f:
                f.write(img_bytes)

            r = subprocess.run(
                [
                    "curl", "-s", "-X", "POST",
                    "https://api.imgur.com/3/image",
                    "-H", "Authorization: Client-ID 546c25a59c58ad7",
                    "-F", f"image=@{tmp}",
                    "-F", "type=file",
                ],
                capture_output=True, text=True, timeout=30,
            )

            try:
                resp = json.loads(r.stdout)
                if resp.get("success"):
                    result[rid] = resp["data"]["link"]
            except Exception:
                pass

            os.remove(tmp)

    return result
