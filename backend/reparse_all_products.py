"""
Re-parse all products in the database using the updated _parse_raw that expands
grouped additive declarations like:
  "raising agents (INS 503(ii), INS 500(ii))" → individual classified ingredients

Run from the backend/ directory:
  python reparse_all_products.py
"""
import sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, '.')

from routes.product_new import _parse_raw, _build_ingredient_item
from grading import calculate_grade
from db.supabase_client import supabase_admin

BATCH = 50   # rows per page
updated = 0
skipped = 0
errors  = 0

print("Fetching products with ingredients_raw...")

offset = 0
while True:
    result = supabase_admin.from_("ai_extracted_products") \
        .select("id, name, category, ingredients_raw, ingredients, grade") \
        .not_.is_("ingredients_raw", "null") \
        .neq("ingredients_raw", "") \
        .range(offset, offset + BATCH - 1) \
        .execute()

    rows = result.data or []
    if not rows:
        break

    for p in rows:
        try:
            raw  = (p.get("ingredients_raw") or "").strip()
            cat  = p.get("category") or ""
            pid  = p["id"]
            name = p.get("name", "")

            if not raw:
                skipped += 1
                continue

            # Re-parse with new grouped-expansion logic
            names = _parse_raw(raw)
            if not names:
                skipped += 1
                continue

            # Re-classify every ingredient
            fresh = [_build_ingredient_item(n, cat) for n in names]
            fresh_dicts = [i.dict() for i in fresh]
            new_grade   = calculate_grade(fresh_dicts)

            # Compare with stored to see if anything changed
            # Guard: stored ingredients may be strings (old format) or dicts
            stored_ings  = p.get("ingredients") or []
            stored_names = set()
            for i in stored_ings:
                if isinstance(i, dict):
                    stored_names.add((i.get("name") or "").strip())
                elif isinstance(i, str):
                    stored_names.add(i.strip())
            fresh_names  = {(i.name or "").strip() for i in fresh}

            grade_changed = new_grade != p.get("grade")
            ings_changed  = stored_names != fresh_names

            # Detect stale classifications — any ingredient whose stored classification
            # differs from the freshly computed one (e.g. after ingredient_database.py update)
            cls_changed = False
            if not ings_changed and stored_ings:
                stored_cls_map = {
                    (i.get("name") or "").strip(): i.get("classification", "")
                    for i in stored_ings if isinstance(i, dict)
                }
                cls_changed = any(
                    stored_cls_map.get((fi.name or "").strip(), fi.classification) != fi.classification
                    for fi in fresh
                )

            if not grade_changed and not ings_changed and not cls_changed:
                skipped += 1
                continue

            payload = {"ingredients": fresh_dicts}
            if grade_changed:
                payload["grade"] = new_grade

            supabase_admin.from_("ai_extracted_products") \
                .update(payload).eq("id", pid).execute()

            updated += 1
            label = f"[{updated}] {name[:50]}"
            reason = []
            if grade_changed:  reason.append(f"grade {p.get('grade')}→{new_grade}")
            if ings_changed:   reason.append("ingredients changed")
            if cls_changed:    reason.append("classifications updated")
            print(f"  UPDATED {label}  ({', '.join(reason)})  ({len(fresh)} ingredients)")

        except Exception as e:
            errors += 1
            print(f"  ERROR id={p.get('id')}: {e}")

    offset += BATCH
    if len(rows) < BATCH:
        break

    time.sleep(0.3)   # stay within Supabase rate limits

print(f"\nDone — updated: {updated}, skipped (no change): {skipped}, errors: {errors}")
