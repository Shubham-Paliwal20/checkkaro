"""
Insert Indian Protein Supplements
Whey, Plant-based, Mass Gainers, and Clinical Nutrition
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['aspartame', 'sucralose', 'acesulfame', 'artificial', 'soy lecithin', 'emulsifier', 'vegetable oil']
_WORTH = ['whey', 'casein', 'plant protein', 'natural', 'stevia', 'bcaa', 'amino acid', 'creatine monohydrate']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'aspartame' in n or 'sucralose' in n: return 'Artificial sweetener; FDA approved'
        if 'soy lecithin' in n: return 'Emulsifier; derived from soy'
        if 'artificial' in n: return 'Artificial ingredient; flavoring agent'
    if cls == 'worth_knowing':
        if 'whey' in n: return 'Whey protein; complete amino acid profile'
        if 'plant' in n or 'pea' in n or 'hemp' in n: return 'Plant-based protein; vegan source'
        if 'bcaa' in n or 'amino acid' in n: return 'Branch-chain amino acids; muscle support'
        if 'creatine' in n: return 'Creatine monohydrate; strength support'
        if 'stevia' in n: return 'Stevia; natural sweetener'
    return 'Protein supplement ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains approved artificial sweeteners; suitable for fitness'
    if cls == 'worth_knowing': return 'Natural ingredients with clinical efficacy; scientifically formulated'
    return 'Dietary supplement ingredient'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 4
        elif ing['classification'] == 'worth_knowing': score -= 1
    return max(0, min(100, score))

PRODUCTS = [
    # WHEY PROTEIN
    {"name": "MuscleBlaze Whey Protein", "brand": "MuscleBlaze", "category": "Protein Supplement",
     "raw": "Whey Protein Concentrate, Whey Protein Isolate, Cocoa Powder, Sugar, Soy Lecithin, Artificial Flavor, Aspartame, Calcium Carbonate.",
     "type": "Whey Protein", "serving": "25g protein per serving"},
    {"name": "Optimum Nutrition Gold Standard Whey", "brand": "Optimum Nutrition", "category": "Protein Supplement",
     "raw": "Whey Protein Isolate, Whey Protein Concentrate, Cocoa Powder, Natural and Artificial Flavor, Cellulose, Sodium Chloride, Sucralose, Lecithin.",
     "type": "Whey Protein", "serving": "24g protein per serving"},
    {"name": "MuscleTech Nitro-Tech Whey", "brand": "MuscleTech", "category": "Protein Supplement",
     "raw": "Whey Protein Isolate, Whey Protein Concentrate, Whey Peptides, Cocoa Powder, Artificial Flavor, Acesulfame Potassium, Sucralose, Lecithin.",
     "type": "Whey Protein", "serving": "30g protein per serving"},
    # PLANT-BASED PROTEIN
    {"name": "MuscleBlaze Plant Protein", "brand": "MuscleBlaze", "category": "Protein Supplement",
     "raw": "Pea Protein Isolate, Brown Rice Protein, Hemp Protein, Cocoa Powder, Natural Flavor, Stevia Extract, Mineral Blend, Vitamin Blend.",
     "type": "Plant-Based Protein", "serving": "23g protein per serving"},
    {"name": "Orgain Organic Protein Powder", "brand": "Orgain", "category": "Protein Supplement",
     "raw": "Organic Pea Protein Isolate, Organic Brown Rice Protein, Organic Hemp Seed Protein, Organic Cocoa, Organic Stevia, Sea Salt, Probiotics.",
     "type": "Plant-Based Protein", "serving": "21g protein per serving"},
    {"name": "GNC Plant Protein", "brand": "GNC", "category": "Protein Supplement",
     "raw": "Pea Protein Isolate, Brown Rice Protein, Quinoa, Hemp Protein, Natural Flavor, Stevia, Guar Gum, Mineral Complex.",
     "type": "Plant-Based Protein", "serving": "20g protein per serving"},
    # MASS GAINERS
    {"name": "MuscleBlaze Mass Gainer XXL", "brand": "MuscleBlaze", "category": "Protein Supplement",
     "raw": "Whey Protein Concentrate, Maltodextrin, Oats, Creatine Monohydrate, Cocoa Powder, Sugar, Soy Lecithin, Artificial Flavor, Aspartame.",
     "type": "Mass Gainer", "serving": "50g protein + 185g carbs"},
    {"name": "MuscleTech Mass-Tech Elite", "brand": "MuscleTech", "category": "Protein Supplement",
     "raw": "Whey Protein Concentrate, Whey Protein Isolate, Maltodextrin, Dextrose, Creatine Monohydrate, Amino Acid Blend, Cocoa Powder, Natural Flavor.",
     "type": "Mass Gainer", "serving": "63g protein + 252g carbs"},
    # CLINICAL & DISEASE-SPECIFIC
    {"name": "Nutricost Diabetic Protein Powder", "brand": "Nutricost", "category": "Protein Supplement",
     "raw": "Whey Protein Concentrate, Whey Protein Isolate, Natural Flavor, Stevia Extract, Chromium Picolinate, Cinnamon Extract, Fenugreek Seed Extract.",
     "type": "Diabetic Nutrition", "serving": "25g protein, 2g carbs"},
    {"name": "Abbott Ensure Plus Nutrition Drink", "brand": "Abbott", "category": "Protein Supplement",
     "raw": "Milk Protein Concentrate, Sugars, Vegetable Oil, Corn Syrup Solids, Minerals, Vitamins, DHA, Vitamin D, Prebiotics.",
     "type": "Clinical Nutrition", "serving": "13g protein per bottle"},
    {"name": "Bajaaj Viva Nutrition Drink", "brand": "Bajaaj", "category": "Protein Supplement",
     "raw": "Milk Protein, Sugar, Vegetable Oil, Corn Syrup, Minerals (Calcium, Iron, Zinc), Vitamins (A, D, B12), Prebiotics.",
     "type": "Clinical Nutrition", "serving": "10g protein per serving"},
    {"name": "Orgain Protein Shake for Recovery", "brand": "Orgain", "category": "Protein Supplement",
     "raw": "Organic Whey Protein Concentrate, Organic Coconut Milk, Organic Stevia, Organic Flavor, Probiotics, Digestive Enzymes, BCAA.",
     "type": "Recovery Protein", "serving": "20g protein + probiotics"},
    {"name": "SCI-MX Nutrition Whey Protein Pro", "brand": "SCI-MX", "category": "Protein Supplement",
     "raw": "Whey Protein Concentrate, Whey Protein Isolate, Cocoa Powder, BCAA Blend, Creatine Monohydrate, Natural Flavor, Stevia, Mineral Blend.",
     "type": "Performance Protein", "serving": "25g protein + BCAA"},
    {"name": "MusclePharm Combat Protein Powder", "brand": "MusclePharm", "category": "Protein Supplement",
     "raw": "Whey Protein Isolate, Whey Protein Concentrate, Whey Peptides, Casein, Egg Albumen, Micellar Casein, Chocolate, Natural Flavor.",
     "type": "Multi-Source Protein", "serving": "24g protein per serving"},
    {"name": "Dymatize ISO-100 Whey Isolate", "brand": "Dymatize", "category": "Protein Supplement",
     "raw": "Whey Protein Isolate, Cocoa Powder, Natural and Artificial Flavor, Vanilla, Sucralose, Acesulfame Potassium, Lecithin.",
     "type": "Whey Isolate", "serving": "25g protein per serving"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p['type']}. {p.get('serving', '')}. Score: {score}/100.",
            'fssai_note': 'Dietary supplement - not intended to diagnose, treat, cure or prevent any disease. Consult healthcare professional.',
            'verdict': 'Comprehensive formula with clinically studied ingredients' if score >= 85 else 'Standard protein supplement formulation',
            'recommendation': 'Mix with milk or water. Take 1-2 servings daily post-workout or with meals. Keep out of reach of children.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Indian Protein Supplements...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
