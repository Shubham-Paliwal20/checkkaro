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

# Classification keywords (from product_final.py)
BANNED_INGREDIENTS = [
    'triclosan', 'formaldehyde', 'hydroquinone', 'mercury', 'lead',
    'e128', 'e216', 'e217', 'e240', 'sudan red', 'para red',
    'methylparaben', 'propylparaben', 'butylparaben', 'ethylparaben',
    'bha', 'bht', 'sodium nitrite', 'sodium nitrate', 'potassium bromate',
    'azodicarbonamide', 'brominated vegetable oil', 'olestra',
    'asbestos', 'benzene', 'vinyl chloride', 'aflatoxin'
]

COMMONLY_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles',
    'phthalate', 'diethyl phthalate', 'dibutyl phthalate',
    'artificial color', 'artificial colour', 'tartrazine', 'sunset yellow',
    'carmoisine', 'allura red', 'brilliant blue', 'e102', 'e110', 'e122', 'e124', 'e133',
    'monosodium glutamate', 'msg', 'disodium guanylate', 'disodium inosinate',
    'sodium benzoate', 'potassium sorbate', 'tetrasodium edta',
    'propylene glycol', 'polyethylene glycol', 'peg-', 'fragrance', 'parfum',
    'titanium dioxide', 'aluminum', 'aluminium'
]

WORTH_KNOWING = [
    'palm oil', 'palmolein', 'vegetable oil', 'edible vegetable oil',
    'sugar', 'glucose syrup', 'high fructose corn syrup', 'corn syrup',
    'artificial flavor', 'artificial flavour', 'natural flavor', 'natural flavour',
    'citric acid', 'ascorbic acid', 'sodium chloride', 'salt',
    'emulsifier', 'stabilizer', 'thickener', 'preservative',
    'caramel color', 'caramel colour', 'lecithin', 'soy lecithin'
]

def classify_ingredient(ingredient_name: str) -> str:
    """Classify ingredient based on keywords"""
    name_lower = ingredient_name.lower()

    for banned in BANNED_INGREDIENTS:
        if banned in name_lower:
            return "banned"

    for questioned in COMMONLY_QUESTIONED:
        if questioned in name_lower:
            return "commonly_questioned"

    for worth in WORTH_KNOWING:
        if worth in name_lower:
            return "worth_knowing"

    return "generally_recognised"

def migrate():
    offset = 0
    total_updated = 0

    print("Starting grade migration...")

    while True:
        print(f"  Fetching batch starting at offset {offset}...")
        resp = supabase.from_('ai_extracted_products') \
            .select('id, name, ingredients') \
            .range(offset, offset + BATCH - 1) \
            .execute()

        rows = resp.data or []
        if not rows:
            print("  No more rows to process.")
            break

        for row in rows:
            ingredients = row.get('ingredients') or []
            # Classify each ingredient (handle both string and dict formats)
            classified_ingredients = []
            for ing in ingredients:
                if isinstance(ing, dict):
                    ing_name = ing.get('name', '')
                else:
                    ing_name = str(ing)

                classified_ingredients.append({
                    'name': ing_name,
                    'classification': classify_ingredient(ing_name)
                })

            grade = calculate_grade(classified_ingredients)

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
