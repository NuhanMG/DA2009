"""
The PDF builder used by build_guides.py.

Turns a simple list of blocks - headings, paragraphs, bullets, tables, code
and question/answer pairs - into a printable A4 document with a contents
page and page numbers.

Helper file, not part of the scraping project itself.
"""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

#--- Colours: printer friendly, dark ink on white ------------------------#
INK = colors.HexColor("#14181f")
BODY = colors.HexColor("#24292f")
SOFT = colors.HexColor("#57606a")
ACCENT = colors.HexColor("#0b5f75")
RULE = colors.HexColor("#d0d7de")
PANEL = colors.HexColor("#f4f6f8")
CODEBG = colors.HexColor("#eef1f5")
QBG = colors.HexColor("#eaf3f6")

PAGE_W, PAGE_H = A4
MARGIN = 2.0 * cm


#=========================================================================#
#  STYLES                                                                 #
#=========================================================================#

def build_styles():
    base = getSampleStyleSheet()

    s = {}

    s["title"] = ParagraphStyle(
        "title", parent=base["Title"], fontName="Helvetica-Bold",
        fontSize=26, leading=31, textColor=INK, alignment=TA_LEFT,
        spaceAfter=6)

    s["subtitle"] = ParagraphStyle(
        "subtitle", fontName="Helvetica", fontSize=13, leading=18,
        textColor=SOFT, alignment=TA_LEFT, spaceAfter=4)

    s["cover_small"] = ParagraphStyle(
        "cover_small", fontName="Helvetica", fontSize=10.5, leading=15,
        textColor=SOFT, alignment=TA_LEFT)

    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=18, leading=23,
        textColor=INK, spaceBefore=18, spaceAfter=8)

    # Same look as h1, but a different style name so afterFlowable
    # ignores it and the contents page does not list itself.
    s["h1_plain"] = ParagraphStyle(
        "h1_plain", fontName="Helvetica-Bold", fontSize=18, leading=23,
        textColor=INK, spaceBefore=18, spaceAfter=8)

    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13.5, leading=18,
        textColor=ACCENT, spaceBefore=14, spaceAfter=6)

    s["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
        textColor=INK, spaceBefore=10, spaceAfter=4)

    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10, leading=15,
        textColor=BODY, spaceAfter=7)

    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], leftIndent=14, bulletIndent=4,
        spaceAfter=3)

    s["code"] = ParagraphStyle(
        "code", fontName="Courier", fontSize=8.4, leading=11.6,
        textColor=INK, backColor=CODEBG, borderPadding=7,
        leftIndent=2, rightIndent=2, spaceBefore=11, spaceAfter=13)

    s["note"] = ParagraphStyle(
        "note", parent=s["body"], backColor=PANEL, borderPadding=8,
        leftIndent=2, rightIndent=2, spaceBefore=16, spaceAfter=18)

    s["question"] = ParagraphStyle(
        "question", fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=INK, spaceBefore=9, spaceAfter=3)

    s["answer"] = ParagraphStyle(
        "answer", fontName="Helvetica", fontSize=9.8, leading=14,
        textColor=BODY, leftIndent=12, spaceAfter=4)

    s["level"] = ParagraphStyle(
        "level", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        textColor=ACCENT, spaceBefore=12, spaceAfter=2)

    s["cell"] = ParagraphStyle(
        "cell", fontName="Helvetica", fontSize=8.8, leading=12,
        textColor=BODY)

    s["cell_head"] = ParagraphStyle(
        "cell_head", fontName="Helvetica-Bold", fontSize=8.8, leading=12,
        textColor=INK)

    s["toc1"] = ParagraphStyle(
        "toc1", fontName="Helvetica-Bold", fontSize=10.5, leading=15,
        textColor=INK, spaceBefore=4)

    s["toc2"] = ParagraphStyle(
        "toc2", fontName="Helvetica", fontSize=9, leading=12.5,
        textColor=BODY, leftIndent=16)

    return s


STYLES = build_styles()


#=========================================================================#
#  PAGE FURNITURE                                                         #
#=========================================================================#

class Guide(BaseDocTemplate):
    """A document that remembers its own headings for the contents page."""

    def __init__(self, filename, footer_text, toc_depth=2, **kw):
        super().__init__(filename, pagesize=A4,
                         leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=1.7 * cm, **kw)
        self.footer_text = footer_text
        # 1 = list chapters only; 2 = chapters and their sections.
        self.toc_depth = toc_depth

        frame = Frame(self.leftMargin, self.bottomMargin,
                      self.width, self.height, id="body")

        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame],
                         onPage=self._blank),
            PageTemplate(id="normal", frames=[frame],
                         onPage=self._decorate),
        ])

    def _blank(self, canvas, doc):
        pass

    def _decorate(self, canvas, doc):
        canvas.saveState()

        # A thin line and the footer text along the bottom.
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 1.35 * cm, PAGE_W - MARGIN, 1.35 * cm)

        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(SOFT)
        canvas.drawString(MARGIN, 1.0 * cm, self.footer_text)
        canvas.drawRightString(PAGE_W - MARGIN, 1.0 * cm,
                               str(canvas.getPageNumber()))

        canvas.restoreState()

    def afterFlowable(self, flowable):
        """Record headings so the contents page can list them."""
        if not isinstance(flowable, Paragraph):
            return

        name = flowable.style.name
        if name == "h1":
            self.notify("TOCEntry", (0, flowable.getPlainText(), self.page))
        elif name == "h2" and self.toc_depth >= 2:
            self.notify("TOCEntry", (1, flowable.getPlainText(), self.page))


#=========================================================================#
#  BLOCK BUILDERS                                                         #
#=========================================================================#

def escape(text):
    """Make text safe for reportlab, which reads a few XML style tags."""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def markup(text):
    """
    Allow a couple of simple marks in the source text:
        **bold**      ->  bold
        `code`        ->  monospace
    Everything else is escaped so stray < or & cannot break the build.
    """
    text = escape(text)

    out = []
    for i, chunk in enumerate(text.split("**")):
        out.append(f"<b>{chunk}</b>" if i % 2 else chunk)
    text = "".join(out)

    out = []
    for i, chunk in enumerate(text.split("`")):
        if i % 2:
            out.append(f'<font face="Courier" size="9">{chunk}</font>')
        else:
            out.append(chunk)
    return "".join(out)


def h1(text):
    return [Paragraph(escape(text), STYLES["h1"])]


def h2(text):
    return [Paragraph(escape(text), STYLES["h2"])]


def h3(text):
    return [Paragraph(escape(text), STYLES["h3"])]


def p(text):
    return [Paragraph(markup(text), STYLES["body"])]


def note(text):
    return [Paragraph(markup(text), STYLES["note"])]


def bullets(items):
    return [Paragraph(markup(i), STYLES["bullet"], bulletText="•")
            for i in items]


def numbered(items):
    return [Paragraph(markup(t), STYLES["bullet"], bulletText=f"{n}.")
            for n, t in enumerate(items, start=1)]


def code(text):
    """A code block. Spaces are preserved so indentation survives."""
    lines = escape(text.strip("\n")).split("\n")
    body = "<br/>".join(line.replace(" ", "&nbsp;") for line in lines)
    return [Paragraph(body, STYLES["code"])]


def table(rows, widths=None, head=True):
    """A simple table. rows[0] is the heading row."""
    data = []
    for r, row in enumerate(rows):
        style = STYLES["cell_head"] if (head and r == 0) else STYLES["cell"]
        data.append([Paragraph(markup(c), style) for c in row])

    total = PAGE_W - 2 * MARGIN
    if widths is None:
        widths = [total / len(rows[0])] * len(rows[0])
    else:
        scale = total / sum(widths)
        widths = [w * scale for w in widths]

    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PANEL if head else colors.white),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [t, Spacer(1, 9)]


def qa(number, question, answer, code_block=None):
    """
    One question and its answer, kept on the same page where possible.
    """
    parts = [Paragraph(f"{number}. {markup(question)}", STYLES["question"])]
    for chunk in answer.strip().split("\n\n"):
        parts.append(Paragraph(markup(chunk), STYLES["answer"]))
    if code_block:
        parts += code(code_block)
    return [KeepTogether(parts)]


def level(text):
    return [Paragraph(escape(text.upper()), STYLES["level"])]


def gap(height=8):
    return [Spacer(1, height)]


def page_break():
    return [PageBreak()]


#=========================================================================#
#  COVER AND CONTENTS                                                     #
#=========================================================================#

def cover(title, subtitle, lines):
    parts = [Spacer(1, 5.5 * cm)]

    bar = Table([[""]], colWidths=[3.2 * cm], rowHeights=[3])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), ACCENT)]))
    parts += [bar, Spacer(1, 14)]

    parts.append(Paragraph(escape(title), STYLES["title"]))
    parts.append(Paragraph(escape(subtitle), STYLES["subtitle"]))
    parts.append(Spacer(1, 26))

    for line in lines:
        # An empty string in the list means "leave a gap here". An empty
        # paragraph would collapse to nothing, so we add a Spacer instead.
        if not line.strip():
            parts.append(Spacer(1, 10))
        else:
            parts.append(Paragraph(markup(line), STYLES["cover_small"]))

    parts.append(NextPageTemplate("normal"))
    parts.append(PageBreak())
    return parts


def contents():
    toc = TableOfContents()
    toc.levelStyles = [STYLES["toc1"], STYLES["toc2"]]
    return [Paragraph("Contents", STYLES["h1_plain"]), Spacer(1, 6), toc,
            PageBreak()]


#=========================================================================#
#  EXTRA BLOCKS FOR THE MEMBER DOCUMENTS                                  #
#=========================================================================#

IDEA_BG = colors.HexColor("#fff5d6")      # soft yellow - comparisons
KEY_BG = colors.HexColor("#e3f3e6")       # soft green  - things to remember
TRY_BG = colors.HexColor("#e6effa")       # soft blue   - try it yourself
WARN_BG = colors.HexColor("#fdeaea")      # soft red    - be careful

STYLES["idea"] = ParagraphStyle(
    "idea", parent=STYLES["body"], backColor=IDEA_BG, borderPadding=9,
    leftIndent=3, rightIndent=3, spaceBefore=20, spaceAfter=22)

STYLES["remember"] = ParagraphStyle(
    "remember", parent=STYLES["body"], backColor=KEY_BG, borderPadding=9,
    leftIndent=3, rightIndent=3, spaceBefore=20, spaceAfter=22)

STYLES["tryit"] = ParagraphStyle(
    "tryit", parent=STYLES["body"], backColor=TRY_BG, borderPadding=9,
    leftIndent=3, rightIndent=3, spaceBefore=20, spaceAfter=4)

STYLES["careful"] = ParagraphStyle(
    "careful", parent=STYLES["body"], backColor=WARN_BG, borderPadding=9,
    leftIndent=3, rightIndent=3, spaceBefore=20, spaceAfter=22)

STYLES["caption"] = ParagraphStyle(
    "caption", fontName="Helvetica-Oblique", fontSize=8.5, leading=11.5,
    textColor=SOFT, alignment=TA_CENTER, spaceBefore=3, spaceAfter=10)

STYLES["big"] = ParagraphStyle(
    "big", parent=STYLES["body"], fontSize=11.5, leading=17)


def idea(text):
    """A comparison with something from everyday life."""
    return [Paragraph("<b>Think of it like this.</b> " + markup(text),
                      STYLES["idea"])]


def remember(text):
    """The one thing to take away from a section."""
    return [Paragraph("<b>Remember:</b> " + markup(text), STYLES["remember"])]


def careful(text):
    """A trap, or something an examiner might test."""
    return [Paragraph("<b>Be careful:</b> " + markup(text),
                      STYLES["careful"])]


def tryit(text, command=None):
    """Something to run on the computer, and what should happen."""
    parts = [Paragraph("<b>Try it yourself.</b> " + markup(text),
                       STYLES["tryit"])]
    if command:
        parts += code(command)
    else:
        parts.append(Spacer(1, 16))
    return parts


def big(text):
    """A slightly larger paragraph, for the key sentence of a chapter."""
    return [Paragraph(markup(text), STYLES["big"])]


def image(path, width_cm, caption=None, max_height_cm=13):
    """A picture, scaled to a width and kept in proportion."""
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Image

    w, h = ImageReader(str(path)).getSize()
    width = width_cm * cm
    height = width * h / w
    if height > max_height_cm * cm:
        height = max_height_cm * cm
        width = height * w / h

    parts = [Image(str(path), width=width, height=height)]
    if caption:
        parts.append(Paragraph(markup(caption), STYLES["caption"]))
    else:
        parts.append(Spacer(1, 8))
    return [KeepTogether(parts)]


def glossary(pairs):
    """A two column word list, sorted A to Z."""
    rows = [["Word", "What it means"]]
    for word, meaning in sorted(pairs, key=lambda x: x[0].lower()):
        rows.append([f"**{word}**", meaning])
    return table(rows, widths=[2.2, 6.3])


#=========================================================================#
#  BUILD                                                                  #
#=========================================================================#

def build(path, footer, blocks, toc_depth=2):
    doc = Guide(str(path), footer, toc_depth=toc_depth)
    # multiBuild runs the document twice so the contents page can pick up
    # the real page numbers.
    doc.multiBuild(blocks)
    return path
