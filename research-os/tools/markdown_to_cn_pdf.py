"""Minimal Markdown-to-PDF converter for local Chinese research translations."""
from pathlib import Path
import re, sys
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
from xml.sax.saxutils import escape

FONT = r"C:\\Windows\\Fonts\\simhei.ttf"
pdfmetrics.registerFont(TTFont("CN", FONT))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CNBody", parent=styles["BodyText"], fontName="CN", fontSize=9.2, leading=13.5, spaceAfter=4, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CNTitle", parent=styles["Title"], fontName="CN", fontSize=17, leading=23, alignment=TA_CENTER, spaceAfter=10, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CNH1", parent=styles["Heading1"], fontName="CN", fontSize=14, leading=19, spaceBefore=9, spaceAfter=5, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CNH2", parent=styles["Heading2"], fontName="CN", fontSize=11.5, leading=16, spaceBefore=7, spaceAfter=4, wordWrap="CJK"))
styles.add(ParagraphStyle(name="CNMeta", parent=styles["BodyText"], fontName="CN", fontSize=8.5, leading=12, textColor=colors.HexColor("#333333"), wordWrap="CJK"))
styles.add(ParagraphStyle(name="CNQuote", parent=styles["BodyText"], fontName="CN", fontSize=8.8, leading=13, leftIndent=10, borderColor=colors.grey, borderWidth=0.5, borderPadding=5, wordWrap="CJK"))


def inline(text):
    # Escape Markdown as plain text for robust Chinese PDF generation. This
    # intentionally avoids nested ReportLab markup when bold/code spans overlap.
    return escape(text)


def convert(src, dst):
    lines = Path(src).read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            story.append(Spacer(1, 3)); i += 1; continue
        if line.startswith("# "):
            story.append(Paragraph(inline(line[2:]), styles["CNTitle"])); i += 1; continue
        if line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), styles["CNH1"])); i += 1; continue
        if line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), styles["CNH2"])); i += 1; continue
        if line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), styles["CNQuote"])); i += 1; continue
        if line.startswith("```"):
            block=[]; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                block.append(lines[i]); i += 1
            i += 1
            story.append(Preformatted("\n".join(block), styles["Code"])); continue
        if line.startswith("| ") or line.startswith("|"):
            rows=[]
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                raw=lines[i].strip().strip("|")
                cells=[c.strip() for c in raw.split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append([Paragraph(inline(c), styles["CNMeta"]) for c in cells])
                i += 1
            if rows:
                n=max(len(r) for r in rows); rows=[r+[""]*(n-len(r)) for r in rows]
                t=Table(rows, repeatRows=1, colWidths=[(180/n)*mm]*n)
                t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.25,colors.grey),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e8eef7")),("VALIGN",(0,0),(-1,-1),"TOP"),("FONTNAME",(0,0),(-1,-1),"CN"),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3)]))
                story.append(t); story.append(Spacer(1,5))
            continue
        if re.match(r"^[-*] ", line):
            story.append(Paragraph("• " + inline(line[2:]), styles["CNBody"])); i += 1; continue
        story.append(Paragraph(inline(line), styles["CNBody"])); i += 1
    doc=SimpleDocTemplate(str(dst), pagesize=A4, rightMargin=16*mm, leftMargin=16*mm, topMargin=15*mm, bottomMargin=15*mm, title=Path(src).stem)
    doc.build(story)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: markdown_to_cn_pdf.py input.md output.pdf")
    convert(sys.argv[1], sys.argv[2])
