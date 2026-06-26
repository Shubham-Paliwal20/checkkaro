"""
Converts PROJECT_DOCUMENTATION.md to a styled PDF.
"""
from fpdf import FPDF
import re

MD_FILE = "PROJECT_DOCUMENTATION.md"
PDF_FILE = "CheckKaro_Project_Documentation.pdf"

BRAND_COLOR  = (30, 90, 60)    # dark green
HEAD2_COLOR  = (30, 58, 138)   # navy
HEAD3_COLOR  = (55, 65, 81)    # dark grey
CODE_BG      = (245, 245, 245)
CODE_FG      = (31, 41, 55)
TABLE_HEADER = (30, 58, 138)
TABLE_ALT    = (248, 250, 252)
AMBER        = (180, 100, 0)

class DocPDF(FPDF):
    def header(self):
        self.set_fill_color(*BRAND_COLOR)
        self.rect(0, 0, 210, 10, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        self.set_xy(10, 2)
        self.cell(0, 6, "Parkho (CheckKaro) -- Project Documentation", align="L")
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-12)
        self.set_fill_color(*BRAND_COLOR)
        self.rect(0, self.get_y(), 210, 12, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "", 7)
        self.set_x(10)
        self.cell(0, 8, f"Page {self.page_no()} -- Confidential -- For internal/developer use only", align="L")
        self.set_text_color(0, 0, 0)


def safe(text):
    # Replace common Unicode punctuation with ASCII equivalents before encoding
    text = text.replace('--', '--').replace('-', '-')
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('…', '...').replace('°', ' deg')
    text = text.replace('→', '->').replace('←', '<-')
    text = text.replace('•', '*').replace('·', '.')
    return text.encode('latin-1', 'replace').decode('latin-1')


def strip_inline(text):
    """Remove markdown inline formatting for plain rendering."""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*',     r'\1', text)
    text = re.sub(r'`(.+?)`',       r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return text


def render(pdf, lines):
    in_code    = False
    code_buf   = []
    in_table   = False
    table_rows = []
    i = 0

    while i < len(lines):
        raw = lines[i]
        stripped = raw.rstrip()

        # ── Code block ────────────────────────────────────────────────────────
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_buf = []
            else:
                in_code = False
                # render code block
                if code_buf:
                    pdf.set_fill_color(*CODE_BG)
                    pdf.set_draw_color(200, 200, 200)
                    pdf.set_font("Courier", "", 7.5)
                    pdf.set_text_color(*CODE_FG)
                    pdf.set_x(14)
                    block_text = "\n".join(code_buf)
                    pdf.multi_cell(
                        182, 4.5,
                        safe(block_text),
                        border=1, fill=True, align="L"
                    )
                    pdf.ln(2)
                    code_buf = []
                pdf.set_text_color(0, 0, 0)
                pdf.set_draw_color(0, 0, 0)
            i += 1
            continue

        if in_code:
            code_buf.append(stripped)
            i += 1
            continue

        # ── Table ─────────────────────────────────────────────────────────────
        if stripped.startswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            # skip separator rows like |---|---|
            if all(re.match(r'^[-:]+$', c) for c in cells if c):
                i += 1
                continue
            table_rows.append(cells)
            i += 1
            # peek ahead -- if next line is not a table row, flush
            next_line = lines[i].rstrip() if i < len(lines) else ""
            if not next_line.startswith("|"):
                flush_table(pdf, table_rows)
                table_rows = []
            continue

        # ── H1 ────────────────────────────────────────────────────────────────
        if stripped.startswith("# ") and not stripped.startswith("## "):
            text = strip_inline(stripped[2:])
            pdf.ln(4)
            pdf.set_fill_color(*BRAND_COLOR)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_x(10)
            pdf.cell(190, 10, safe(text), fill=True, align="C", ln=True)
            pdf.ln(4)
            pdf.set_text_color(0, 0, 0)
            i += 1
            continue

        # ── H2 ────────────────────────────────────────────────────────────────
        if stripped.startswith("## "):
            text = strip_inline(stripped[3:])
            pdf.ln(5)
            pdf.set_text_color(*HEAD2_COLOR)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_x(10)
            pdf.cell(0, 8, safe(text), ln=True)
            # underline rule
            pdf.set_draw_color(*HEAD2_COLOR)
            pdf.set_line_width(0.5)
            x = pdf.get_x()
            y = pdf.get_y()
            pdf.line(10, y, 200, y)
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)
            pdf.set_text_color(0, 0, 0)
            i += 1
            continue

        # ── H3 ────────────────────────────────────────────────────────────────
        if stripped.startswith("### "):
            text = strip_inline(stripped[4:])
            pdf.ln(3)
            pdf.set_text_color(*HEAD3_COLOR)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(10)
            pdf.cell(0, 7, safe(text), ln=True)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0)
            i += 1
            continue

        # ── H4 ────────────────────────────────────────────────────────────────
        if stripped.startswith("#### "):
            text = strip_inline(stripped[5:])
            pdf.ln(2)
            pdf.set_text_color(*AMBER)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_x(10)
            pdf.cell(0, 6, safe(text), ln=True)
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0)
            i += 1
            continue

        # ── HR ────────────────────────────────────────────────────────────────
        if stripped.startswith("---"):
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)
            i += 1
            continue

        # ── Blank line ────────────────────────────────────────────────────────
        if not stripped:
            pdf.ln(2)
            i += 1
            continue

        # ── Blockquote ────────────────────────────────────────────────────────
        if stripped.startswith("> "):
            text = strip_inline(stripped[2:])
            pdf.set_fill_color(235, 245, 255)
            pdf.set_draw_color(100, 150, 220)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(40, 60, 120)
            pdf.set_x(14)
            pdf.multi_cell(176, 5.5, safe(text), border="L", fill=True, align="L")
            pdf.ln(1)
            pdf.set_text_color(0, 0, 0)
            pdf.set_draw_color(0, 0, 0)
            i += 1
            continue

        # ── Bullet list ───────────────────────────────────────────────────────
        if stripped.startswith("- ") or stripped.startswith("* "):
            text = strip_inline(stripped[2:])
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            y = pdf.get_y()
            pdf.set_x(14)
            pdf.cell(4, 5.5, chr(149), ln=False)   # bullet
            pdf.set_x(18)
            pdf.multi_cell(176, 5.5, safe(text), align="L")
            pdf.ln(0.5)
            i += 1
            continue

        # ── Numbered list ─────────────────────────────────────────────────────
        num_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if num_match:
            num  = num_match.group(1)
            text = strip_inline(num_match.group(2))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(14)
            pdf.cell(6, 5.5, f"{num}.", ln=False)
            pdf.set_x(20)
            pdf.multi_cell(174, 5.5, safe(text), align="L")
            pdf.ln(0.5)
            i += 1
            continue

        # ── Regular paragraph ─────────────────────────────────────────────────
        text = strip_inline(stripped)
        if text:
            pdf.set_font("Helvetica", "", 9.5)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(10)
            pdf.multi_cell(190, 5.5, safe(text), align="L")
            pdf.ln(1)

        i += 1


def flush_table(pdf, rows):
    if not rows:
        return
    pdf.ln(2)
    num_cols = max(len(r) for r in rows)
    if num_cols == 0:
        return

    col_w = 190 / num_cols

    for ri, row in enumerate(rows):
        if ri == 0:
            # header
            pdf.set_fill_color(*TABLE_HEADER)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Helvetica", "B", 8)
        else:
            fill = ri % 2 == 0
            pdf.set_fill_color(*(TABLE_ALT if fill else (255, 255, 255)))
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 8)

        pdf.set_x(10)
        # measure row height
        max_lines = 1
        for cell in row:
            chars_per_line = int(col_w / 2.2)
            lines = max(1, len(safe(strip_inline(cell))) // chars_per_line + 1)
            max_lines = max(max_lines, lines)
        row_h = max(5.5, max_lines * 5)

        x_start = 10
        y_start = pdf.get_y()
        for ci, cell in enumerate(row):
            text = safe(strip_inline(cell))
            pdf.set_xy(x_start + ci * col_w, y_start)
            pdf.multi_cell(col_w, row_h / max(1, max_lines), text,
                           border=1, fill=(ri == 0 or ri % 2 == 0), align="L")
            pdf.set_xy(x_start + (ci + 1) * col_w, y_start)

        pdf.set_xy(10, y_start + row_h)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)


def build_cover(pdf):
    pdf.add_page()
    # background strip
    pdf.set_fill_color(*BRAND_COLOR)
    pdf.rect(0, 0, 210, 70, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_xy(10, 22)
    pdf.cell(190, 14, "Parkho", align="C", ln=True)

    pdf.set_font("Helvetica", "", 13)
    pdf.set_xy(10, 38)
    pdf.cell(190, 8, "(CheckKaro) -- Project Documentation", align="C", ln=True)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_xy(10, 52)
    pdf.cell(190, 6, "Complete technical reference for developers", align="C", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, 78)
    pdf.set_font("Helvetica", "", 10)
    info = [
        ("Project",     "Parkho / CheckKaro"),
        ("Platform",    "React + FastAPI + Supabase"),
        ("Deployed on", "Vercel (frontend) + Render (backend)"),
        ("Prepared by", "Shubham Paliwal"),
        ("Date",        "June 2026"),
    ]
    for label, value in info:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_x(30)
        pdf.cell(50, 7, label + ":", ln=False)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(120, 7, value, ln=True)

    # notice box
    pdf.set_fill_color(255, 248, 230)
    pdf.set_draw_color(200, 140, 0)
    pdf.set_xy(20, 140)
    pdf.multi_cell(170, 6,
        "NOTICE: This document is for internal and developer use only. "
        "It does not contain any API keys, passwords, or credentials. "
        "Do not share publicly.",
        border=1, fill=True, align="C")


def main():
    with open(MD_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    pdf = DocPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(10, 14, 10)

    # Cover page
    build_cover(pdf)

    # Content pages
    pdf.add_page()
    render(pdf, lines)

    pdf.output(PDF_FILE)
    print(f"PDF saved: {PDF_FILE}")


if __name__ == "__main__":
    main()
