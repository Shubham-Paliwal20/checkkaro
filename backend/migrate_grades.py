"""
Recalculate and write grade (A/B/C/D) for every product in ai_extracted_products.
Run once after adding the grade column:
  python migrate_grades.py
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv
from grading import calculate_grade

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

BATCH = 100

def migrate():
    offset = 0
    total_updated = 0

    while True:
        resp = supabase.from_('ai_extracted_products') \
            .select('id, name, ingredients') \
            .range(offset, offset + BATCH - 1) \
            .execute()

        rows = resp.data or []
        if not rows:
            break

        for row in rows:
            ingredients = row.get('ingredients') or []
            grade = calculate_grade(ingredients)

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
