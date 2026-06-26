"""
Re-parse and update ingredient classifications for all 41 products.
The _normalize_ins() fix now correctly handles prefixed names like
'Raising Agent 503(ii)', 'Emulsifier 322', 'Dough Conditioner (223)'.
This script re-computes grade, ingredients JSON, verdict, recommendation,
awareness_score, and summary for every product we inserted.
"""
import sys, os, re
sys.path.insert(0, 'backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')
from supabase import create_client
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

SUPABASE_URL = os.environ['SUPABASE_URL']
SERVICE_KEY  = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(SUPABASE_URL, SERVICE_KEY)

# ── helpers (same as add_new_products.py) ────────────────────────────────────

def parse_ingredients(raw: str):
    parts, depth, cur = [], 0, ""
    for ch in raw:
        if ch == '(':
            depth += 1; cur += ch
        elif ch == ')':
            depth -= 1; cur += ch
        elif ch == ',' and depth == 0:
            p = cur.strip().rstrip('.')
            if p:
                parts.append(p)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip().rstrip('.'))
    return parts

def classify_one(name: str) -> dict:
    try:
        cls = classify_ingredient(name)
        if not isinstance(cls, str):
            cls = cls.get('classification', 'generally_recognised')
    except Exception:
        cls = 'generally_recognised'

    key = name.lower().strip()
    raw_desc = (
        INGREDIENT_DESCRIPTIONS.get(key) or
        INGREDIENT_DESCRIPTIONS.get(re.sub(r'\s*\(.*?\)', '', key).strip())
    )
    desc = raw_desc if isinstance(raw_desc, dict) else {}
    return {
        "name": name,
        "aliases": desc.get('aliases', ''),
        "classification": cls,
        "one_line_note": desc.get('one_line_note', ''),
        "regulatory_note": desc.get('regulatory_note', ''),
        "commonly_found_in": desc.get('commonly_found_in'),
        "health_effects": desc.get('health_effects'),
        "countries_restricted": desc.get('countries_restricted', []),
        "fssai_position": desc.get('fssai_position'),
        "recommendation": desc.get('recommendation'),
    }

def compute_grade(classified: list) -> str:
    if not classified:
        return "B"
    total = len(classified)
    questioned = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    worth      = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    if questioned > 0:
        return "D"
    if worth == 0:
        return "A"
    return "B" if worth / total <= 0.30 else "C"

def make_summary(name, brand, grade, questioned, worth, total) -> str:
    if grade == "A":
        return (f"{name} by {brand} scores Grade A. All {total} ingredients are "
                f"generally recognised as safe with no concerning additives detected.")
    elif grade == "B":
        return (f"{name} by {brand} scores Grade B. {total} ingredients analysed; "
                f"{worth} are worth knowing about but no restricted additives found.")
    elif grade == "C":
        return (f"{name} by {brand} scores Grade C. Contains {worth} worth-knowing "
                f"ingredients (>30% of total). Use with awareness.")
    else:
        return (f"{name} by {brand} scores Grade D. Contains {questioned} "
                f"commonly questioned ingredient(s) that are restricted or flagged in some countries.")

# ── product names to reparse (all 41 from our insert) ────────────────────────

PRODUCT_NAMES = [
    "Nestle KitKat 4 Finger", "Nestle Munch", "Nestle Milkybar", "Cadbury Gems",
    "Parle Monaco Classic", "Parle Krackjack", "Britannia Marie Gold",
    "Britannia Good Day Butter Cookies", "Tropicana 100% Orange Juice",
    "Paper Boat Frooti Mango Drink", "Minute Maid Pulpy Orange",
    "Red Bull Energy Drink", "Sting Energy Drink Berry Blast",
    "Quaker Oats Original", "Kellogg's Corn Flakes", "Kellogg's Chocos",
    "Sunfeast Yippee Magic Masala Noodles", "Knorr Classic Tomato Soup",
    "Kissan Mixed Fruit Jam", "Yoga Bar Oats And Berries Bar",
    "Too Yumm Multigrain Chips",
    "Himalaya Nourishing Skin Cream", "Himalaya Aloe Vera Face Wash",
    "Himalaya Anti-Dandruff Shampoo", "St. Ives Apricot Scrub",
    "Re'equil Oxi-Moist Moisturizer SPF 15", "Fixderma Shadow SPF 30 Sunscreen",
    "Pilgrim Salicylic Acid Face Wash", "Pilgrim Red Vine Anti-Aging Serum",
    "The Derma Co 1% Hyaluronic Acid Serum", "The Derma Co 0.3% Retinol Night Serum",
    "Kama Ayurveda Kumkumadi Oil", "Beardo Beard Growth Oil",
    "Mars by GHC 5% Minoxidil Hair Serum", "Plum Green Tea Pore-Cleansing Face Wash",
    "Aqualogica Glow+ Dewy Sunscreen SPF 50", "Fixderma Shadow SPF 50+ Sunscreen Gel",
    "Wild Stone Ultra Sensual Body Spray", "Fogg Xpression Deodorant For Men",
    "Engage W1 Perfume Spray For Women", "Sugar Cosmetics Aquaholic Sunscreen",
]

def reparse_product(row: dict) -> bool:
    name    = row['name']
    brand   = row.get('brand', '')
    raw     = row.get('ingredients_raw', '')

    if not raw:
        print(f"  [SKIP] no ingredients_raw")
        return False

    ing_names  = parse_ingredients(raw)
    classified = [classify_one(n) for n in ing_names]
    grade      = compute_grade(classified)
    questioned = sum(1 for i in classified if i['classification'] == 'commonly_questioned')
    worth      = sum(1 for i in classified if i['classification'] == 'worth_knowing')
    total      = len(classified)

    summary        = make_summary(name, brand, grade, questioned, worth, total)
    verdict        = (
        f"Contains {questioned} restricted/flagged ingredient(s)." if questioned else
        f"Contains {worth} ingredient(s) worth monitoring." if worth else
        "All ingredients are generally safe."
    )
    recommendation = (
        "Avoid or use sparingly — contains commonly questioned ingredients." if questioned else
        "Use with awareness — some additives worth monitoring." if worth else
        "Safe to use — no concerning ingredients detected."
    )
    awareness_score = max(0, 100 - (questioned * 25) - (worth * 8))

    update = {
        "ingredients":      classified,
        "grade":            grade,
        "summary":          summary,
        "verdict":          verdict,
        "recommendation":   recommendation,
        "awareness_score":  awareness_score,
    }

    sb.table('ai_extracted_products').update(update).eq('id', row['id']).execute()
    print(f"  Grade={grade}  questioned={questioned}  worth={worth}  total={total}")
    return True


def main():
    updated = skipped = not_found = 0

    for name in PRODUCT_NAMES:
        print(f"\n[{name}]")
        res = sb.table('ai_extracted_products').select(
            'id, name, brand, ingredients_raw'
        ).ilike('name', name).limit(1).execute()

        if not res.data:
            print(f"  NOT FOUND in DB")
            not_found += 1
            continue

        ok = reparse_product(res.data[0])
        if ok:
            updated += 1
        else:
            skipped += 1

    print(f"\n{'='*55}")
    print(f"Done.  Updated: {updated}  |  Skipped: {skipped}  |  Not found: {not_found}")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
