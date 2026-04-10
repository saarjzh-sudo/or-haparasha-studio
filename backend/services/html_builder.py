"""HTML Email Builder — generates premium styled email HTML for אור הפרשה.

Table-based layout for Gmail compatibility. Suez One + Heebo fonts.
Gold dividers, cream-gold hero, dark navy footer.
RTL with inline direction + text-align on every element (Gmail strips dir from html).
"""

from html import escape
from config import LOGO_STANDING, LEGACY_LINK
from services.image_service import extract_images


# -- Style constants --
FONT_HEADING = "'Suez One',David,serif"
FONT_BODY = "'Heebo',Arial,sans-serif"
COLOR_GOLD = "#8b6914"
COLOR_NAVY = "#1a2c5a"
COLOR_TEXT = "#333333"
GOLD_GRADIENT = "linear-gradient(to left,#8b6914,#e8c862,#f5e199,#e8c862,#8b6914)"
HERO_GRADIENT = "linear-gradient(135deg,#fef9ef 0%,#fef0c0 100%)"
FOOTER_GRADIENT = "linear-gradient(160deg,#0f1c3f,#1a2c5a)"


def _render_content_blocks(blocks: list, font_size: int, image_urls: dict) -> str:
    """Render a list of content blocks to HTML."""
    parts = []
    for block in blocks:
        btype = block["type"]

        if btype == "heading":
            parts.append(
                f'<h3 style="font-family:{FONT_HEADING};font-size:{font_size + 4}px;'
                f'color:{COLOR_GOLD};margin:28px 0 12px;direction:rtl;text-align:right;">'
                f'{block["html"]}</h3>'
            )

        elif btype == "paragraph":
            parts.append(
                f'<p style="font-family:{FONT_BODY};font-size:{font_size}px;'
                f'color:{COLOR_TEXT};line-height:1.9;margin:0 0 14px;'
                f'direction:rtl;text-align:justify;">{block["html"]}</p>'
            )

        elif btype == "textbox":
            text = escape(block["text"])
            parts.append(
                f'<div style="background:#fff;border:2px solid #e8c862;border-radius:10px;'
                f'padding:16px 20px;margin:20px 0;direction:rtl;text-align:right;">'
                f'<p style="font-family:{FONT_HEADING};font-size:15px;color:{COLOR_GOLD};'
                f'margin:0 0 8px;direction:rtl;text-align:right;"><strong>תשובות:</strong></p>'
                f'<p style="font-family:{FONT_BODY};font-size:13px;color:#555;'
                f'line-height:1.8;margin:0;direction:rtl;text-align:right;">{text}</p>'
                f'</div>'
            )

        elif btype == "image":
            rid = block.get("rId", "")
            url = image_urls.get(rid, "")
            if url:
                parts.append(
                    f'<p style="text-align:center;margin:20px 0;">'
                    f'<img src="{url}" style="max-width:100%;height:auto;border-radius:8px;" alt="">'
                    f'</p>'
                )

        elif btype == "table":
            parts.append(_render_word_search_table(block["data"]))

    return '\n'.join(parts)


def _render_word_search_table(data: list) -> str:
    """Render a word-search table with gold styling."""
    header_style = (
        f"width:30px;height:30px;text-align:center;vertical-align:middle;"
        f"font-family:{FONT_BODY};font-size:11px;color:{COLOR_GOLD};"
        f"font-weight:bold;background:#fef9ef;border:1px solid #e8c862;"
    )
    cell_style = (
        f"width:30px;height:30px;text-align:center;vertical-align:middle;"
        f"font-family:{FONT_HEADING};font-size:15px;color:{COLOR_NAVY};"
        f"background:#ffffff;border:1px solid #e8c862;"
    )

    rows_html = []
    for i, row in enumerate(data):
        cells = []
        for j, cell in enumerate(row):
            style = header_style if i == 0 or j == 0 else cell_style
            cells.append(f'<td style="{style}">{escape(cell)}</td>')
        rows_html.append(f'<tr>{"".join(cells)}</tr>')

    return (
        f'<table dir="rtl" style="border-collapse:collapse;margin:20px auto;direction:rtl;" '
        f'cellpadding="0" cellspacing="0">\n'
        + '\n'.join(rows_html)
        + '\n</table>'
    )


def build_email_html(
    parsed: dict,
    message_type: str = "parsha",
    pdf_url: str = "",
    moreshet_url: str = "",
) -> str:
    """Build complete email HTML from parsed DOCX data.

    Args:
        parsed: Output from parse_docx()
        message_type: 'parsha' or 'motza_sh'
        pdf_url: URL for PDF download button
        moreshet_url: URL for Moreshet booklet button
    """
    # Upload images to imgur
    image_urls = {}
    if parsed.get("docx_path"):
        try:
            image_urls = extract_images(parsed["docx_path"])
        except Exception:
            pass

    parsha_name = escape(parsed.get("parsha_name", ""))
    subtitle = escape(parsed.get("subtitle", ""))
    dedication = escape(parsed.get("dedication", ""))

    # Children content = 16px, Teacher content = 14px
    children_html = _render_content_blocks(
        parsed.get("children_content", []), font_size=16, image_urls=image_urls
    )
    teacher_html = _render_content_blocks(
        parsed.get("teacher_content", []), font_size=14, image_urls=image_urls
    )

    # Buttons
    pdf_button = ""
    if pdf_url:
        pdf_button = f'''
<tr>
<td style="background:#ffffff;padding:8px 40px 10px;text-align:center;">
  <a href="{escape(pdf_url)}" class="btn-link" style="display:inline-block;padding:14px 36px;background:{HERO_GRADIENT};color:{COLOR_NAVY};font-family:{FONT_BODY};font-size:16px;font-weight:600;text-decoration:none;border-radius:8px;direction:rtl;">⬇ מצורף קובץ מעוצב להדפסה – לחצו כאן</a>
</td>
</tr>'''

    moreshet_button = ""
    if moreshet_url:
        moreshet_button = f'''
<tr>
<td style="background:#ffffff;padding:6px 40px 24px;text-align:center;">
  <a href="{escape(moreshet_url)}" class="btn-link" style="display:inline-block;padding:14px 36px;background:linear-gradient(135deg,{COLOR_NAVY},#2a3c6a);color:#ffffff;font-family:{FONT_BODY};font-size:16px;font-weight:600;text-decoration:none;border-radius:8px;direction:rtl;">📚 חוברת מורשה – לחצו כאן</a>
</td>
</tr>'''

    # Teacher section row (if exists)
    teacher_section = ""
    if teacher_html:
        teacher_section = f'''
<!-- GOLD DIVIDER -->
<tr><td style="background:{GOLD_GRADIENT};height:5px;font-size:0;line-height:0;" class="gold-divider">&nbsp;</td></tr>

<!-- TEACHER CONTENT -->
<tr>
<td class="teacher-cell" style="background:#fdf6ec;padding:28px 40px 32px;direction:rtl;text-align:right;">
{teacher_html}
</td>
</tr>'''

    html = f'''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Suez+One&family=Heebo:wght@300;400;500;600&display=swap');
@media only screen and (max-width: 600px) {{
  .outer-table {{ padding: 8px 4px !important; }}
  .inner-table {{ border-radius: 8px !important; }}
  .hero-cell {{ padding: 24px 18px 20px !important; }}
  .hero-logo {{ max-width: 180px !important; }}
  .hero-title {{ font-size: 22px !important; }}
  .hero-subtitle {{ font-size: 16px !important; }}
  .hero-quote {{ font-size: 15px !important; }}
  .body-cell {{ padding: 22px 18px 24px !important; }}
  .body-cell p {{ font-size: 15px !important; line-height: 1.85 !important; }}
  .body-cell h3 {{ font-size: 17px !important; }}
  .teacher-cell {{ padding: 20px 18px !important; }}
  .teacher-cell p {{ font-size: 13px !important; }}
  .teacher-cell h3 {{ font-size: 15px !important; }}
  .btn-link {{ font-size: 14px !important; padding: 14px 20px !important; display: block !important; }}
  .footer-cell {{ padding: 20px 18px !important; }}
  td {{ word-break: break-word; }}
  .gold-divider {{ height: 3px !important; }}
}}
</style>
</head>
<body style="margin:0;padding:0;background:#f0ece3;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f0ece3;padding:24px 10px;" class="outer-table">
<tr><td align="center">
<table width="650" cellpadding="0" cellspacing="0" style="max-width:650px;width:100%;border-radius:12px;overflow:hidden;box-shadow:0 6px 28px rgba(0,0,0,0.13);background:#ffffff;" class="inner-table">

<!-- HERO -->
<tr>
<td class="hero-cell" style="background:{HERO_GRADIENT};padding:36px 40px 28px;text-align:center;direction:rtl;">
  <img src="{LOGO_STANDING}" alt="בית מדרש למלמדים" style="max-width:220px;height:auto;margin-bottom:18px;" class="hero-logo">
  <h1 class="hero-title" style="font-family:{FONT_HEADING};font-size:26px;color:{COLOR_GOLD};margin:0 0 6px;direction:rtl;text-align:center;">{parsha_name}</h1>
  <h2 class="hero-subtitle" style="font-family:{FONT_HEADING};font-size:20px;color:{COLOR_NAVY};margin:0 0 8px;font-weight:600;direction:rtl;text-align:center;">{subtitle}</h2>
  {"" if not dedication else f'<p style="font-family:{FONT_BODY};font-size:11px;color:#8b7a55;margin:0;line-height:1.6;direction:rtl;text-align:center;">{dedication}</p>'}
</td>
</tr>

<!-- GOLD DIVIDER -->
<tr><td style="background:{GOLD_GRADIENT};height:5px;font-size:0;line-height:0;" class="gold-divider">&nbsp;</td></tr>

<!-- BODY - CHILDREN'S CONTENT -->
<tr>
<td class="body-cell" style="background:#ffffff;padding:32px 40px 36px;direction:rtl;text-align:right;">
{children_html}
</td>
</tr>

{teacher_section}

<!-- GOLD DIVIDER -->
<tr><td style="background:{GOLD_GRADIENT};height:5px;font-size:0;line-height:0;" class="gold-divider">&nbsp;</td></tr>

<!-- SIGNATURE -->
<tr>
<td style="background:#ffffff;padding:24px 40px 8px;text-align:center;direction:rtl;">
  <p style="font-family:{FONT_HEADING};font-size:18px;color:{COLOR_NAVY};margin:0;direction:rtl;text-align:center;">בְּאַהֲבָה וֶאֱמוּנָה,<br>יְהוּדָה וְצוֶוֶת בֵּית הַמִּדְרָשׁ לַמְּלַמְּדִים</p>
</td>
</tr>

<!-- NB -->
<tr>
<td style="background:#ffffff;padding:12px 40px 20px;direction:rtl;text-align:right;">
  <p style="font-family:{FONT_BODY};font-size:13px;color:#666;line-height:1.7;margin:0;direction:rtl;text-align:right;">
    <strong>נ.ב.</strong><br>
    ניתן כעת להקדיש שיעור, יום לימוד, דף פרשת שבוע או חוברת שממשיכים להאיר נשמות של ילדים, הורים ומורים בכל הארץ.<br>
    לפרטי הנצחה ושותפות לחצו כאן &gt;&gt; <a href="{LEGACY_LINK}" style="color:{COLOR_GOLD};font-weight:600;">{LEGACY_LINK}</a>
  </p>
</td>
</tr>

{pdf_button}
{moreshet_button}

<!-- FOOTER -->
<tr>
<td class="footer-cell" style="background:{FOOTER_GRADIENT};padding:28px 40px;text-align:center;direction:rtl;">
  <img src="{LOGO_STANDING}" alt="בית מדרש למלמדים" style="max-width:160px;height:auto;margin-bottom:12px;">
  <p style="font-family:{FONT_HEADING};font-size:16px;color:#e8c862;margin:0;direction:rtl;text-align:center;">בּוֹנִים עָתִיד לָאֻמָּה</p>
</td>
</tr>

</table>
</td></tr>
</table>
</body>
</html>'''

    return html
