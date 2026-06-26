"""
Fix Monaco Classic (b24b5aa8) and any other pre-existing product rows
that have stale ingredient classifications from before the _normalize_ins fix.
"""
import sys, os, re, json
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

def parse_ingredients(raw: str):
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(': depth += 1; cur += ch
        elif ch == ')': depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p: parts.append(p)
            cur = ""
        else: cur += ch
    if cur.strip(): parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'
    key = name.lower().strip()
    raw_desc = (INGREDIENT_DESCRIPTIONS.get(key) or
                INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip()))
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {"name": name, "aliases": desc.get('aliases', ''), "classification": cls,
            "one_line_note": desc.get('one_line_note', ''), "regulatory_note": desc.get('regulatory_note', ''),
            "commonly_found_in": desc.get('commonly_found_in'), "health_effects": desc.get('health_effects'),
            "countries_restricted": desc.get('countries_restricted', []),
            "fssai_position": desc.get('fssai_position'), "recommendation": desc.get('recommendation')}

def compute_grade(classified):
    if not classified: return "B"
    total = len(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if q > 0: return "D"
    if w == 0: return "A"
    return "B" if w / total <= 0.30 else "C"

def make_summary(name, brand, grade, q, w, total):
    if grade == "A":
        return f"{name} by {brand} scores Grade A. All {total} ingredients generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about, no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

def reparse_row(row):
    name  = row['name']
    brand = row.get('brand') or ''
    raw   = row.get('ingredients_raw') or ''

    # If no raw string, rebuild from stored ingredients list
    if not raw:
        stored = row.get('ingredients') or []
        if isinstance(stored, str):
            stored = json.loads(stored)
        if stored and isinstance(stored, list) and isinstance(stored[0], dict):
            raw = ', '.join(i.get('name', '') for i in stored)
        else:
            print(f"  [SKIP] no raw or stored ingredients")
            return

    ing_names  = parse_ingredients(raw)
    classified = [classify_one(n) for n in ing_names]
    grade      = compute_grade(classified)
    q = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    w = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    total = len(classified)

    verdict = (f"Contains {q} restricted/flagged ingredient(s)." if q else
               f"Contains {w} ingredient(s) worth monitoring." if w else
               "All ingredients are generally safe.")
    recommendation = ("Avoid or use sparingly — contains commonly questioned ingredients." if q else
                      "Use with awareness — some additives worth monitoring." if w else
                      "Safe to use — no concerning ingredients detected.")
    awareness_score = max(0, 100 - (q * 25) - (w * 8))

    sb.table('ai_extracted_products').update({
        "ingredients":      classified,
        "ingredients_raw":  raw,
        "grade":            grade,
        "summary":          make_summary(name, brand, grade, q, w, total),
        "verdict":          verdict,
        "recommendation":   recommendation,
        "awareness_score":  awareness_score,
    }).eq('id', row['id']).execute()

    print(f"  UPDATED  Grade={grade}  questioned={q}  worth={w}  total={total}")
    for i in classified:
        print(f"    [{i['classification']:25s}] {i['name']}")


# Fix the specific rows identified
TARGET_IDS = [
    'b24b5aa8-a479-427a-8a62-9b03d8fe2a70',  # Monaco Classic - has wrong classifications
    '3dcee136-9f58-49ab-81a6-d624cb2129ea',  # Parle Monaco Salted Biscuits - no raw, Grade C but likely wrong
]

for rid in TARGET_IDS:
    res = sb.table('ai_extracted_products').select(
        'id, name, brand, grade, ingredients_raw, ingredients'
    ).eq('id', rid).execute()
    if not res.data:
        print(f"NOT FOUND: {rid}")
        continue
    row = res.data[0]
    print(f"\n[{row['name']}] (was Grade={row['grade']})")
    reparse_row(row)
