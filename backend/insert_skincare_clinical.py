"""
Insert Cetaphil, Aqualogica, and Derma Touch skincare products from Clinical PDFs
Comprehensive clinical skincare formulations with ingredient analysis
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_BANNED = ['triclosan', 'formaldehyde']
_QUESTIONED = [
    'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles',
    'methylparaben', 'propylparaben', 'butylparaben', 'propylene glycol',
    'alcohol', 'salicylic acid', 'titanium dioxide',
]
_WORTH = ['mineral oil', 'paraffin', 'silicone', 'dimethicone', 'glycolic acid']

def _classify(name: str) -> str:
    n = name.lower()
    for b in _BANNED:
        if b in n: return 'banned'
    for q in _QUESTIONED:
        if q in n: return 'commonly_questioned'
    for w in _WORTH:
        if w in n: return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'banned':
        return 'Banned or restricted ingredient'
    if cls == 'commonly_questioned':
        if 'salicylic acid' in n: return 'BHA exfoliant; can cause irritation in sensitive skin'
        if 'sodium lauryl sulfate' in n or 'sls' in n: return 'Harsh anionic surfactant; stripping'
        if 'paraben' in n: return 'Preservative; controversial but widely used'
        if 'propylene glycol' in n: return 'Humectant; can irritate sensitive individuals'
        if 'alcohol' in n: return 'Drying agent; can strip natural oils'
        return 'Commonly questioned ingredient'
    if cls == 'worth_knowing':
        if 'glycolic acid' in n: return 'AHA exfoliant; gentle but requires sun protection'
        if 'dimethicone' in n or 'silicone' in n: return 'Silicone conditioning; non-biodegradable'
        if 'petrolatum' in n or 'mineral oil' in n: return 'Occlusive moisturizer; petroleum-derived'
        return 'Moderate concern; safe in regulated amounts'
    # generally_recognised
    if 'hyaluronic acid' in n: return 'Hydrating humectant; draws moisture to skin'
    if 'glycerin' in n: return 'Humectant; hydrating and soothing'
    if 'niacinamide' in n: return 'Vitamin B3; brightening and pore-minimizing'
    if 'aloe vera' in n: return 'Soothing and hydrating botanical'
    if 'green tea' in n: return 'Antioxidant-rich; protective'
    if 'vitamin c' in n or 'ascorbic acid' in n: return 'Antioxidant; brightening and protective'
    if 'vitamin e' in n: return 'Antioxidant; protective and conditioning'
    if 'cucumber' in n: return 'Soothing and hydrating'
    if 'papaya' in n or 'papain' in n: return 'Enzyme exfoliant; gentle'
    if 'turmeric' in n: return 'Anti-inflammatory and antioxidant'
    if 'cica' in n or 'centella' in n: return 'Centella asiatica; soothing and protective'
    if 'ceramide' in n: return 'Barrier-repair lipid; essential for skin health'
    if 'caffeine' in n: return 'De-puffing and energizing agent'
    if 'peptide' in n: return 'Collagen-boosting ingredient'
    if 'shea butter' in n: return 'Nourishing natural butter; rich in fatty acids'
    if 'watermelon' in n: return 'Hydrating and antioxidant-rich'
    if 'zinc oxide' in n: return 'Physical UV filter; safe and natural'
    return 'Generally recognised as safe'

def _reg_note(cls: str) -> str:
    if cls == 'banned': return 'Banned in multiple jurisdictions'
    if cls == 'commonly_questioned': return 'Subject to regulatory scrutiny; permitted by FSSAI'
    if cls == 'worth_knowing': return 'Permitted ingredient; use as directed'
    return 'Approved under cosmetic regulations'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    items = [i.strip() for i in raw.split(',')]
    return [i for i in items if len(i) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {
        'name': name,
        'aliases': '',
        'classification': cls,
        'one_line_note': _note(name, cls),
        'regulatory_note': _reg_note(cls),
    }

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        cls = ing['classification']
        if cls == 'banned': score -= 50
        elif cls == 'commonly_questioned': score -= 10
        elif cls == 'worth_knowing': score -= 3
    return max(0, min(100, score))

PRODUCTS = [
    # CETAPHIL ACTIVE RANGE
    {"name": "Cetaphil Gentle Skin Cleanser", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Cetyl Alcohol, Propylene Glycol, Sodium Lauryl Sulfate, Stearyl Alcohol, Methylparaben, Propylparaben, Butylparaben."},
    {"name": "Cetaphil Moisturising Cream", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Glycerin, Petrolatum, Dicaprylyl Ether, Dimethicone, Glyceryl Stearate, Cetyl Alcohol, Helianthus Annuus Seed Oil, PEG-30 Stearate, Tocopheryl Acetate."},
    {"name": "Cetaphil Sun SPF 50+ Light Gel", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Ethylhexyl Methoxycinnamate, Alcohol, C12-15 Alkyl Benzoate, Diethylamino Hydroxybenzoyl Hexyl Benzoate, Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine."},
    {"name": "Cetaphil Oily Skin Cleanser", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Cetyl Alcohol, PEG-7 Glyceryl Cocoate, Sodium Laureth Sulfate, Panthenol, Glycerin, Methylparaben, Propylparaben."},
    {"name": "Cetaphil Daily Facial Moisturizer SPF 15", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Octocrylene, Isopropyl Adipate, Glycerin, Octisalate, Avobenzone, Glyceryl Stearate, PEG-100 Stearate, Methylparaben."},
    {"name": "Cetaphil Hydrating Eye Gel-Cream", "brand": "Cetaphil", "category": "Skincare",
     "raw": "Aqua, Cyclopentasiloxane, Glycerin, Niacinamide, Sodium Hyaluronate, Panthenol, Tocopheryl Acetate."},

    # AQUALOGICA ACTIVE RANGE
    {"name": "Aqualogica Radiance+ Dewy Sunscreen", "brand": "Aqualogica", "category": "Skincare",
     "raw": "Aqua, Suncat MTA, Niacinamide, Watermelon Fruit Extract, Hyaluronic Acid, Glycerin, Aloe Vera Juice, Zinc Oxide."},
    {"name": "Aqualogica Hydrate+ Jello Gel", "brand": "Aqualogica", "category": "Skincare",
     "raw": "Aqua, Coconut Water, Hyaluronic Acid, Glycerin, Glyceryl Glucoside, Ammonium Acryloyldimethyltaurate/VP Copolymer."},
    {"name": "Aqualogica Glow+ Concentrate Face Serum", "brand": "Aqualogica", "category": "Skincare",
     "raw": "Aqua, Vitamin C, Papaya Extract, Hyaluronic Acid, Glycerin, Propylene Glycol, Ethoxydiglycol."},
    {"name": "Aqualogica Detox+ Smoothie Face Wash", "brand": "Aqualogica", "category": "Skincare",
     "raw": "Aqua, Matcha Green Tea, Salicylic Acid, Glycerin, Cocamidopropyl Betaine, Sodium Lauroyl Sarcosinate."},
    {"name": "Aqualogica Radiance+ Plump Lip Mask", "brand": "Aqualogica", "category": "Skincare",
     "raw": "Shea Butter, Watermelon Extract, Hyaluronic Acid, Vitamin E, Castor Oil, Candelilla Wax."},
    {"name": "Aqualogica Illuminate+ Smoothie Body Lotion", "brand": "Aqualogica", "category": "Personal Care",
     "raw": "Aqua, Wild Berry Extract, Alpha Arbutin, Hyaluronic Acid, Glycerin, Shea Butter."},

    # DERMA TOUCH ACTIVE RANGE
    {"name": "Derma Touch Bye Bye Pigmentation Cream", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Aqua, Kojic Acid Dipalmitate, Niacinamide, Alpha Arbutin, Glycolic Acid, Vitamin E, Glycerin, Mulberry Extract."},
    {"name": "Derma Touch Salicylic Acid 2% Face Wash", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Aqua, Salicylic Acid, Allantoin, Aloe Vera Extract, Panthenol, Cocamidopropyl Betaine."},
    {"name": "Derma Touch Under Eye Recovery Serum", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Aqua, Caffeine, Hyaluronic Acid, Peptide Complex, Niacinamide, Cucumber Extract."},
    {"name": "Derma Touch Ceramide Complex Intensive Moisturizer", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Aqua, Ceramide NP, Ceramide AP, Ceramide EOP, Phytosphingosine, Cholesterol, Glycerin."},
    {"name": "Derma Touch 10% Niacinamide Serum", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Aqua, Niacinamide (10%), Zinc PCA (1%), Propanediol, Hyaluronic Acid, Phenoxyethanol."},
    {"name": "Derma Touch Silicone Sunscreen SPF 50", "brand": "Derma Touch", "category": "Skincare",
     "raw": "Cyclopentasiloxane, Zinc Oxide, Titanium Dioxide, Dimethicone Crosspolymer, Vitamin E."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)

    try:
        existing = supabase.from_('ai_extracted_products') \
            .select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False

        supabase.from_('ai_extracted_products').insert({
            'name':            name,
            'brand':           p['brand'],
            'category':        p['category'],
            'image_url':       None,
            'images':          [],
            'awareness_score': score,
            'summary': (
                f"{name} by {p['brand']}. Clinical formulation. "
                f"Awareness score: {score}/100. Not a health assessment or medical advice."
            ),
            'fssai_note':      'Subject to applicable cosmetic regulations.',
            'verdict':         'Clean formulation' if score >= 80 else 'Average formulation' if score >= 60 else 'Review before use',
            'recommendation':  'Suitable for most.' if score >= 80 else 'Test on small area first.' if score >= 60 else 'Consult dermatologist.',
            'ingredients':     ingredient_objs,
            'ingredients_raw': raw,
            'status':          'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Cetaphil, Aqualogica, Derma Touch products...")
    inserted = 0
    for p in PRODUCTS:
        if insert(p):
            inserted += 1
        time.sleep(0.1)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
