"""
PDF -> Supabase product importer (pure Python, no AI)
Usage:
  py -3 import_products_from_pdf.py                   # uses CheckKaro_Product_List.pdf
  py -3 import_products_from_pdf.py <folder_or_pdf>   # your own folder/file
"""

import os, sys, re, time
import pdfplumber
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

# ── Category keywords -> standard names ─────────────────────────────────────
CATEGORY_MAP = [
    ('biscuit',           'Biscuits'),
    ('cookie',            'Biscuits'),
    ('instant noodle',    'Instant Noodles'),
    ('noodle',            'Instant Noodles'),
    ('chocolate',         'Chocolate'),
    ('confectionery',     'Confectionery'),
    ('candy',             'Confectionery'),
    ('gum',               'Confectionery'),
    ('health drink',      'Health Drink'),
    ('soft drink',        'Soft Drink'),
    ('cola',              'Soft Drink'),
    ('energy drink',      'Energy Drink'),
    ('fruit drink',       'Fruit Drink'),
    ('fruit juice',       'Fruit Juice'),
    ('tea',               'Beverages'),
    ('coffee',            'Beverages'),
    ('beverage',          'Beverages'),
    ('water',             'Beverages'),
    ('dairy',             'Dairy'),
    ('ice cream',         'Dairy'),
    ('ghee',              'Dairy'),
    ('butter',            'Dairy'),
    ('cheese',            'Dairy'),
    ('milk',              'Dairy'),
    ('cooking oil',       'Cooking Oil'),
    ('edible oil',        'Cooking Oil'),
    ('breakfast cereal',  'Breakfast Cereal'),
    ('cereal',            'Breakfast Cereal'),
    ('oats',              'Breakfast Cereal'),
    ('snack',             'Snacks'),
    ('chips',             'Snacks'),
    ('popcorn',           'Snacks'),
    ('namkeen',           'Snacks'),
    ('spice',             'Spices'),
    ('masala',            'Spices'),
    ('condiment',         'Condiments'),
    ('sauce',             'Condiments'),
    ('pickle',            'Condiments'),
    ('jam',               'Condiments'),
    ('spread',            'Condiments'),
    ('ketchup',           'Condiments'),
    ('ready to eat',      'Ready to Eat'),
    ('supplement',        'Health Supplement'),
    ('protein',           'Health Supplement'),
    ('nutraceutical',     'Health Supplement'),
    ('baby',              'Baby Care'),
    ('infant',            'Baby Care'),
    ('skincare',          'Skincare'),
    ('skin care',         'Skincare'),
    ('sunscreen',         'Skincare'),
    ('moisturiser',       'Skincare'),
    ('moisturizer',       'Skincare'),
    ('face wash',         'Skincare'),
    ('serum',             'Skincare'),
    ('hair care',         'Hair Care'),
    ('haircare',          'Hair Care'),
    ('shampoo',           'Hair Care'),
    ('hair oil',          'Hair Care'),
    ('soap',              'Personal Care'),
    ('handwash',          'Personal Care'),
    ('body wash',         'Personal Care'),
    ('personal care',     'Personal Care'),
    ('deodorant',         'Personal Care'),
    ('cosmetic',          'Cosmetics'),
    ('makeup',            'Cosmetics'),
    ('lipstick',          'Cosmetics'),
    ('foundation',        'Cosmetics'),
    ('oral care',         'Oral Care'),
    ('toothpaste',        'Oral Care'),
    ('mouthwash',         'Oral Care'),
    ('household',         'Household'),
    ('detergent',         'Household'),
    ('dishwash',          'Household'),
    ('flour',             'Food'),
    ('atta',              'Food'),
    ('honey',             'Food'),
    ('sugar',             'Food'),
    ('salt',              'Food'),
]

def guess_category(text: str) -> str | None:
    t = text.lower()
    for key, cat in CATEGORY_MAP:
        if key in t:
            return cat
    return None

def verdict(score: int) -> str:
    if score >= 80: return 'Clean formulation'
    if score >= 60: return 'Average formulation'
    if score >= 40: return 'Worth reviewing'
    return 'Review carefully'

def recommendation(score: int) -> str:
    if score >= 80: return 'Generally suitable for regular use. Check for personal allergies.'
    if score >= 60: return 'Suitable for most people. Some ingredients may warrant attention.'
    if score >= 40: return 'Review ingredient list before regular use, especially for sensitive individuals.'
    return 'Consider checking with a professional before regular use.'

# ── Build a row-number -> category map by scanning all text first ────────────
# This is the key fix: we map each serial-number range to its correct category
# e.g. rows 1-16 -> Biscuits, rows 17-38 -> Snacks, etc.

def build_row_category_map(pdf) -> dict:
    """Returns {row_number: category} for all rows found in text."""
    # First collect (row_num, line) pairs from all pages in order
    all_lines = []
    for page in pdf.pages:
        text = page.extract_text() or ''
        all_lines.extend(text.splitlines())

    row_cat_map = {}          # row_num -> category
    current_cat = 'Food'
    last_header_row = 0       # row number where last category header was seen

    # Category boundaries: list of (start_row, category)
    # We'll fill row_cat_map afterwards
    boundaries = []           # [(start_row_number, category)]

    for line in all_lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a category section header
        # Patterns: "BISCUITS (16 products)", "SNACKS", "PERSONAL CARE"
        is_header = bool(
            re.match(r'^[A-Z][A-Z &/\-]{2,}(?:\s*\(\d+\s*products?\))?$', line)
            and not re.match(r'^\d', line)
        )
        if is_header:
            cat = guess_category(line)
            if cat:
                current_cat = cat
                # The next numeric row starts this category
                boundaries.append((None, cat))  # row number TBD
            continue

        # Check if this is a product row: starts with a number
        m = re.match(r'^(\d+)\s+(.+)', line)
        if m:
            row_num = int(m.group(1))
            # Assign pending boundary the current row number if not yet set
            if boundaries and boundaries[-1][0] is None:
                boundaries[-1] = (row_num, boundaries[-1][1])
            row_cat_map[row_num] = current_cat

    return row_cat_map, boundaries


def category_for_row(row_num: int, row_cat_map: dict, boundaries: list) -> str:
    # Direct lookup first
    if row_num in row_cat_map:
        return row_cat_map[row_num]
    # Fallback: find closest boundary <= row_num
    cat = 'Food'
    for start, c in sorted((b for b in boundaries if b[0] is not None), key=lambda x: x[0]):
        if start <= row_num:
            cat = c
    return cat


# ── Parse PDF ────────────────────────────────────────────────────────────────

def parse_pdf(path: str) -> list:
    products = []

    with pdfplumber.open(path) as pdf:
        row_cat_map, boundaries = build_row_category_map(pdf)

        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if not row:
                        continue
                    cells = [str(c).strip() if c else '' for c in row]

                    # Skip header rows
                    if not cells[0].isdigit():
                        continue

                    row_num = int(cells[0])

                    name      = cells[1].strip() if len(cells) > 1 else ''
                    brand     = cells[2].strip() if len(cells) > 2 else ''
                    score_raw = cells[3].strip() if len(cells) > 3 else cells[-1].strip()

                    if not name or len(name) < 2:
                        continue
                    if name.lower() in ('product name', 'name', 'product'):
                        continue

                    try:
                        score = int(re.sub(r'[^\d]', '', score_raw)) if score_raw else 50
                        score = max(0, min(100, score))
                    except ValueError:
                        score = 50

                    category = category_for_row(row_num, row_cat_map, boundaries)

                    products.append({
                        'row':      row_num,
                        'name':     name,
                        'brand':    brand or name.split()[0],
                        'category': category,
                        'score':    score,
                    })

    # Deduplicate by row number (table rows can appear in multiple extractions)
    seen_rows = set()
    unique = []
    for p in products:
        if p['row'] not in seen_rows:
            seen_rows.add(p['row'])
            unique.append(p)

    return sorted(unique, key=lambda x: x['row'])


# ── Fallback: free-text parser for non-table PDFs ────────────────────────────

def parse_pdf_freetext(path: str) -> list:
    products = []
    current_cat = 'Food'

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ''
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue

                # Category header
                if re.match(r'^[A-Z][A-Z &/\-]{3,}(?:\s*\(\d+\s*products?\))?$', line):
                    cat = guess_category(line)
                    if cat:
                        current_cat = cat
                    continue

                # Product row starting with a number
                m = re.match(r'^(\d+)\s+(.+)', line)
                if not m:
                    continue

                rest = m.group(2).strip()
                # Try to find score at the end (last standalone number)
                sm = re.search(r'\s(\d{1,3})\s*$', rest)
                if sm:
                    score = int(sm.group(1))
                    rest  = rest[:sm.start()].strip()
                else:
                    score = 50

                # Split name and brand: brand is last 1-3 words usually
                words = rest.split()
                if len(words) >= 4:
                    # Try to find repeated brand at end
                    for brand_len in [3, 2, 1]:
                        candidate_brand = ' '.join(words[-brand_len:])
                        if candidate_brand.lower() in rest.lower().replace(candidate_brand.lower(), '', 1):
                            name  = ' '.join(words[:-brand_len]).strip() or rest
                            brand = candidate_brand
                            break
                    else:
                        name  = rest
                        brand = words[0]
                else:
                    name  = rest
                    brand = words[0] if words else ''

                if len(name) >= 2:
                    products.append({'row': int(m.group(1)), 'name': name, 'brand': brand, 'category': current_cat, 'score': score})

    return products


# ── Insert into Supabase ─────────────────────────────────────────────────────

def insert_product(p: dict) -> bool:
    name  = p['name'][:200]
    brand = p['brand'][:100]
    score = p['score']

    try:
        existing = supabase.from_('ai_extracted_products') \
            .select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False

        supabase.from_('ai_extracted_products').insert({
            'name':            name,
            'brand':           brand,
            'category':        p['category'],
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary':         (
                f"{name} by {brand}. Awareness score: {score}/100. "
                "This information is for general awareness based on publicly available data. "
                "Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable FSSAI regulations.',
            'verdict':         verdict(score),
            'recommendation':  recommendation(score),
            'ingredients':     [],
            'ingredients_raw': '',
            'status':          'active',
        }).execute()
        print(f"  + {name} | {brand} | {p['category']} | score {score}")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False


def process_pdf(path: str) -> tuple:
    print(f"\nProcessing: {os.path.basename(path)}")
    products = parse_pdf(path)

    if not products:
        print("  No table products found, trying text parser...")
        products = parse_pdf_freetext(path)

    if not products:
        print("  WARNING: No products extracted")
        return 0, 0

    print(f"  Found {len(products)} products -> inserting into Supabase...")
    inserted = 0
    for p in products:
        if insert_product(p):
            inserted += 1
        time.sleep(0.15)

    return len(products), inserted


def main():
    default_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'CheckKaro_Product_List.pdf'),
        os.path.join(os.path.dirname(__file__), 'CheckKaro_Product_List.pdf'),
    ]

    target = sys.argv[1] if len(sys.argv) >= 2 else next(
        (p for p in default_paths if os.path.isfile(p)), None
    )

    if not target:
        print("Usage: py -3 import_products_from_pdf.py <pdf_file_or_folder>")
        sys.exit(1)

    if os.path.isfile(target):
        pdf_files = [target]
    elif os.path.isdir(target):
        pdf_files = sorted(
            os.path.join(target, f)
            for f in os.listdir(target) if f.lower().endswith('.pdf')
        )
        if not pdf_files:
            print(f"No PDFs found in: {target}")
            sys.exit(1)
    else:
        print(f"Not a valid file or folder: {target}")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s)")

    total_found = total_inserted = 0
    for pdf_path in pdf_files:
        found, inserted = process_pdf(pdf_path)
        total_found    += found
        total_inserted += inserted

    print(f"\n{'='*55}")
    print(f"DONE: {total_inserted} new products added ({total_found} found in PDFs)")
    print(f"{'='*55}")

if __name__ == '__main__':
    main()
