"""
Delete community rows (static_key IS NULL) whose name matches a static product.
Run once after migration:  python cleanup_duplicates.py
"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from dotenv import load_dotenv
load_dotenv()
from db.supabase_client import supabase_admin

def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())

# Fetch all static products
print("Fetching static products...")
static = supabase_admin.from_("ai_extracted_products") \
    .select("id, name") \
    .not_.is_("static_key", "null") \
    .limit(2000).execute()
static_norms = {norm(p["name"]) for p in (static.data or [])}
print(f"  {len(static_norms)} static products loaded")

# Fetch all community products (in batches)
print("Fetching community products...")
to_delete = []
offset = 0
while True:
    batch = supabase_admin.from_("ai_extracted_products") \
        .select("id, name") \
        .is_("static_key", "null") \
        .range(offset, offset + 499).execute()
    rows = batch.data or []
    if not rows:
        break
    for p in rows:
        if norm(p["name"]) in static_norms:
            to_delete.append(p["id"])
    offset += 500

print(f"  {len(to_delete)} community duplicates found")

if not to_delete:
    print("Nothing to delete.")
else:
    # Delete in batches of 100
    deleted = 0
    for i in range(0, len(to_delete), 100):
        batch = to_delete[i:i+100]
        supabase_admin.from_("ai_extracted_products") \
            .delete().in_("id", batch).execute()
        deleted += len(batch)
        print(f"  Deleted {deleted}/{len(to_delete)}")
    print(f"\nDone — {deleted} duplicates removed.")
