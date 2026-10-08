# 11_CONTENT_FACTORY/artifact_generators/pdf_generator.py — 产品说明 PDF 生成

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_pdf(title: str, sections: list[dict], output_path: Path) -> dict[str, Any]:
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import cm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    except ImportError as exc:
        return {"status": "error", "file_path": "", "error": f"reportlab not installed: {exc}"}

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        font_name = "STSong-Light"
    except Exception:
        font_name = "Helvetica"

    doc = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("CustomTitle", parent=styles["Heading1"], fontName=font_name, fontSize=18, spaceAfter=12)
    heading_style = ParagraphStyle("CustomHeading", parent=styles["Heading2"], fontName=font_name, fontSize=14, spaceAfter=8)
    body_style = ParagraphStyle("CustomBody", parent=styles["Normal"], fontName=font_name, fontSize=11, spaceAfter=6)

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.3 * cm))

    for sec in sections:
        story.append(Paragraph(sec.get("title", ""), heading_style))
        for line in sec.get("lines", []):
            story.append(Paragraph(line.replace("\n", "<br/>"), body_style))
        story.append(Spacer(1, 0.2 * cm))

    doc.build(story)
    return {"status": "ok", "file_path": str(output_path)}
