"""
Recalculate and write grade (A/B/C/D) for every product in ai_extracted_products.
Uses _classify() from product_new.py — single source of truth for classification.
Run: python migrate_grades.py
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


def migrate():
    offset = 0
    total_updated = 0

    print("Starting grade migration (using product_new._classify)...")

    while True:
        print(f"  Fetching batch at offset {offset}...")
        resp = supabase.from_('ai_extracted_products') \
            .select('id, name, ingredients, ingredients_raw') \
            .range(offset, offset + BATCH - 1) \
            .execute()

        rows = resp.data or []
        if not rows:
            print("  No more rows.")
            break

        for row in rows:
            ingredients = row.get('ingredients') or []
            raw = row.get('ingredients_raw') or ''

            # Use ingredients_raw when ingredients are plain strings (better parsing)
            if raw and ingredients and isinstance(ingredients[0], str):
                names = _parse_raw(raw)
            else:
                names = []
                for ing in ingredients:
                    if isinstance(ing, dict):
                        names.append(ing.get('name', ''))
                    else:
                        names.append(str(ing))
                names = [n for n in names if n]

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
