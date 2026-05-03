"""
Backfill grade column for all rows in ai_extracted_products.
Run once after adding the grade column in Supabase:
  python backfill_grades.py
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from db.supabase_client import supabase_admin
from routes.product_new import _classify, _parse_raw
from grading import calculate_grade

def compute_grade(row: dict) -> str:
    raw = row.get("ingredients_raw") or ""
    if raw:
        names = _parse_raw(raw)
        classified = [{"name": n, "classification": _classify(n)} for n in names if n]
        return calculate_grade(classified) if classified else "C"
    ings = row.get("ingredients") or []
    if ings:
        classified = []
        for ing in ings:
            name = ing.get("name", "") if isinstance(ing, dict) else str(ing)
            if name:
                classified.append({"name": name, "classification": _classify(name)})
        return calculate_grade(classified) if classified else "C"
    return "C"

BATCH = 200
offset = 0
total_updated = 0

print("Fetching all rows to backfill grades...")

while True:
    result = supabase_admin.from_("ai_extracted_products") \
        .select("id, ingredients_raw, ingredients") \
        .range(offset, offset + BATCH - 1) \
        .execute()

    rows = result.data or []
    if not rows:
        break

    updates = [{"id": r["id"], "grade": compute_grade(r)} for r in rows]

    for upd in updates:
        supabase_admin.from_("ai_extracted_products") \
            .update({"grade": upd["grade"]}) \
            .eq("id", upd["id"]) \
            .execute()

    total_updated += len(rows)
    print(f"  Updated {total_updated} rows...")
    offset += BATCH
    time.sleep(0.2)

print(f"\nDone — {total_updated} rows backfilled.")
