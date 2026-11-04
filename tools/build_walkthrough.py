"""Build the walkthrough from docs/walkthrough.json.

    python tools/build_walkthrough.py

Writes walkthrough.pdf at the repo root.
Requires: pip install reportlab
"""
import json
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, NextPageTemplate, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "docs" / "walkthrough.json").read_text(encoding="utf-8"))

INK, GOLD, GOLD_D, PAPER, NIGHT, MUTE = (HexColor(c) for c in
                                         ("#2e2014", "#c9a24a", "#8a6a2e", "#f4ead2", "#0b0a10", "#6a5030"))
W, H = A4

S = {
    "h1": ParagraphStyle("h1", fontName="Times-Bold", fontSize=22, leading=26, textColor=HexColor("#4a2410"), spaceAfter=2),
    "kick": ParagraphStyle("kick", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=GOLD_D, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Times-Bold", fontSize=13.5, leading=17, textColor=INK, spaceBefore=8, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Times-Roman", fontSize=11, leading=15, textColor=INK, spaceAfter=6),
    "li": ParagraphStyle("li", fontName="Times-Roman", fontSize=11, leading=14.5, textColor=INK, leftIndent=14, bulletIndent=3, spaceAfter=3),
    "td": ParagraphStyle("td", fontName="Times-Roman", fontSize=10, leading=13, textColor=INK),
    "tk": ParagraphStyle("tk", fontName="Times-Bold", fontSize=10, leading=13, textColor=HexColor("#4a2410")),
    "tip": ParagraphStyle("tip", fontName="Times-Italic", fontSize=10.5, leading=14, textColor=INK),
    "toc": ParagraphStyle("toc", fontName="Times-Roman", fontSize=12.5, leading=20, textColor=INK),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cover(c, doc):
    c.saveState()
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    cx, cy = W / 2, H * .62
    for r, col in ((120, "#3a1e0c"), (104, "#7a4214"), (92, "#e3923f"), (86, "#f6c46d")):
        c.setFillColor(HexColor(col))
        c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(HexColor("#050407"))
    c.circle(cx, cy, 82, fill=1, stroke=0)
    c.setFillColor(HexColor("#f1d48a"))
    c.setFont("Times-Bold", 50)
    c.drawCentredString(cx, H * .36, "ECLIPSE")
    c.setFont("Times-Bold", 17)
    c.drawCentredString(cx, H * .36 - 30, "THE LAST KINGDOM")
    c.setStrokeColor(GOLD)
    c.setLineWidth(.8)
    c.line(cx - 120, H * .36 - 46, cx + 120, H * .36 - 46)
    c.setFillColor(HexColor("#cbb88e"))
    c.setFont("Helvetica", 11)
    c.drawCentredString(cx, H * .36 - 66, DATA["subtitle"])
    c.restoreState()


def page(c, doc):
    c.saveState()
    c.setFillColor(PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setStrokeColor(GOLD_D)
    c.setLineWidth(1.4)
    c.rect(12 * mm, 12 * mm, W - 24 * mm, H - 24 * mm, fill=0, stroke=1)
    c.setLineWidth(.4)
    c.rect(14 * mm, 14 * mm, W - 28 * mm, H - 28 * mm, fill=0, stroke=1)
    c.setFillColor(MUTE)
    c.setFont("Helvetica", 7.5)
    c.drawString(20 * mm, 8 * mm, "ECLIPSE: THE LAST KINGDOM  ·  WALKTHROUGH")
    c.drawRightString(W - 20 * mm, 8 * mm, str(doc.page))
    c.restoreState()


def block_flow(b):
    if "p" in b:
        return [Paragraph(esc(b["p"]), S["p"])]
    if "h" in b:
        return [Paragraph(esc(b["h"]), S["h2"])]
    if "list" in b:
        return [Paragraph(esc(x), S["li"], bulletText="•") for x in b["list"]]
    if "tip" in b:
        t = Table([[Paragraph("<b>Tip.</b> " + esc(b["tip"]), S["tip"])]], colWidths=[W - 52 * mm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), HexColor("#e8d9b0")),
                               ("LINEBEFORE", (0, 0), (0, -1), 2.5, GOLD),
                               ("LEFTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 6),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        return [Spacer(1, 3), t, Spacer(1, 6)]
    if "table" in b:
        rows = [[Paragraph(esc(k), S["tk"]), Paragraph(esc(v), S["td"])] for k, v in b["table"]]
        t = Table(rows, colWidths=[48 * mm, W - 52 * mm - 48 * mm])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LINEBELOW", (0, 0), (-1, -1), .4, HexColor("#c8b080")),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                               ("ROWBACKGROUNDS", (0, 0), (-1, -1), [HexColor("#efe3c2"), PAPER])]))
        return [t, Spacer(1, 6)]
    raise ValueError(b)


def build_pdf(out):
    doc = BaseDocTemplate(str(out), pagesize=A4, title="Eclipse: The Last Kingdom — Walkthrough",
                          author="Ananth Krishna J", leftMargin=26 * mm, rightMargin=26 * mm,
                          topMargin=24 * mm, bottomMargin=22 * mm)
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate("cover", [fr], onPage=cover), PageTemplate("page", [fr], onPage=page)])
    story = [NextPageTemplate("page"), PageBreak(),
             Paragraph("Contents", S["h1"]), Spacer(1, 8)]
    for i, s in enumerate(DATA["sections"], 1):
        story.append(Paragraph(f'<font color="#8a6a2e">{i:02d}</font>&nbsp;&nbsp;{esc(s["title"])}', S["toc"]))
    for s in DATA["sections"]:
        story.append(PageBreak())
        head = [Paragraph(esc(s["title"]), S["h1"])]
        head.append(Paragraph(esc(s.get("kicker", "")).upper() or "&nbsp;", S["kick"]))
        flows = [f for b in s["blocks"] for f in block_flow(b)]
        story.append(KeepTogether(head + flows[:1]))
        story.extend(flows[1:])
    doc.build(story)


if __name__ == "__main__":
    build_pdf(ROOT / "walkthrough.pdf")
    print("Wrote walkthrough.pdf")
