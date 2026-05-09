"""
Recompute and sync grades for every product in ai_extracted_products.
Run locally:  python backfill_grades.py
Or call the  POST /api/admin/regrade-all  endpoint from the Admin page.
"""
import os, sys, time
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from db.supabase_client import supabase_admin
from routes.product_new import _classify, _parse_raw
from grading import calculate_grade

def compute_grade(row: dict) -> str:
    cat = row.get("category") or ""
    raw = row.get("ingredients_raw") or ""
    if raw:
        names = _parse_raw(raw)
        classified = [{"name": n, "classification": _classify(n, cat)} for n in names if n]
        return calculate_grade(classified) if classified else "C"
    ings = row.get("ingredients") or []
    if ings:
        classified = []
        for ing in ings:
            name = ing.get("name", "") if isinstance(ing, dict) else str(ing)
            if name:
                classified.append({"name": name, "classification": _classify(name, cat)})
        return calculate_grade(classified) if classified else "C"
    return "C"

BATCH = 200

def run_backfill(log=print):
    offset = 0
    total_updated = 0
    changed = 0

    log("Fetching all rows to recompute grades...")

    while True:
        result = supabase_admin.from_("ai_extracted_products") \
            .select("id, category, ingredients_raw, ingredients, grade") \
            .range(offset, offset + BATCH - 1) \
            .execute()

        rows = result.data or []
        if not rows:
            break

        for r in rows:
            new_grade = compute_grade(r)
            total_updated += 1
            if new_grade != r.get("grade"):
                supabase_admin.from_("ai_extracted_products") \
                    .update({"grade": new_grade}) \
                    .eq("id", r["id"]) \
                    .execute()
                changed += 1

        log(f"  Processed {total_updated} rows ({changed} updated)...")
        offset += BATCH
        time.sleep(0.1)

    log(f"\nDone — {total_updated} rows processed, {changed} grades updated.")
    return {"processed": total_updated, "updated": changed}

if __name__ == "__main__":
    run_backfill()
