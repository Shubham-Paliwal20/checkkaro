"""Generate CheckKaro Product List PDF"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

from routes.product_all_data import ALL_PRODUCTS
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = os.path.join(os.path.dirname(__file__), 'CheckKaro_Product_List.pdf')

# Group products by category
CATEGORY_ORDER = [
    "Biscuits", "Snacks", "Instant Noodles", "Chocolate", "Confectionery",
    "Health Drink", "Soft Drink", "Fruit Drink", "Fruit Juice", "Beverages",
    "Energy Drink", "Dairy", "Cooking Oil", "Spices", "Food",
    "Ready to Eat", "Bakery", "Breakfast Cereal", "Condiments", "Nutrition",
    "Health Supplement", "Dessert", "Pickles",
    "Skincare", "Hair Care", "Personal Care", "Oral Care",
    "Cosmetics", "Baby Care", "Household",
]

groups = {}
for key, val in ALL_PRODUCTS.items():
    name, brand, category, score, verdict, _ = val
    groups.setdefault(category, []).append((name, brand, score, verdict))

# Sort each group
for cat in groups:
    groups[cat].sort(key=lambda x: x[0])

# Build PDF
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('title', fontSize=22, fontName='Helvetica-Bold',
    textColor=colors.HexColor('#FF9933'), alignment=TA_CENTER, spaceAfter=4)
subtitle_style = ParagraphStyle('subtitle', fontSize=11, fontName='Helvetica',
    textColor=colors.HexColor('#555555'), alignment=TA_CENTER, spaceAfter=2)
date_style = ParagraphStyle('date', fontSize=9, fontName='Helvetica',
    textColor=colors.HexColor('#888888'), alignment=TA_CENTER, spaceAfter=14)
cat_style = ParagraphStyle('cat', fontSize=13, fontName='Helvetica-Bold',
    textColor=colors.white, alignment=TA_LEFT)
footer_style = ParagraphStyle('footer', fontSize=8, fontName='Helvetica',
    textColor=colors.HexColor('#999999'), alignment=TA_CENTER)

story = []

# Title block
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("CheckKaro", title_style))
story.append(Paragraph("Complete Product Database — 360 Indian Products", subtitle_style))
story.append(Paragraph("Food | Skincare | Haircare | Cosmetics | Personal Care", subtitle_style))
story.append(Paragraph("Generated for internal reference | checkkaro.in", date_style))
story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#FF9933'), spaceAfter=16))

sno = 1
for cat in CATEGORY_ORDER:
    if cat not in groups:
        continue
    products = groups[cat]

    # Category header
    cat_table = Table(
        [[Paragraph(f"  {cat.upper()}  ({len(products)} products)", cat_style)]],
        colWidths=[16.4*cm]
    )
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0D1B2A')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 4))

    # Table headers
    header = [
        Paragraph('<b>#</b>', ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Product Name</b>', ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Brand</b>', ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold', textColor=colors.white)),
        Paragraph('<b>Score</b>', ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold', textColor=colors.white)),
    ]

    rows = [header]
    for i, (name, brand, score, verdict) in enumerate(products):
        score_hex = (
            '#16a34a' if score >= 80 else
            '#ca8a04' if score >= 60 else
            '#ea580c' if score >= 40 else
            '#dc2626'
        )
        rows.append([
            Paragraph(str(sno), ParagraphStyle('cell', fontSize=8, fontName='Helvetica', textColor=colors.HexColor('#888888'))),
            Paragraph(name, ParagraphStyle('cell', fontSize=8.5, fontName='Helvetica')),
            Paragraph(brand, ParagraphStyle('cell', fontSize=8, fontName='Helvetica', textColor=colors.HexColor('#555555'))),
            Paragraph(f'<font color="{score_hex}"><b>{score}</b></font>',
                ParagraphStyle('score', fontSize=9, fontName='Helvetica-Bold', alignment=TA_CENTER)),
        ])
        sno += 1

    tbl = Table(rows, colWidths=[1*cm, 9.5*cm, 3.5*cm, 2.4*cm])
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#138808')),
        ('GRID', (0,0), (-1,-1), 0.25, colors.HexColor('#e5e7eb')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
    ]
    for i in range(1, len(rows)):
        bg = colors.HexColor('#f9fafb') if i % 2 == 1 else colors.white
        style_cmds.append(('BACKGROUND', (0,i), (-1,i), bg))

    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)
    story.append(Spacer(1, 12))

# Footer
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e5e7eb'), spaceBefore=8))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "CheckKaro — Know What's Inside | This list is for internal reference only. "
    "Ingredient data is based on publicly available regulatory information. Not medical advice.",
    footer_style
))

doc.build(story)
print(f"PDF saved: {OUTPUT}")
print(f"Total products: {sno - 1}")
