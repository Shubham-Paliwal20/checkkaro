"""
Insert NIVEA Product Catalogue
Comprehensive skincare and personal care with moisturizing focus
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['paraffin', 'lanolin', 'edta']
_WORTH = ['glycerin', 'vitamin', 'panthenol', 'shea butter', 'dimethicone']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'paraffin' in n: return 'Mineral oil derivative; occlusive'
        if 'lanolin' in n: return 'Wool derivative; potential allergen'
        if 'edta' in n: return 'Chelating agent; environmental concerns'
    if cls == 'worth_knowing':
        if 'glycerin' in n: return 'Humectant; hydrating'
        if 'vitamin' in n: return 'Vitamin additive; nourishing'
        if 'panthenol' in n: return 'Pro-vitamin B5; soothing'
        if 'shea butter' in n: return 'Natural butter; moisturizing'
        if 'dimethicone' in n: return 'Silicone; protective barrier'
    return 'Personal care ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains minerals; permits as approved'
    if cls == 'worth_knowing': return 'Permitted moisturizing ingredient'
    return 'Approved personal care ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 5
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    {"name": "NIVEA Creme (The Iconic Blue Tin)", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Paraffinum Liquidum, Cera Microcristallina, Glycerin, Lanolin Alcohol (Eucerit), Paraffin, Panthenol, Magnesium Sulfate, Decyl Oleate, Octyldodecanol, Aluminum Stearates, Citric Acid, Magnesium Stearate, Limonene, Geraniol, Hydroxycitronellal, Linalool, Citronellol, Benzyl Benzoate, Cinnamyl Alcohol, Parfum."},
    {"name": "NIVEA Soft Light Moisturiser", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Paraffinum Liquidum, Myristyl Alcohol, Butylene Glycol, Alcohol Denat., Stearic Acid, Myristyl Myristate, Cera Microcristallina, Glyceryl Stearate, Hydrogenated Coco-Glycerides, Simmondsia Chinensis Seed Oil, Tocopheryl Acetate, Lanolin Alcohol (Eucerit), Polyglyceryl-2 Caprate, Dimethicone, Sodium Hydroxide, Carbomer, Phenoxyethanol, Linalool, Citronellol, Alpha-Isomethyl Ionone, Benzyl Alcohol, Limonene, Benzyl Salicylate, Parfum."},
    {"name": "NIVEA Men Dark Spot Reduction Cream", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Isopropyl Palmitate, Cetearyl Alcohol, Ethylhexyl Salicylate, Octocrylene, Butyl Methoxydibenzoylmethane, Glyceryl Stearate, Glycyrrhiza Glabra Root Extract (Licorice), Sodium Ascorbyl Phosphate, Tocopheryl Acetate, Dimethicone, Sodium Carbomer, Phenoxyethanol, Ethylhexylglycerin, Trisodium EDTA, Linalool, Limonene, Coumarin, Alpha-Isomethyl Ionone, Parfum."},
    {"name": "NIVEA Sun Protect & Moisture SPF 50+", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Homosalate, Octocrylene, Glycerin, Ethylhexyl Salicylate, Butyl Methoxydibenzoylmethane, Alcohol Denat., Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine, Sodium Phenylbenzimidazole Sulfonate, C12-15 Alkyl Benzoate, Panthenol, Tocopheryl Acetate, VP/Hexadecene Copolymer, Silica Dimethyl Silylate, Tetrasodium Iminodisuccinate, Cellulose Gum, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Xanthan Gum, Sodium Stearoyl Glutamate, Trisodium EDTA, Sodium Chloride, Hydroxyacetophenone, Ethylhexylglycerin, Citral, Linalool, Limonene, Benzyl Alcohol, Alpha-Isomethyl Ionone, Citronellol, Parfum."},
    {"name": "NIVEA Milk Delights Fine Gramflour Face Wash", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Myristic Acid, Palmitic Acid, Stearic Acid, Potassium Hydroxide, Lauric Acid, Glyceryl Stearate, PEG-8, Cera Alba, Cicer Arietinum Seed Extract (Gramflour), Sine Adipe Lac (Milk), Saffron Extract, Acrylates Copolymer, Sodium Methyl Cocoyl Taurate, Trisodium EDTA, Phenoxyethanol, Ethylhexylglycerin, Linalool, Benzyl Alcohol, Parfum."},
    {"name": "NIVEA Body Lotion Shea Smooth", "brand": "NIVEA", "category": "Personal Care",
     "raw": "Aqua, Glycerin, Cetearyl Alcohol, C15-19 Alkane, Isopropyl Palmitate, Paraffinum Liquidum, Glyceryl Stearate SE, Butyrospermum Parkii Butter (Shea Butter), Dimethicone, Glyceryl Glucoside, Sodium Cetearyl Sulfate, Sodium Carbomer, Phenoxyethanol, Ethylhexylglycerin, Linalool, Limonene, Benzyl Alcohol, Citronellol, Parfum."},
]

def insert(p: dict) -> bool:
    name = p['name']
    raw = p['raw']
    parsed = _parse(raw)
    ingredient_objs = [_build_obj(i) for i in parsed]
    score = _score(ingredient_objs)
    try:
        existing = supabase.from_('ai_extracted_products').select('id').ilike('name', name).limit(1).execute()
        if existing.data:
            print(f"  skip (exists): {name}")
            return False
        supabase.from_('ai_extracted_products').insert({
            'name': name, 'brand': p['brand'], 'category': p['category'], 'image_url': None, 'images': [],
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. Personal care product. Score: {score}/100. Trusted brand formula.",
            'fssai_note': 'Personal care product with moisturizing formulation.',
            'verdict': 'Premium personal care' if score >= 80 else 'Standard formulation',
            'recommendation': 'Suitable for all skin types. Apply daily for best results.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} NIVEA products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
