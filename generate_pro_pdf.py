"""
Parkho / CheckKaro -- Professional Project Documentation PDF
Matches the design from CheckKaro_Documentation.pdf
"""
from fpdf import FPDF

OUT = "CheckKaro_Project_Documentation.pdf"

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY        = (26,  43,  74)
NAVY_MED    = (30,  58,  138)
NAVY_DARK   = (15,  23,  42)
ORANGE      = (234, 88,  12)
ORANGE_LT   = (249, 115, 22)
WHITE       = (255, 255, 255)
GRAY_900    = (17,  24,  39)
GRAY_700    = (55,  65,  81)
GRAY_500    = (107, 114, 128)
GRAY_300    = (209, 213, 219)
GRAY_100    = (243, 244, 246)
GRAY_50     = (249, 250, 251)
BLUE_700    = (29,  78,  216)
BLUE_100    = (219, 234, 254)
GREEN_700   = (21,  128, 61)
GREEN_100   = (220, 252, 231)
AMBER_700   = (180, 83,  9)
AMBER_100   = (254, 243, 199)
RED_700     = (185, 28,  28)
RED_100     = (254, 226, 226)
CODE_BG     = (15,  23,  42)
CODE_TEXT   = (148, 163, 184)
TBL_HEAD    = (30,  58,  138)
TBL_ALT     = (248, 250, 252)
CALLOUT_BG  = (239, 246, 255)
CALLOUT_BD  = (59,  130, 246)
WARN_BG     = (255, 251, 235)
WARN_BD     = (202, 138, 4)
TAG_BG      = (30,  58,  95)   # tech stack pill background

def safe(t):
    subs = {
        '—':'--', '–':'-', '→':'->', '←':'<-',
        '‘':"'",  '’':"'", '“':'"',  '”':'"',
        '…':'...', '°':' deg', '•':'*', '₹':'Rs.',
        'é':'e',   '×':'x',  '≥':'>=', '≤':'<=',
        '─':'-',   '├':'|', '└':'L',   '├':'|',
        '←':'<-',  '≈':'~=', ' ':' ',
        # Box drawing characters
        '│':'|',   '┌':'+',  '┐':'+',
        '┘':'+',   '╞':'|',  '╡':'|',
        '╠':'|',   '╣':'|',  '╦':'+', '╩':'+',
    }
    for k, v in subs.items():
        t = t.replace(k, v)
    return t.encode('latin-1', 'replace').decode('latin-1')


# ── PDF Class ─────────────────────────────────────────────────────────────────
class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self._page_label = ""
        self.total_pages = 0

    def header(self):
        if self.page_no() == 1:
            return
        # thin navy bar
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 9, 'F')
        self.set_text_color(*WHITE)
        self.set_font('Helvetica', 'B', 7)
        self.set_xy(10, 1.5)
        self.cell(0, 6, "Parkho -- Technical Documentation", align='L')
        self.set_xy(0, 1.5)
        self.cell(200, 6, "www.parkho.in", align='R')
        self.set_text_color(0, 0, 0)
        self.set_y(12)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_draw_color(*GRAY_300)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(1)
        self.set_font('Helvetica', '', 7)
        self.set_text_color(*GRAY_500)
        self.set_x(10)
        self.cell(0, 5, f"Page {self.page_no()}", align='C')
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)


# ── Element Helpers ───────────────────────────────────────────────────────────

def pill(pdf, text, bg, fg, x, y, pad_x=3, h=6, fs=7.5):
    pdf.set_font('Helvetica', 'B', fs)
    w = pdf.get_string_width(text) + pad_x * 2
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*bg)
    pdf.rect(x, y, w, h, 'F')
    pdf.set_text_color(*fg)
    pdf.set_xy(x, y)
    pdf.cell(w, h, text, align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(0, 0, 0)
    return x + w + 2


def section_header(pdf, num, title):
    pdf.ln(6)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(*GRAY_900)
    pdf.set_x(10)
    pdf.cell(0, 10, safe(f"{num}. {title}"), ln=True)
    # orange underline
    pdf.set_draw_color(*ORANGE)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(4)
    pdf.set_text_color(0, 0, 0)


def subsection(pdf, title):
    pdf.ln(4)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*BLUE_700)
    pdf.set_x(10)
    pdf.cell(0, 7, safe(title), ln=True)
    pdf.ln(1)
    pdf.set_text_color(0, 0, 0)


def subsubsection(pdf, title):
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(*GRAY_700)
    pdf.set_x(10)
    pdf.cell(0, 6, safe(title), ln=True)
    pdf.set_text_color(0, 0, 0)


def para(pdf, text, indent=10):
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(*GRAY_700)
    pdf.set_x(indent)
    pdf.multi_cell(200 - indent, 5.5, safe(text), align='L')
    pdf.ln(1)
    pdf.set_text_color(0, 0, 0)


def bullet(pdf, items, indent=14):
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(*GRAY_700)
    for item in items:
        pdf.set_x(indent)
        pdf.cell(4, 5.5, '*', ln=False)
        pdf.set_x(indent + 4)
        pdf.multi_cell(200 - indent - 4, 5.5, safe(item), align='L')
        pdf.ln(0.5)
    pdf.set_text_color(0, 0, 0)


def numbered_list(pdf, items, indent=14):
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(*GRAY_700)
    for i, item in enumerate(items, 1):
        pdf.set_x(indent)
        pdf.cell(6, 5.5, f"{i}.", ln=False)
        pdf.set_x(indent + 6)
        pdf.multi_cell(200 - indent - 6, 5.5, safe(item), align='L')
        pdf.ln(0.5)
    pdf.set_text_color(0, 0, 0)


def callout(pdf, text, label=None, bg=CALLOUT_BG, bd=CALLOUT_BD):
    pdf.ln(2)
    pdf.set_fill_color(*bg)
    pdf.set_draw_color(*bd)
    pdf.set_line_width(0.3)
    y0 = pdf.get_y()
    pdf.set_x(10)
    # left border bar
    pdf.set_fill_color(*bd)
    pdf.rect(10, y0, 2, 20, 'F')   # placeholder; we'll recalculate
    pdf.set_fill_color(*bg)
    pdf.set_x(12)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(*NAVY_MED)
    if label:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(0, 5.5, safe(label), ln=True)
        pdf.set_x(14)
        pdf.set_font('Helvetica', '', 9)
    else:
        pdf.set_x(14)
    y1 = pdf.get_y()
    pdf.multi_cell(180, 5.5, safe(text), align='L')
    y2 = pdf.get_y()
    # draw left border
    pdf.set_fill_color(*bd)
    pdf.rect(10, y0, 2.5, y2 - y0 + 2, 'F')
    # draw background
    pdf.set_fill_color(*bg)
    pdf.rect(12.5, y0, 188, y2 - y0 + 2, 'F')
    # redraw text on top
    pdf.set_xy(14, y0 + (2 if label else 2))
    if label:
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(*NAVY_MED)
        pdf.cell(0, 5.5, safe(label), ln=True)
        pdf.set_x(14)
        pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(180, 5.5, safe(text), align='L')
    pdf.set_y(y2 + 2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.2)
    pdf.ln(1)


def code_block(pdf, code_lines):
    pdf.ln(2)
    all_text = '\n'.join(code_lines) if isinstance(code_lines, list) else code_lines
    line_count = all_text.count('\n') + 1
    block_h = max(12, line_count * 4.5 + 6)
    y0 = pdf.get_y()
    pdf.set_fill_color(*CODE_BG)
    pdf.set_draw_color(*CODE_BG)
    pdf.rect(10, y0, 190, block_h, 'F')
    pdf.set_xy(14, y0 + 3)
    pdf.set_font('Courier', '', 7.5)
    pdf.set_text_color(*CODE_TEXT)
    pdf.multi_cell(182, 4.5, safe(all_text), align='L')
    pdf.set_y(y0 + block_h + 2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(1)


def table(pdf, headers, rows, col_widths=None, font_size=8.5):
    if not headers:
        return
    pdf.ln(2)
    n = len(headers)
    if col_widths is None:
        col_widths = [190 / n] * n
    row_h = 7

    # Header row
    pdf.set_fill_color(*TBL_HEAD)
    pdf.set_text_color(*WHITE)
    pdf.set_font('Helvetica', 'B', font_size)
    pdf.set_x(10)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], row_h, safe(h), border=1, fill=True, align='L')
    pdf.ln(row_h)

    # Data rows
    pdf.set_font('Helvetica', '', font_size)
    for ri, row in enumerate(rows):
        # estimate row height
        max_lines = 1
        for ci, cell in enumerate(row):
            if ci < len(col_widths):
                chars_per_line = max(1, int(col_widths[ci] / 2.2))
                lines = max(1, (len(safe(str(cell))) // chars_per_line) + 1)
                max_lines = max(max_lines, lines)
        rh = max(row_h, max_lines * 5)

        fill = ri % 2 == 1
        pdf.set_fill_color(*(TBL_ALT if fill else WHITE))
        pdf.set_text_color(*GRAY_900)
        x0 = 10
        y0 = pdf.get_y()
        for ci, cell in enumerate(row):
            if ci >= len(col_widths):
                break
            w = col_widths[ci]
            # Draw cell background
            pdf.set_xy(x0, y0)
            pdf.set_fill_color(*(TBL_ALT if fill else WHITE))
            pdf.multi_cell(w, rh / max_lines, safe(str(cell)), border=1, fill=True, align='L')
            x0 += w
            pdf.set_xy(x0, y0)
        pdf.set_xy(10, y0 + rh)

    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.ln(3)


def api_endpoint(pdf, method, path, description):
    y0 = pdf.get_y()
    pdf.set_x(10)
    # method badge
    colors = {
        'GET':    (GREEN_100, GREEN_700),
        'POST':   (AMBER_100, AMBER_700),
        'DELETE': (RED_100,   RED_700),
        'PATCH':  (BLUE_100,  BLUE_700),
        'PUT':    (BLUE_100,  BLUE_700),
    }
    bg, fg = colors.get(method, (GRAY_100, GRAY_700))
    pdf.set_fill_color(*bg)
    pdf.set_text_color(*fg)
    pdf.set_font('Helvetica', 'B', 7.5)
    badge_w = 14
    pdf.cell(badge_w, 6, method, fill=True, border=0, align='C')
    # path
    pdf.set_text_color(*NAVY_MED)
    pdf.set_font('Courier', 'B', 8)
    pdf.cell(0, 6, safe('  ' + path), ln=True)
    # description
    pdf.set_x(10 + badge_w + 2)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(*GRAY_500)
    pdf.multi_cell(185 - badge_w, 5, safe(description), align='L')
    pdf.ln(2)
    # left border rule
    pdf.set_fill_color(*CALLOUT_BD)
    pdf.rect(10, y0, 1.5, pdf.get_y() - y0, 'F')
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)


def grade_badge_inline(pdf, grade, text):
    colors = {'A': GREEN_700, 'B': BLUE_700, 'C': AMBER_700, 'D': RED_700}
    c = colors.get(grade, GRAY_700)
    pdf.set_fill_color(*c)
    pdf.set_text_color(*WHITE)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(8, 8, grade, fill=True, align='C')
    pdf.set_text_color(*GRAY_700)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 8, safe('  ' + text), ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)


def divider(pdf):
    pdf.ln(3)
    pdf.set_draw_color(*GRAY_300)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.set_draw_color(0, 0, 0)
    pdf.ln(4)


# ── Cover Page ────────────────────────────────────────────────────────────────

def cover_page(pdf):
    pdf.add_page()
    # Full navy background
    pdf.set_fill_color(*NAVY_DARK)
    pdf.rect(0, 0, 210, 297, 'F')

    # "TECHNICAL DOCUMENTATION" orange pill badge
    badge_text = "TECHNICAL DOCUMENTATION"
    pdf.set_font('Helvetica', 'B', 7)
    bw = pdf.get_string_width(badge_text) + 8
    bx = (210 - bw) / 2
    pdf.set_fill_color(*ORANGE)
    pdf.rect(bx, 38, bw, 7, 'F')
    pdf.set_text_color(*WHITE)
    pdf.set_xy(bx, 38)
    pdf.cell(bw, 7, badge_text, align='C')

    # "Parkho" title
    pdf.set_font('Helvetica', 'B', 48)
    pdf.set_text_color(*ORANGE)
    pdf.set_xy(0, 50)
    pdf.cell(210, 20, "Parkho", align='C', ln=True)

    # Subtitle
    pdf.set_font('Helvetica', '', 13)
    pdf.set_text_color(180, 195, 215)
    pdf.set_x(0)
    pdf.cell(210, 8, safe("Know What's Inside -- Full Project Documentation"), align='C', ln=True)

    # Tech stack pills
    pills = ["React 18", "FastAPI", "Supabase", "Vercel", "Render", "Google Gemini"]
    total_w = sum(pdf.get_string_width(p) + 12 for p in pills) + (len(pills) - 1) * 3
    x = (210 - total_w) / 2
    y = 90
    pdf.set_font('Helvetica', 'B', 7.5)
    for p in pills:
        w = pdf.get_string_width(p) + 12
        pdf.set_fill_color(40, 70, 110)
        pdf.set_text_color(*WHITE)
        pdf.rect(x, y, w, 7, 'F')
        pdf.set_xy(x, y)
        pdf.cell(w, 7, p, align='C')
        x += w + 3

    # Second row pills
    row2 = ["Tailwind CSS", "PostgreSQL"]
    total_w2 = sum(pdf.get_string_width(p) + 12 for p in row2) + (len(row2) - 1) * 3
    x = (210 - total_w2) / 2
    y = 101
    for p in row2:
        w = pdf.get_string_width(p) + 12
        pdf.set_fill_color(40, 70, 110)
        pdf.set_text_color(*WHITE)
        pdf.rect(x, y, w, 7, 'F')
        pdf.set_xy(x, y)
        pdf.cell(w, 7, p, align='C')
        x += w + 3

    # URL info
    info = [
        ("[WEB]  Production URL:", "https://www.parkho.in"),
        ("[API]  Backend API:",    "https://checkkaro.onrender.com"),
        ("[DB]   Database:",       "Supabase (PostgreSQL)"),
    ]
    y = 120
    pdf.set_font('Helvetica', '', 9)
    for label, val in info:
        pdf.set_text_color(160, 180, 210)
        pdf.set_xy(40, y)
        pdf.cell(65, 7, label)
        pdf.set_text_color(*WHITE)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(0, 7, val)
        pdf.set_font('Helvetica', '', 9)
        y += 8

    # Version
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(100, 130, 170)
    pdf.set_xy(0, 155)
    pdf.cell(210, 6, "Version 1.0  |  June 2026", align='C')

    # Bottom white bar for page number
    pdf.set_fill_color(25, 38, 65)
    pdf.rect(0, 277, 210, 20, 'F')
    pdf.set_text_color(120, 150, 190)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_xy(0, 281)
    pdf.cell(210, 6, "Page 1", align='C')
    pdf.set_text_color(0, 0, 0)


# ── Table of Contents ─────────────────────────────────────────────────────────

def toc_page(pdf):
    pdf.add_page()
    pdf.set_y(14)

    # TOC box
    y0 = pdf.get_y()
    pdf.set_fill_color(*CALLOUT_BG)
    pdf.set_draw_color(*CALLOUT_BD)
    pdf.set_line_width(0.5)
    pdf.rect(10, y0, 190, 90, 'FD')
    pdf.set_line_width(0.2)

    pdf.set_xy(14, y0 + 4)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(*NAVY_MED)
    pdf.cell(0, 7, "[=] Table of Contents", ln=True)

    toc_items = [
        ("1.", "What Is This App?"),
        ("2.", "Tech Stack"),
        ("3.", "High-Level Architecture"),
        ("4.", "Repository Structure"),
        ("5.", "Backend -- FastAPI"),
        ("6.", "Frontend -- React"),
        ("7.", "Database -- Supabase"),
        ("8.", "Ingredient Classification Engine"),
        ("9.", "Grading System"),
        ("10.", "Authentication"),
        ("11.", "Admin Panel"),
        ("12.", "Deployment"),
        ("13.", "Local Setup Guide"),
        ("14.", "Key Concepts for New Developers"),
        ("15.", "What NOT to Touch"),
    ]
    # Two columns
    mid = len(toc_items) // 2
    col1 = toc_items[:mid]
    col2 = toc_items[mid:]

    base_y = pdf.get_y() + 2
    for i, ((n1, t1), (n2, t2)) in enumerate(zip(col1, col2)):
        pdf.set_xy(16, base_y + i * 6.5)
        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(*ORANGE)
        pdf.cell(8, 6, n1)
        pdf.set_font('Helvetica', '', 8.5)
        pdf.set_text_color(*BLUE_700)
        pdf.cell(82, 6, t1)

        pdf.set_font('Helvetica', 'B', 8.5)
        pdf.set_text_color(*ORANGE)
        pdf.cell(9, 6, n2)
        pdf.set_font('Helvetica', '', 8.5)
        pdf.set_text_color(*BLUE_700)
        pdf.cell(0, 6, t2, ln=True)

    pdf.set_y(y0 + 94)
    pdf.set_text_color(0, 0, 0)


# ── Section 1: What Is This App ───────────────────────────────────────────────

def sec1(pdf):
    section_header(pdf, 1, "What Is This App?")

    para(pdf, "Parkho (formerly CheckKaro) is an ingredient awareness platform for Indian consumers.")

    bullet(pdf, [
        "Search any food or cosmetic product by name",
        "See a Grade (A / B / C / D) based on the ingredient list",
        "Understand what each ingredient is -- in plain English with scientific detail",
        "Check any ingredient individually on the Check Ingredient page",
        "Submit new products for review and upload product photos",
        "Read and write blogs about ingredient safety",
    ])

    callout(pdf,
        "Core Value Proposition: Type any Indian product name (e.g. 'Maggi 2-Minute Masala Noodles') "
        "and instantly see every ingredient explained in plain English -- whether it's safe, questionable, "
        "or restricted -- with FSSAI regulatory context.",
        label="Core Value Proposition")

    para(pdf, "The app is live at www.parkho.in and is targeted at Indian consumers using FSSAI-aligned ingredient data.")

    subsection(pdf, "Key Numbers")
    table(pdf,
        ["Metric", "Value"],
        [
            ["Products in database",          "570+ (ai_extracted_products table)"],
            ["Ingredient entries",             "1,000+ (ingredient_database.py)"],
            ["E/INS number entries",           "167 indexed E-numbers"],
            ["Ingredient classification tiers","3 (generally_recognised, worth_knowing, commonly_questioned)"],
            ["Product grade system",          "A / B / C / D"],
            ["Frontend pages",                "9 routes"],
            ["API endpoints",                 "~20"],
        ],
        col_widths=[80, 110]
    )


# ── Section 2: Tech Stack ─────────────────────────────────────────────────────

def sec2(pdf):
    section_header(pdf, 2, "Tech Stack")

    table(pdf,
        ["Layer", "Technology", "Hosted On"],
        [
            ["Frontend",      "React 18 + Vite + Tailwind CSS",        "Vercel"],
            ["Backend",       "FastAPI (Python 3.11)",                  "Render"],
            ["Database",      "PostgreSQL via Supabase",                "Supabase"],
            ["Auth",          "Supabase Auth (email OTP + Google OAuth)","Supabase"],
            ["File Storage",  "Supabase Storage (S3-compatible)",       "Supabase"],
            ["AI Extraction", "Google Gemini 1.5 Flash (image->ingredients)", "Google Cloud"],
            ["AI Analysis",   "Groq (LLaMA 3 70B), Anthropic Claude",  "Cloud APIs"],
        ],
        col_widths=[40, 100, 50]
    )

    subsection(pdf, "Backend Package Versions")
    table(pdf,
        ["Package", "Version", "Purpose"],
        [
            ["fastapi",             "0.111.0",  "Web framework -- async HTTP, routing, validation"],
            ["uvicorn[standard]",   "0.29.0",   "ASGI server"],
            ["supabase",            "2.4.2",    "Supabase Python client (DB + Auth)"],
            ["google-generativeai", "0.8.3",    "Gemini API for ingredient extraction from images"],
            ["groq",                "0.9.0",    "Groq API (LLaMA) -- fast AI inference"],
            ["anthropic",           ">=0.40.0", "Claude API -- ingredient analysis"],
            ["httpx",               "0.27.0",   "Async HTTP client for external API calls"],
            ["pydantic",            "2.7.1",    "Request/response data validation"],
            ["python-dotenv",       "1.0.1",    "Load environment variables from .env file"],
        ],
        col_widths=[50, 25, 115]
    )

    subsection(pdf, "Frontend Package Versions")
    table(pdf,
        ["Package", "Version", "Purpose"],
        [
            ["react",               "18.3.1",  "UI framework"],
            ["react-router-dom",    "6.23.1",  "Client-side routing (9 routes)"],
            ["@supabase/supabase-js","2.103.3", "Supabase client -- DB queries, auth, storage"],
            ["axios",               "1.7.2",   "HTTP client for backend API calls"],
            ["framer-motion",       "11.2.10", "Page transitions and micro-animations"],
            ["react-helmet-async",  "3.0.0",   "Dynamic <head> for SEO"],
            ["vite",                "5.2.12",  "Build tool and dev server"],
            ["tailwindcss",         "3.4.4",   "Utility-first CSS framework"],
        ],
        col_widths=[55, 25, 110]
    )


# ── Section 3: Architecture ───────────────────────────────────────────────────

def sec3(pdf):
    section_header(pdf, 3, "High-Level Architecture")

    para(pdf, "Parkho uses a classic Client-Server + Layered N-Tier architecture:")

    code_block(pdf, """User's Browser
      |
      |-- React Frontend (Vercel / www.parkho.in)
      |         |
      |         |-- axios --> FastAPI Backend (Render / checkkaro.onrender.com)
      |         |               |
      |         |               |-- ingredient_database.py  <- Classification engine
      |         |               |-- grading.py              <- A/B/C/D logic
      |         |               L-- Supabase PostgreSQL     <- Product data
      |         |
      |         L-- Supabase JS client (anon key)
      |                   |
      |                   |-- Auth (login / signup / Google OAuth)
      |                   |-- product_photos (read)
      |                   L-- product_reviews (read/write)
      |
Admin Browser
      |
      L-- /admin page --> FastAPI /api/admin (JWT required)
                              |
                              L-- Google Gemini (image extraction)""")

    subsection(pdf, "Request Flow -- Product Search")
    numbered_list(pdf, [
        "React frontend sends GET /api/product/search?name=Maggi+Masala+Noodles",
        "Backend checks in-memory search cache (5-min TTL, 500 entries max)",
        "Cache miss: multi-strategy fuzzy search in Supabase (exact -> prefix -> word pattern -> substring)",
        "Product found with stored ingredients: fast path -- skip re-classification",
        "Product found without ingredients: slow path -- classify each ingredient, store result",
        "Compute A/B/C/D grade, build ProductResponse JSON",
        "Cache result, return to frontend",
        "React renders ingredient cards with classification badges",
    ])

    callout(pdf,
        "Key design decision: The backend is the primary source of product data. "
        "The frontend has a direct Supabase fallback (read-only) for when Render free tier "
        "is cold-starting. Both paths return identical product data.",
        label="Design Decision")


# ── Section 4: Repository Structure ──────────────────────────────────────────

def sec4(pdf):
    section_header(pdf, 4, "Repository Structure")

    code_block(pdf, """checkkaro/
|-- backend/                    <- FastAPI Python app
|   |-- main.py                 <- App entry point, middleware, routers
|   |-- grading.py              <- Grade calculation (A/B/C/D)
|   |-- requirements.txt
|   |-- db/
|   |   L-- supabase_client.py  <- Two Supabase connections (anon + admin)
|   |-- models/
|   |   L-- schemas.py          <- Pydantic request/response models
|   |-- routes/
|   |   |-- product_new.py      <- ACTIVE: all product endpoints + caching
|   |   |-- ingredient.py       <- Ingredient search endpoints
|   |   |-- ingredient_database.py  <- 5500-line classification engine
|   |   |-- admin_extract.py    <- Admin: Gemini extraction + product CRUD
|   |   |-- reports.py          <- Admin: ingredient report review
|   |   L-- history.py          <- Search history (stub)
|   L-- services/               <- External API clients (Gemini, Groq, Claude)
|
|-- frontend/                   <- React Vite app
|   |-- index.html              <- Root HTML with meta tags, OG tags
|   |-- vite.config.js
|   |-- tailwind.config.js
|   |-- vercel.json             <- SPA rewrites + security + cache headers
|   |-- public/
|   |   |-- sitemap.xml         <- Sitemap index (3 child sitemaps)
|   |   |-- robots.txt          <- Allow /, Disallow /admin, /blog/write
|   |   L-- og-image.png        <- 1200x630 Open Graph social preview image
|   L-- src/
|       |-- main.jsx            <- Entry point -- HelmetProvider wrapper
|       |-- App.jsx             <- Router, AuthProvider, Navbar, Footer
|       |-- context/
|       |   L-- AuthContext.jsx <- Global auth state
|       |-- lib/
|       |   L-- supabaseClient.js   <- Supabase client + session refresh
|       |-- pages/              <- 9 full pages
|       L-- components/         <- 17 reusable components
|
L-- _saved_recommendations_feature.md  <- Saved feature code for later""")


# ── Section 5: Backend ────────────────────────────────────────────────────────

def sec5(pdf):
    section_header(pdf, 5, "Backend -- FastAPI")

    subsection(pdf, "Entry Point: main.py")
    bullet(pdf, [
        "Rate limiting -- 60 requests/minute per IP (in-memory sliding window)",
        "Security headers -- X-Frame-Options, X-Content-Type-Options, HSTS",
        "CORS -- allows parkho.in and *.vercel.app origins",
        "GZip compression on all responses > 500 bytes",
        "Sitemap generation -- /sitemap-products.xml, /sitemap-blogs.xml",
        "Health check -- GET /health (pinged by UptimeRobot to prevent Render sleep)",
    ])

    subsection(pdf, "Active Route Mounts")
    table(pdf,
        ["Mount Path", "File", "Purpose"],
        [
            ["/api/product",    "product_new.py",  "Product search, browse, suggestions, verify"],
            ["/api/ingredient", "ingredient.py",   "Ingredient lookup, list, popular"],
            ["/api/admin",      "admin_extract.py + reports.py", "Admin-only operations (JWT required)"],
            ["/api/history",    "history.py",      "Stub -- returns empty list"],
        ],
        col_widths=[45, 70, 75]
    )

    subsection(pdf, "Product Endpoints   /api/product")
    api_endpoint(pdf, "GET", "/api/product/search?name={query}",
        "Most important endpoint. Multi-strategy fuzzy search returns full ProductResponse with "
        "classified ingredients. Fast path uses stored ingredients; slow path re-classifies. Cached 5 min.")
    api_endpoint(pdf, "GET", "/api/product/browse?page=1&category=Snacks&brand=Nestle&sort=grade",
        "Paginated product browse with filters. Category, brand, search query, sort supported. Cached 2 min per filter combo.")
    api_endpoint(pdf, "GET", "/api/product/suggest?q={query}",
        "Typeahead suggestions -- returns product names matching query. Cached 5 minutes.")
    api_endpoint(pdf, "GET", "/api/product/brands",
        "List of all unique brand names for filter dropdown.")
    api_endpoint(pdf, "GET", "/api/product/categories",
        "List of all unique categories.")
    api_endpoint(pdf, "POST", "/api/product/verify?product_name=X&is_correct=true",
        "User confirms a product's ingredient data is correct.")
    api_endpoint(pdf, "POST", "/api/product/correct?product_name=X&ingredients=Y",
        "User submits corrected ingredient list. Creates a correction_report entry.")
    api_endpoint(pdf, "POST", "/api/product/report",
        "User reports a product issue (wrong data, missing product, outdated info).")

    subsection(pdf, "Ingredient Endpoints   /api/ingredient")
    api_endpoint(pdf, "GET", "/api/ingredient/check?name={ingredient}",
        "Looks up ingredient by name, E-number, or INS number. Returns classification, health effects, regulatory data.")
    api_endpoint(pdf, "GET", "/api/ingredient/list",
        "Paginated list of all known ingredients in the database.")
    api_endpoint(pdf, "GET", "/api/ingredient/suggestions?q={query}&limit=10",
        "Autocomplete suggestions for ingredient search. Cached 5 min.")
    api_endpoint(pdf, "GET", "/api/ingredient/popular",
        "Returns popular/featured ingredients list for homepage display.")

    subsection(pdf, "Admin Endpoints   /api/admin  (JWT required)")
    callout(pdf, "All admin endpoints require Authorization: Bearer {supabase_jwt} where the JWT belongs to the admin email.", bg=WARN_BG, bd=WARN_BD)
    api_endpoint(pdf, "POST", "/api/admin/extract-from-image",
        "Upload product image URL -> Gemini AI extracts ingredients -> saves to Supabase. Runs as background task.")
    api_endpoint(pdf, "GET",  "/api/admin/task-status/{task_id}",
        "Poll background extraction task status.")
    api_endpoint(pdf, "POST", "/api/admin/save-product",
        "Save or update a product with manually entered data.")
    api_endpoint(pdf, "DELETE", "/api/admin/delete-product/{id}",
        "Permanently delete a product from the database.")
    api_endpoint(pdf, "POST", "/api/admin/reports/approve",
        "Approve a correction report -- updates product ingredients in DB.")
    api_endpoint(pdf, "POST", "/api/admin/reports/reject",
        "Reject a correction report with optional reason.")

    subsection(pdf, "Utility Endpoints")
    api_endpoint(pdf, "GET", "/health",
        "Health check -- returns {status: ok}. Used by UptimeRobot and frontend keep-alive ping.")
    api_endpoint(pdf, "GET", "/sitemap-products.xml",
        "Dynamic XML sitemap of all products from Supabase. Used by Google Search Console.")
    api_endpoint(pdf, "GET", "/sitemap-blogs.xml",
        "Dynamic XML sitemap of all approved blog posts.")

    subsection(pdf, "In-Memory Caching Architecture")
    para(pdf, "Three in-memory caches (reset on each Render deploy, not shared across requests on paid plans):")
    table(pdf,
        ["Cache", "TTL", "Max Size", "Purpose"],
        [
            ["_search_cache", "5 min", "500 entries", "Full product search results"],
            ["_browse_cache", "2 min", "80 combos",   "Paginated browse results per filter combo"],
            ["_suggest_cache","5 min", "200 queries",  "Autocomplete suggestions"],
        ],
        col_widths=[45, 20, 30, 95]
    )


# ── Section 6: Frontend ───────────────────────────────────────────────────────

def sec6(pdf):
    section_header(pdf, 6, "Frontend -- React")

    subsection(pdf, "Pages (Routes)")
    table(pdf,
        ["Route", "File", "Description"],
        [
            ["/",                "Home.jsx",            "Landing page with search bar, reviews, how-it-works"],
            ["/products",        "Products.jsx",        "Browse/filter all products (paginated, 20 per page)"],
            ["/result/:name",    "Result.jsx",          "Product detail page -- core feature"],
            ["/check-ingredient","CheckIngredient.jsx", "Standalone ingredient lookup by name or E-number"],
            ["/admin",           "Admin.jsx",           "Admin dashboard (restricted to admin email)"],
            ["/blog",            "Blog.jsx",            "Blog listing (static + DB posts)"],
            ["/blog/:slug",      "BlogPost.jsx",        "Single blog post reader"],
            ["/blog/write",      "WriteBlog.jsx",       "User blog submission form (requires login)"],
            ["/about",           "About.jsx",           "About page"],
        ],
        col_widths=[45, 50, 95]
    )

    subsection(pdf, "Key Components")
    table(pdf,
        ["Component", "What It Does"],
        [
            ["SearchBar.jsx",        "Main search input with debounced autocomplete; navigates to /result/:name"],
            ["GradeBadge.jsx",       "Shows A/B/C/D grade as a colored pill with animated display"],
            ["AuthModal.jsx",        "Login/signup modal (email OTP + Google OAuth), multi-step flow"],
            ["ProductReviews.jsx",   "Star rating + comment widget per product"],
            ["SEO.jsx",              "Sets page title, meta tags, Open Graph, and JSON-LD structured data"],
            ["PhotoUploadModal.jsx", "Upload a product photo to Supabase Storage"],
            ["ProductNotFound.jsx",  "Shown when search finds nothing; lets user submit the product"],
            ["DisclaimerBox.jsx",    "FSSAI disclaimer shown on result pages"],
        ],
        col_widths=[55, 135]
    )

    subsection(pdf, "Data Flow in Result.jsx (Product Detail Page)")
    code_block(pdf, """User navigates to /result/maggi-masala-noodles
        |
        |-- 1. Check module-level cache (10-min TTL)
        |         L-- Cache hit -> render immediately
        |
        |-- 2. Try axios GET /api/product/search?name=maggi...
        |         L-- Success -> cache result -> render product
        |
        L-- 3. Fallback: Supabase JS direct query on ai_extracted_products
                  (5 strategies: exact -> prefix -> word -> substring -> alphanumeric)
                  L-- Success -> render product with stored classification""")

    para(pdf, "The fallback exists because Render free tier can have cold starts (backend sleeping after 15 min idle). "
              "The frontend retries once with an extended 25s timeout before using the Supabase fallback.")

    subsection(pdf, "Key Frontend Patterns")
    subsubsection(pdf, "Module-Level Cache (Result.jsx)")
    para(pdf, "Product data is cached at module level -- survives component re-mounts, shared across navigations. "
              "Cache has 10-minute TTL to overlap with Render's 15-min idle window.")
    code_block(pdf, """const _productCache = new Map()  // key -> { data, ts }
const CACHE_TTL_MS = 10 * 60 * 1000

function cacheGet(key) {
  const entry = _productCache.get(key)
  if (!entry) return null
  if (Date.now() - entry.ts > CACHE_TTL_MS) { _productCache.delete(key); return null }
  return entry.data
}""")

    subsubsection(pdf, "Render Cold Start Retry")
    code_block(pdf, """try { response = await tryBackend(10000) }
catch (firstErr) {
  if (firstErr.code === 'ECONNABORTED' || firstErr.code === 'ERR_NETWORK') {
    await new Promise(r => setTimeout(r, 2000))
    response = await tryBackend(25000)  // second try with longer timeout
  }
}""")

    subsubsection(pdf, "Client-Side Classification Overrides")
    para(pdf, "Some ingredients stored in Supabase have outdated classifications from old analysis runs. "
              "These are corrected client-side without touching the database:")
    code_block(pdf, """const CLASSIFICATION_OVERRIDES = [
  { pattern: /disodium\\s+5['\\-]?\\s*ribonucleotides/i, classification: 'worth_knowing' },
  { pattern: /tbhq|tertiary\\s+butylhydroquinone/i,      classification: 'commonly_questioned' },
  { pattern: /titanium\\s+dioxide|\\be171\\b/i,           classification: 'commonly_questioned' },
]""")


# ── Section 7: Database ───────────────────────────────────────────────────────

def sec7(pdf):
    section_header(pdf, 7, "Database -- Supabase")

    para(pdf, "Supabase provides a hosted PostgreSQL database with built-in Auth and Storage. "
              "The project uses two Supabase clients with different permission levels.")

    table(pdf,
        ["Client", "Key Used", "Permissions", "Used For"],
        [
            ["supabase",       "anon key",          "Subject to RLS",    "All user-facing reads"],
            ["supabase_admin", "service_role key",  "Bypasses all RLS",  "Admin writes only (server-side)"],
        ],
        col_widths=[35, 40, 40, 75]
    )

    subsection(pdf, "Primary Table: ai_extracted_products")
    para(pdf, "Every product query in the live app hits this table. It is the source of truth.")
    table(pdf,
        ["Column", "Type", "Description"],
        [
            ["id",              "UUID (PK)",    "Auto-generated primary key"],
            ["name",            "TEXT",         "Full product name (e.g. 'Maggi 2-Minute Masala Noodles')"],
            ["brand",           "TEXT",         "Brand name (e.g. 'Nestle')"],
            ["category",        "TEXT",         "Product category (Snacks, Skincare, Beverages, etc.)"],
            ["grade",           "TEXT",         "Computed safety grade: A, B, C, or D"],
            ["ingredients_raw", "TEXT",         "Raw ingredients string as printed on label"],
            ["ingredients",     "JSONB",        "Pre-classified ingredient array (name, classification, notes)"],
            ["image_url",       "TEXT",         "Primary product image URL"],
            ["images",          "TEXT[]",       "Array of additional image URLs"],
            ["static_key",      "TEXT",         "Normalized search slug (e.g. maggi2minutemasalanoodles)"],
            ["summary",         "TEXT",         "AI-generated product summary"],
            ["fssai_note",      "TEXT",         "FSSAI-specific regulatory note"],
            ["data_source",     "TEXT",         "database_verified or community_verified"],
            ["confidence",      "TEXT",         "high (admin-verified) or medium"],
            ["created_at",      "TIMESTAMPTZ",  "Auto-set creation timestamp"],
        ],
        col_widths=[40, 28, 122]
    )

    subsection(pdf, "Other Tables")
    table(pdf,
        ["Table", "Purpose"],
        [
            ["products_catalog",         "Lightweight table for sitemap generation and browse listing"],
            ["product_photos",            "Multiple photos per product (user-uploaded, pending review)"],
            ["product_reviews",           "Star ratings + comments, one per user per product"],
            ["user_profiles",             "One row per user -- email, quiz answers, preferences"],
            ["blogs",                     "Blog posts with pending/approved/rejected status"],
            ["correction_reports",        "User-reported ingredient corrections (pending admin review)"],
            ["search_history",            "Anonymous search log (ip_hash, query, timestamp)"],
        ],
        col_widths=[60, 130]
    )

    subsection(pdf, "Row Level Security (RLS)")
    bullet(pdf, [
        "ai_extracted_products -- anyone can read (SELECT), only admin can write (INSERT/UPDATE)",
        "product_photos -- anyone can read, only admin for all writes",
        "product_reviews -- authenticated users can read/write their own reviews",
        "user_profiles -- users can only see and update their own profile row",
        "blogs -- anyone can read approved posts, authenticated users can insert",
        "All tables have RLS enabled -- no table is left unprotected",
    ])


# ── Section 8: Ingredient Classification ─────────────────────────────────────

def sec8(pdf):
    section_header(pdf, 8, "Ingredient Classification Engine")

    para(pdf, "The heart of the app. Lives in backend/routes/ingredient_database.py (~5,500 lines). "
              "Contains 1,000+ ingredient entries with detailed scientific descriptions.")

    subsection(pdf, "Three Classification Tiers")
    table(pdf,
        ["Tier", "Badge", "Meaning", "Example Ingredients"],
        [
            ["generally_recognised", "Safe (Green)",
             "Approved by FSSAI, WHO, CODEX. No known significant concern at regulated levels.",
             "Water, Salt, Wheat Flour, Turmeric, Aloe Vera"],
            ["worth_knowing", "Worth Knowing (Amber)",
             "Permitted but worth being aware of. May cause sensitivity in some individuals.",
             "MSG, Sugar, Palm Oil, Sucralose, Phenoxyethanol"],
            ["commonly_questioned", "Questioned (Red)",
             "Subject to regulatory bans in some countries, or linked to health concerns.",
             "Tartrazine (E102), Sodium Benzoate, Parabens, TBHQ, Titanium Dioxide"],
        ],
        col_widths=[42, 32, 68, 48]
    )

    subsection(pdf, "How Classification Works")
    para(pdf, "classify_ingredient(ingredient_name) is called for every ingredient in every product:")
    numbered_list(pdf, [
        "Pre-checks -- safe food enzymes (amylase, protease, lipase), safe cosmetic bases",
        "E-number lookup -- e621 -> MSG -> worth_knowing",
        "Pattern matching -- checks against 300+ curated patterns in priority order",
        "INGREDIENT_DESCRIPTIONS lookup -- 1,000+ ingredients with 500-900 char scientific descriptions",
        "Generic category handling -- 'Emulsifiers', 'Stabilizers' etc. -> worth_knowing with undisclosed warning",
        "Default -> generally_recognised",
    ])

    callout(pdf,
        "Undisclosed Ingredient Warning: When a brand writes 'Emulsifiers' or 'Flavourings' without "
        "naming specific compounds, the engine sets a recommendation field: 'Brand has not fully disclosed "
        "this ingredient. Specific compounds cannot be independently assessed -- use with caution, "
        "especially if you have allergies or sensitivities.' This is shown as an amber warning on the product page.",
        label="Undisclosed Ingredient Warning")

    subsection(pdf, "Ingredient Database Entry Format")
    code_block(pdf, """'sorbic acid': {
    'what_it_is':         'Natural preservative, also produced synthetically',
    'commonly_found_in':  'Cheese, baked goods, wine, fruit products',
    'one_line_note':      'GRAS by FDA; approved by FSSAI and EU',
    'regulatory_note':    'Permitted in India (FSSAI), EU (E200), USA (FDA)',
    'classification':     'generally_recognised',
    'health_effects':     'No known adverse effects at regulated levels',
    'countries_restricted': [],
    'fssai_position':     'Permitted preservative',
}

# Entries are indexed by: common name, E-number (e.g. e200),
# INS number, and alternate spellings.
# _normalize_ins() converts "INS 200" -> "E200" for unified lookup.""")

    subsection(pdf, "get_ingredient_details() -- Extended Lookup")
    para(pdf, "Used by the Check Ingredient page. Returns everything above plus:")
    bullet(pdf, [
        "commonly_found_in -- product types where it appears",
        "health_effects -- dict of known health effects",
        "countries_restricted -- list of countries with bans/restrictions",
        "fssai_position -- India-specific regulatory note",
        "related_ingredients -- 6 similar ingredients to explore",
        "recommendation -- caution advice if undisclosed or restricted",
    ])


# ── Section 9: Grading System ─────────────────────────────────────────────────

def sec9(pdf):
    section_header(pdf, 9, "Grading System")

    para(pdf, "Defined in backend/grading.py. Pure Python, no AI, completely deterministic.")

    code_block(pdf, """Input: list of ingredient objects, each with a 'classification' field

Rules (evaluated in order):
  1. ANY 'commonly_questioned' ingredient  --> Grade D
  2. ZERO 'worth_knowing' ingredients      --> Grade A
  3. 'worth_knowing' <= 30% of total       --> Grade B
  4. 'worth_knowing' >  30% of total       --> Grade C""")

    subsection(pdf, "Grade Definitions")
    pdf.ln(2)
    pdf.set_x(10)
    grade_badge_inline(pdf, 'A', "All ingredients generally recognised as safe. Best choice.")
    pdf.set_x(10)
    grade_badge_inline(pdf, 'B', "Mostly clean -- a few worth-knowing additives (<=30%). Good choice.")
    pdf.set_x(10)
    grade_badge_inline(pdf, 'C', "Many worth-knowing additives (>30%). Use with awareness.")
    pdf.set_x(10)
    grade_badge_inline(pdf, 'D', "Contains commonly questioned or restricted ingredients. Reconsider.")
    pdf.ln(2)

    callout(pdf,
        "Important: Grades are computed fresh on every search from the stored ingredient classifications. "
        "Changing classification rules in ingredient_database.py does NOT automatically update stored grades. "
        "You must run reparse_all_products.py to re-grade all 570+ products after changing classification logic.",
        label="Note for Developers", bg=WARN_BG, bd=WARN_BD)


# ── Section 10: Authentication ────────────────────────────────────────────────

def sec10(pdf):
    section_header(pdf, 10, "Authentication")

    para(pdf, "Handled entirely by Supabase Auth (email OTP / magic link + Google OAuth).")

    table(pdf,
        ["Component", "Location", "Responsibility"],
        [
            ["AuthContext.jsx", "frontend/src/context/", "Wraps entire app; provides user, profile, openAuthModal() to all components"],
            ["AuthModal.jsx",   "frontend/src/components/", "Login/signup UI -- multi-step: main -> email -> OTP -> quiz -> done"],
            ["supabaseClient.js","frontend/src/lib/",   "Creates Supabase client; refreshes session on tab visibility change"],
            ["Admin check",     "Admin.jsx",            "user.email === ADMIN_EMAIL (checked in frontend)"],
            ["Admin API auth",  "backend/main.py",      "Backend verifies Supabase JWT and checks email claim from token"],
        ],
        col_widths=[40, 50, 100]
    )

    subsection(pdf, "Auth Flow")
    numbered_list(pdf, [
        "User clicks 'Login' -> AuthModal opens",
        "User enters email -> Supabase sends OTP or magic link",
        "User enters OTP -> Supabase returns JWT + user object",
        "AuthContext stores user, fetches user_profiles row",
        "First login: creates user_profiles row + shows onboarding quiz (5 questions)",
        "JWT is stored in browser localStorage by Supabase client",
        "Admin endpoints: frontend sends Authorization: Bearer {jwt} header",
        "Backend extracts email from JWT claims, checks against ADMIN_EMAIL env var",
    ])

    bullet(pdf, [
        "Google OAuth -- one-click sign-in via Google (also supported)",
        "Session refresh on tab visibility change if away > 4 minutes",
        "Email + Password also supported with show/hide toggle",
    ])


# ── Section 11: Admin Panel ───────────────────────────────────────────────────

def sec11(pdf):
    section_header(pdf, 11, "Admin Panel")

    para(pdf, "Located at /admin. Only accessible to the admin email account (shubhampaliwal5@gmail.com). "
              "Redirects all other users to /.")

    subsection(pdf, "Admin Dashboard Tabs")
    table(pdf,
        ["Tab", "Purpose"],
        [
            ["Pending",   "Review and approve/reject product submissions from users"],
            ["Approved",  "Browse all verified products; edit or delete any product"],
            ["Extracted", "Products from AI extraction pipeline awaiting verification"],
            ["Photos",    "Manage user-submitted product photos (approve/reject)"],
            ["Reports",   "Ingredient correction reports from users (approve updates the live product)"],
            ["Blogs",     "Approve, reject, or delete user blog submissions"],
        ],
        col_widths=[35, 155]
    )

    subsection(pdf, "How Product Extraction Works (Admin Flow)")
    code_block(pdf, """Admin pastes product image URL into Admin dashboard
        |
        L-- POST /api/admin/extract-from-image
                  |
                  L-- Google Gemini 1.5 Flash (Vision API)
                            |
                            L-- Returns ingredient list as structured text
                                      |
                                      L-- Saved to ai_extracted_products table
                                                |
                                                L-- Classification + grade computed
                                                   on next user search request""")

    bullet(pdf, [
        "Bulk regrade button -- recomputes A/B/C/D grades for all products",
        "Manual product entry form with live ingredient classification preview",
        "Edit any product: name, brand, category, image, ingredients",
        "Admin can also approve correction_reports (updates live product data)",
    ])


# ── Section 12: Deployment ────────────────────────────────────────────────────

def sec12(pdf):
    section_header(pdf, 12, "Deployment")

    subsection(pdf, "Frontend -- Vercel")
    bullet(pdf, [
        "Platform: Vercel (free tier)",
        "Framework: Vite (detected automatically)",
        "Build command: npm run build   |   Output directory: dist/",
        "Auto-deploy: Every push to main branch triggers a new deployment",
        "SPA routing: vercel.json rewrites all paths to /index.html",
        "Security headers: X-Frame-Options DENY, X-Content-Type-Options, HSTS, CSP",
        "Cache headers: Static assets (JS/CSS/images) cached 1 year (immutable)",
    ])

    subsection(pdf, "Backend -- Render")
    bullet(pdf, [
        "Platform: Render Web Service (free tier)",
        "Runtime: Python 3.11",
        "Start command: uvicorn main:app --host 0.0.0.0 --port $PORT",
        "Auto-deploy: Every push to main branch",
        "Cold start: Sleeps after 15 min idle. First request takes 5-30s to wake up.",
        "URL: https://checkkaro.onrender.com",
    ])

    subsection(pdf, "Database -- Supabase")
    bullet(pdf, [
        "Platform: Supabase (free tier)",
        "Database: PostgreSQL (managed, always on)",
        "Auth: Built-in (email OTP + Google OAuth)",
        "Storage: S3-compatible file storage for product images",
        "RLS: Row Level Security enabled on all tables",
    ])

    subsection(pdf, "Keep-Alive Strategy")
    table(pdf,
        ["Mechanism", "Interval", "Purpose"],
        [
            ["App.jsx usePrewarm()",  "Every 4 min (while app is open)",
             "Pings /health to prevent Render sleep during active user session"],
            ["UptimeRobot",           "Every 5 min (always)",
             "External monitor -- keeps Render awake 24/7 even when no users are online"],
            ["Frontend retry",        "On first cold-start timeout",
             "Retries request with 25s timeout if initial 10s request times out"],
        ],
        col_widths=[45, 45, 100]
    )

    subsection(pdf, "Git Workflow")
    table(pdf,
        ["Branch", "Purpose"],
        [
            ["main",    "Production. Auto-deploys to Vercel (frontend) and Render (backend). Only merge here after testing."],
            ["testing", "Staging. All changes go here first. Verify before merging to main."],
            ["develop", "Experimental / long-running feature work."],
        ],
        col_widths=[25, 165]
    )

    code_block(pdf, """# 1. Make changes locally
git checkout testing
git add <files>
git commit -m "feat: describe your change"
git push origin testing

# 2. Test on staging (Render preview / testing branch)
# 3. Once confirmed working, merge to main
git checkout main
git merge testing --no-edit
git push origin main
# --> Vercel and Render auto-deploy from main""")


# ── Section 13: Local Setup ───────────────────────────────────────────────────

def sec13(pdf):
    section_header(pdf, 13, "Local Setup Guide")

    subsection(pdf, "Prerequisites")
    bullet(pdf, ["Python 3.11+", "Node.js 18+", "Git"])

    subsection(pdf, "Backend Setup")
    code_block(pdf, """cd checkkaro/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and fill in values (see Environment Variables section)
cp .env.example .env

# Run development server
uvicorn main:app --reload --port 8000
# API runs at http://localhost:8000
# Docs at  http://localhost:8000/docs  (non-production mode only)""")

    subsection(pdf, "Frontend Setup")
    code_block(pdf, """cd checkkaro/frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Set: VITE_API_BASE_URL=http://localhost:8000
# Set: VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY

# Run development server
npm run dev
# App runs at http://localhost:5173""")

    subsection(pdf, "Environment Variables")
    subsubsection(pdf, "Backend  (.env on Render / local .env file)")
    table(pdf,
        ["Variable", "Required", "Description"],
        [
            ["SUPABASE_URL",           "Yes",      "Supabase project URL (https://xxx.supabase.co)"],
            ["SUPABASE_KEY",           "Yes",      "Public anon key -- used for regular DB queries"],
            ["SUPABASE_SERVICE_KEY",   "Yes",      "Service role key -- bypasses RLS for admin writes"],
            ["ADMIN_EMAIL",            "Yes",      "Email of the admin user"],
            ["GEMINI_API_KEY",         "Yes",      "Google Gemini API key for image-based extraction"],
            ["GROQ_API_KEY",           "Optional", "Groq API key for LLaMA-based ingredient analysis"],
            ["ANTHROPIC_API_KEY",      "Optional", "Claude API key for detailed analysis"],
            ["ENV",                    "Optional", "Set to 'production' to disable /docs and /redoc"],
        ],
        col_widths=[55, 22, 113]
    )

    subsubsection(pdf, "Frontend  (.env.local on Vercel / local .env.local file)")
    table(pdf,
        ["Variable", "Required", "Description"],
        [
            ["VITE_SUPABASE_URL",      "Yes",      "Supabase project URL (same as backend)"],
            ["VITE_SUPABASE_ANON_KEY", "Yes",      "Public anon key (safe to expose in frontend code)"],
            ["VITE_API_BASE_URL",      "Optional", "Backend URL. Defaults to https://checkkaro.onrender.com"],
        ],
        col_widths=[55, 22, 113]
    )

    callout(pdf,
        "SECURITY: Never commit .env files to Git. The anon key is SAFE to expose in frontend "
        "(it's public by design, controlled by RLS). The service_role key must NEVER be in frontend "
        "code -- it bypasses all Row Level Security and grants unrestricted database access.",
        label="Security Note", bg=WARN_BG, bd=WARN_BD)


# ── Section 14: Key Concepts ──────────────────────────────────────────────────

def sec14(pdf):
    section_header(pdf, 14, "Key Concepts for New Developers")

    subsubsection(pdf, "static_key vs Product Name")
    para(pdf, "static_key is a normalized slug (e.g. maggi2minutenoodles) used for fast exact-match lookups. "
              "Not all products have one. Products with a static_key are considered 'verified' -- the data_source "
              "field shows 'database_verified'.")

    subsubsection(pdf, "Why Two Supabase Clients?")
    para(pdf, "supabase (anon key) has the same permissions as a logged-out browser user -- safe for reads, "
              "controlled by RLS. supabase_admin (service_role key) bypasses all RLS and is used only for admin "
              "writes. It NEVER reaches the browser -- only backend server code uses it.")

    subsubsection(pdf, "Why Is ingredient_database.py in routes/?")
    para(pdf, "Historical accident during development. It's not a router -- it's a pure data module "
              "(classification engine + description dictionary). Don't move it without updating all imports.")

    subsubsection(pdf, "Why Are There Multiple Product Tables?")
    para(pdf, "ai_extracted_products is the ACTIVE table. products_catalog and products are LEGACY tables "
              "from earlier iterations of the app. All live traffic reads from ai_extracted_products. "
              "Legacy tables are kept for reference only.")

    subsubsection(pdf, "What Is reparse_all_products.py?")
    para(pdf, "A local script (not on the server) that reads all products from ai_extracted_products, "
              "re-classifies every ingredient using the current ingredient_database.py, and writes updated "
              "grades and classified ingredients back to Supabase. Run this after significant changes to "
              "the classification engine.")

    subsubsection(pdf, "The Frontend Fallback")
    para(pdf, "Result.jsx queries Supabase directly if the backend API call fails. This means users still "
              "see product data even when Render is cold-starting. The fallback uses stored ingredients JSON "
              "(pre-classified) so it doesn't need the backend classification engine.")

    subsection(pdf, "SEO Setup")
    bullet(pdf, [
        "Every page uses SEO.jsx (react-helmet-async) for dynamic title, description, OG tags",
        "Canonical URL always uses https://www.parkho.in",
        "JSON-LD structured data: FAQPage (Home), Product (Result), BlogPosting (Blog), CollectionPage",
        "Three sitemaps: sitemap-static.xml (core pages), sitemap-products.xml (dynamic), sitemap-blogs.xml",
        "robots.txt: Allow /, Disallow /admin, Disallow /blog/write",
        "parkho.in -> 308 permanent redirect -> www.parkho.in (handled by Vercel dashboard)",
    ])


# ── Section 15: What NOT to Touch ────────────────────────────────────────────

def sec15(pdf):
    section_header(pdf, 15, "What NOT to Touch")

    callout(pdf,
        "The items below are load-bearing parts of the system. Changing them without understanding "
        "the full impact can break product classification for hundreds of products or expose the database.",
        bg=WARN_BG, bd=WARN_BD)

    table(pdf,
        ["Thing", "Why -- Risk"],
        [
            ["ingredient_database.py classification order",
             "Patterns are checked in priority order. Changing order can mis-classify hundreds of ingredients."],
            ["grading.py grade thresholds",
             "Changing the 30% threshold re-grades all 570+ products. Run reparse_all_products.py after."],
            ["Supabase service_role key",
             "Must ONLY live in backend .env and Render env vars. Never in frontend code -- bypasses all RLS."],
            ["main branch",
             "Direct pushes to main deploy to production instantly. Always use testing branch first."],
            ["_BANNED and _QUESTIONED lists in product_new.py",
             "Drive Grade D assignments. Adding a common ingredient here will downgrade many products."],
            ["vercel.json redirect rules",
             "parkho.in -> www redirect is handled by Vercel dashboard. Do NOT add redirects here."],
        ],
        col_widths=[70, 120]
    )

    subsection(pdf, "Quick Reference -- Important URLs")
    table(pdf,
        ["Resource", "URL"],
        [
            ["Production site",    "https://www.parkho.in"],
            ["Backend API",        "https://checkkaro.onrender.com"],
            ["API docs (dev only)","https://checkkaro.onrender.com/docs"],
            ["Health check",       "https://checkkaro.onrender.com/health"],
            ["Supabase dashboard", "app.supabase.com -> your project"],
            ["Vercel dashboard",   "vercel.com -> parkho project"],
            ["Render dashboard",   "render.com -> checkkaro service"],
            ["Google Search Console", "search.google.com/search-console -> www.parkho.in"],
        ],
        col_widths=[65, 125]
    )

    divider(pdf)
    pdf.ln(3)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(*GRAY_500)
    pdf.set_x(0)
    pdf.cell(210, 6, "Parkho Technical Documentation -- Generated June 2026 -- Internal use only. Do not distribute publicly.", align='C')
    pdf.set_text_color(0, 0, 0)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.set_margins(10, 12, 10)

    cover_page(pdf)
    toc_page(pdf)
    sec1(pdf)
    sec2(pdf)
    sec3(pdf)
    sec4(pdf)
    sec5(pdf)
    sec6(pdf)
    sec7(pdf)
    sec8(pdf)
    sec9(pdf)
    sec10(pdf)
    sec11(pdf)
    sec12(pdf)
    sec13(pdf)
    sec14(pdf)
    sec15(pdf)

    pdf.output(OUT)
    print(f"Done: {OUT}  ({pdf.page} pages)")


if __name__ == "__main__":
    main()
