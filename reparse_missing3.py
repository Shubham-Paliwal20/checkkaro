"""Fix 3 products that had no ingredients_raw in DB — supply from our catalogue."""
import sys, os, re
sys.path.insert(0, 'backend')
from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

MISSING = [
    ("Cadbury Gems", "Cadbury",
     "Sugar, Cocoa Butter, Skimmed Milk Powder, Cocoa Mass, Lactose, Vegetable Fats (Palm, Shea), "
     "Whey Permeate Powder, Emulsifier (Soy Lecithin), Glucose Syrup, Starch (Rice, Potato, Maize), "
     "Colours (INS 110, INS 124, INS 102, INS 133, INS 132), Glazing Agent (Carnauba Wax, Shellac), Flavour."),
    ("Britannia Good Day Butter Cookies", "Britannia",
     "Refined Wheat Flour (Maida), Sugar, Edible Vegetable Oil (Palm Olein), Liquid Glucose, "
     "Invert Sugar Syrup, Milk Solids, Butter (3%), Salt, Raising Agents (INS 500(ii), INS 503(ii)), "
     "Emulsifier (INS 322), Flavour (Artificial Butter)."),
    ("Tropicana 100% Orange Juice", "PepsiCo",
     "100% Orange Juice from Concentrate (Water, Orange Juice Concentrate), Vitamin C (Ascorbic Acid)."),
]

def parse_ingredients(raw):
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

def classify_one(name):
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
        return f"{name} by {brand} scores Grade A. All {total} ingredients are generally recognised as safe."
    elif grade == "B":
        return f"{name} by {brand} scores Grade B. {total} ingredients analysed; {w} worth knowing about but no restricted additives."
    elif grade == "C":
        return f"{name} by {brand} scores Grade C. Contains {w} worth-knowing ingredients (>30% of total). Use with awareness."
    else:
        return f"{name} by {brand} scores Grade D. Contains {q} commonly questioned ingredient(s) flagged in some countries."

for name, brand, raw in MISSING:
    print(f"\n[{name}]")
    res = sb.table('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
    if not res.data:
        print("  NOT FOUND"); continue

    classified = [classify_one(n) for n in parse_ingredients(raw)]
    grade = compute_grade(classified)
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
        "ingredients_raw":  raw,
        "ingredients":      classified,
        "grade":            grade,
        "summary":          make_summary(name, brand, grade, q, w, total),
        "verdict":          verdict,
        "recommendation":   recommendation,
        "awareness_score":  awareness_score,
    }).eq('id', res.data[0]['id']).execute()

    print(f"  UPDATED  Grade={grade}  questioned={q}  worth={w}  total={total}")

print("\nDone.")
