"""
Recalculate and write grade (A/B/C/D) for every product in ai_extracted_products.
Uses _classify() from product_new.py — single source of truth for classification.
Run: python migrate_grades.py

Priority for ingredient names:
  1. ingredients_raw (raw label text) — most accurate, parsed by _parse_raw
  2. ingredients list of dicts — fallback when raw is absent
  3. ingredients list of plain strings — legacy fallback
"""
import os, sys, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from routes.product_new import _classify, _parse_raw
from grading import calculate_grade

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

BATCH = 100


def get_ingredient_names(ingredients, raw):
    """
    Always prefer ingredients_raw when available — it preserves parentheses
    correctly (e.g. 'Stabilizers (E412, E407, E410)' stays as one item).
    Ingredient dicts/strings were often split at every comma, breaking E-number
    groups into fragments.
    """
    if raw:
        return _parse_raw(raw)

    # No raw text — fall back to stored list
    names = []
    for ing in ingredients:
        if isinstance(ing, dict):
            names.append(ing.get('name', ''))
        else:
            names.append(str(ing))
    return [n for n in names if n]


def migrate():
    offset = 0
    total_updated = 0

    print("Starting grade migration (product_new._classify, raw-first)...")

    while True:
        print(f"  Fetching batch at offset {offset}...")
        resp = supabase.from_('ai_extracted_products') \
            .select('id, name, ingredients, ingredients_raw') \
            .order('id') \
            .range(offset, offset + BATCH - 1) \
            .execute()

        rows = resp.data or []
        if not rows:
            print("  No more rows.")
            break

        for row in rows:
            names = get_ingredient_names(
                row.get('ingredients') or [],
                row.get('ingredients_raw') or '',
            )

            classified = [
                {'name': n, 'classification': _classify(n)}
                for n in names
            ]

            grade = calculate_grade(classified)

            supabase.from_('ai_extracted_products') \
                .update({'grade': grade}) \
                .eq('id', row['id']) \
                .execute()

            total_updated += 1

        print(f"  Updated {offset + 1}–{offset + len(rows)} | latest: {rows[-1]['name'][:40]}")
        offset += len(rows)
        time.sleep(0.1)

        if len(rows) < BATCH:
            break

    print(f"\nDone — {total_updated} products updated.")


if __name__ == '__main__':
    migrate()
