"""
Fix Amul Ice Cream ingredients: convert ingredients_raw text into
classified ingredient objects that the frontend can display.
"""
import os, re, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

BANNED = [
    'triclosan', 'formaldehyde', 'hydroquinone', 'mercury', 'lead',
    'e128', 'e216', 'e217', 'e240', 'sudan red', 'para red',
    'methylparaben', 'propylparaben', 'butylparaben', 'ethylparaben',
    'sodium nitrite', 'sodium nitrate', 'potassium bromate',
    'azodicarbonamide', 'brominated vegetable oil', 'olestra',
    'asbestos', 'benzene', 'vinyl chloride', 'aflatoxin'
]

QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles',
    'phthalate', 'artificial color', 'artificial colour', 'tartrazine',
    'sunset yellow', 'carmoisine', 'allura red', 'brilliant blue',
    'e102', 'e110', 'e122', 'e124', 'e133',
    'monosodium glutamate', 'msg', 'disodium guanylate', 'disodium inosinate',
    'sodium benzoate', 'potassium sorbate', 'tetrasodium edta',
    'propylene glycol', 'polyethylene glycol', 'titanium dioxide',
    'sucralose', 'acesulfame', 'aspartame',
]

WORTH_KNOWING = [
    'palm oil', 'palmolein', 'vegetable oil', 'edible vegetable fat',
    'sugar', 'glucose syrup', 'high fructose corn syrup',
    'artificial flavor', 'artificial flavour', 'natural flavor', 'nature identical',
    'citric acid', 'emulsifier', 'stabilizer', 'stabiliser',
    'caramel color', 'caramel colour', 'lecithin',
    'e322', 'e471', 'e407', 'e466', 'e412', 'e410', 'e476', 'e162', 'e160',
]


def classify(name: str) -> str:
    n = name.lower()
    for b in BANNED:
        if b in n: return 'banned'
    for q in QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in WORTH_KNOWING:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'


def one_line_note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned':
        return 'Banned/restricted ingredient'
    if cls == 'commonly_questioned':
        if 'sucralose' in n: return 'Artificial sweetener, no sugar but debated long-term effects'
        if 'e110' in n: return 'Sunset Yellow – artificial colour, restricted in EU'
        if 'e122' in n: return 'Carmoisine – artificial colour, restricted in EU'
        if 'e133' in n: return 'Brilliant Blue – artificial colour'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'sugar' in n: return 'Sweetener; high consumption linked to health concerns'
        if 'emulsifier' in n or 'e471' in n: return 'Emulsifier derived from fats, generally safe'
        if 'stabilizer' in n or 'stabiliser' in n: return 'Texture stabilizer, generally recognised as safe'
        if 'e322' in n: return 'Lecithin emulsifier, generally safe'
        if 'vegetable' in n and 'fat' in n: return 'Processed vegetable fat; quality varies by source'
        if 'palm oil' in n: return 'Common edible oil; environmental concerns'
        if 'e407' in n: return 'Carrageenan – seaweed extract stabilizer'
        if 'e466' in n: return 'Carboxymethyl cellulose – thickener'
        if 'e412' in n: return 'Guar gum – natural stabilizer'
        if 'e410' in n: return 'Locust bean gum – natural stabilizer'
        if 'nature identical' in n or 'natural flavour' in n or 'natural flavor' in n:
            return 'Synthetic replica of a natural flavour compound'
        return 'Moderate concern, safe in regulated amounts'
    # generally recognised
    if 'milk solid' in n: return 'Dairy base, source of protein and calcium'
    if 'sugar' in n: return 'Sweetener'
    if 'cocoa' in n: return 'Natural cocoa, source of antioxidants'
    if 'saffron' in n: return 'Natural spice with antioxidant properties'
    if 'honey' in n: return 'Natural sweetener'
    if 'cardamom' in n: return 'Natural spice'
    if 'almond' in n or 'cashew' in n or 'pista' in n or 'pistachio' in n:
        return 'Natural nut, rich in healthy fats and protein'
    if 'mango' in n or 'strawberry' in n or 'litchi' in n or 'fruit' in n:
        return 'Natural fruit or fruit preparation'
    if 'whey protein' in n: return 'Dairy protein concentrate'
    if 'turmeric' in n: return 'Natural spice with anti-inflammatory properties'
    if 'ashwagandha' in n: return 'Adaptogenic herb used in Ayurveda'
    if 'isabgol' in n or 'psyllium' in n: return 'Natural dietary fibre'
    if 'wheat flour' in n or 'wheat' in n: return 'Contains gluten; avoid if gluten intolerant'
    if 'cocoa butter' in n: return 'Natural fat from cocoa beans'
    return 'Generally recognised as safe'


def regulatory_note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned': return 'Banned or restricted in EU and multiple countries'
    if cls == 'commonly_questioned':
        if 'e110' in n: return 'Banned in some EU countries; permitted by FSSAI'
        if 'e122' in n: return 'Restricted in EU; permitted by FSSAI'
        if 'sucralose' in n: return 'Permitted by FSSAI; debated in long-term studies'
        return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing':
        if 'e471' in n: return 'Permitted emulsifier under FSSAI & CODEX'
        if 'e322' in n: return 'Permitted lecithin emulsifier; GRAS status'
        return 'Permitted additive under FSSAI regulations'
    return 'Approved under FSSAI/CODEX standards'


def parse_ingredients(raw: str) -> list:
    """Split ingredient string into individual items."""
    # Normalise separators
    raw = raw.replace('; ', ', ').strip().rstrip('.')

    # Remove parenthetical sub-lists to avoid splitting inside them
    # e.g. "Brownie Pieces (8%) [Wheat Flour, Cocoa Solids, Sugar, Butter]"
    # We want to keep the parent as one ingredient and add sub-items separately
    items = []

    # Split on top-level commas (not inside brackets/parens)
    depth = 0
    current = []
    for ch in raw:
        if ch in '([': depth += 1
        elif ch in ')]': depth -= 1
        if ch == ',' and depth == 0:
            items.append(''.join(current).strip())
            current = []
        else:
            current.append(ch)
    if current:
        items.append(''.join(current).strip())

    # Also handle "Ice Cream: ..." / "Cone: ..." / "Coating: ..." prefixes
    expanded = []
    for item in items:
        # Remove section prefix like "Ice Cream:" "Cone:" "Coating:" "Spray:" "Top:" "Outer Layer:"
        item = re.sub(r'^[A-Za-z\s]+:\s*', '', item).strip()
        if item:
            expanded.append(item)

    return [i for i in expanded if len(i) > 1]


def build_ingredient_obj(raw_name: str) -> dict:
    cls = classify(raw_name)
    return {
        'name': raw_name,
        'aliases': '',
        'classification': cls,
        'one_line_note': one_line_note(raw_name, cls),
        'regulatory_note': regulatory_note(raw_name, cls),
    }


def main():
    # Fetch all Amul Ice Cream products
    result = supabase.from_('ai_extracted_products') \
        .select('id, name, ingredients_raw, ingredients') \
        .eq('brand', 'Amul') \
        .eq('category', 'Dairy') \
        .execute()

    products = result.data or []
    print(f"Found {len(products)} Amul Dairy products to fix")

    updated = 0
    for p in products:
        raw = (p.get('ingredients_raw') or '').strip()
        if not raw:
            print(f"  skip (no raw): {p['name']}")
            continue

        parsed = parse_ingredients(raw)
        if not parsed:
            print(f"  skip (parse fail): {p['name']}")
            continue

        ingredient_objs = [build_ingredient_obj(i) for i in parsed]

        try:
            supabase.from_('ai_extracted_products') \
                .update({'ingredients': ingredient_objs}) \
                .eq('id', p['id']) \
                .execute()
            print(f"  ok ({len(ingredient_objs)} ingredients): {p['name']}")
            updated += 1
        except Exception as e:
            print(f"  ERROR {p['name']}: {e}")

        time.sleep(0.1)

    print(f"\nDone: {updated}/{len(products)} products updated")


if __name__ == '__main__':
    main()
