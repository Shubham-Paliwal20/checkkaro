"""
Insert Himalaya Wellness Company Products
Pharmaceutical, OTC, and Personal Care Products
"""
import os, time
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

_QUESTIONED = ['sodium laureth sulfate', 'synthetic', 'phenoxyethanol', 'color', 'edta', 'talc']
_WORTH = ['neem', 'turmeric', 'aloe vera', 'tea tree', 'herbal', 'ayurvedic', 'bhringaraja', 'natural']

def _classify(name: str) -> str:
    n = name.lower()
    if any(q in n for q in _QUESTIONED): return 'commonly_questioned'
    if any(w in n for w in _WORTH): return 'worth_knowing'
    return 'generally_recognised'

def _note(name: str, cls: str) -> str:
    n = name.lower()
    if cls == 'commonly_questioned':
        if 'sodium laureth sulfate' in n: return 'Surfactant; cleansing agent'
        if 'talc' in n: return 'Talc powder; mineral-based absorbent'
        if 'phenoxyethanol' in n: return 'Preservative; antimicrobial agent'
        if 'edta' in n: return 'Chelating agent; helps formulation stability'
        if 'synthetic' in n or 'color' in n: return 'Synthetic color/additive; permitted'
    if cls == 'worth_knowing':
        if 'neem' in n: return 'Neem; antibacterial and traditional remedy'
        if 'turmeric' in n: return 'Turmeric; anti-inflammatory spice'
        if 'aloe' in n: return 'Aloe vera; soothing botanical'
        if 'tea tree' in n: return 'Tea tree oil; antimicrobial properties'
        if 'herbal' in n or 'ayurvedic' in n: return 'Herbal/Ayurvedic formulation'
        if 'bhringaraja' in n: return 'Bhringaraja; traditional hair care herb'
    return 'Himalaya product ingredient'

def _reg_note(cls: str) -> str:
    if cls == 'commonly_questioned': return 'Contains synthetic ingredients; FDA/FSSAI approved'
    if cls == 'worth_knowing': return 'Ayurvedic/herbal formulation; traditional ingredients'
    return 'Himalaya wellness product'

def _parse(raw: str) -> list:
    raw = raw.strip().rstrip('.')
    return [i.strip() for i in raw.split(',') if len(i.strip()) > 2]

def _build_obj(name: str) -> dict:
    cls = _classify(name)
    return {'name': name, 'aliases': '', 'classification': cls, 'one_line_note': _note(name, cls), 'regulatory_note': _reg_note(cls)}

def _score(ingredient_objs: list) -> int:
    score = 100
    for ing in ingredient_objs:
        if ing['classification'] == 'commonly_questioned': score -= 3
        elif ing['classification'] == 'worth_knowing': score -= 2
    return max(0, min(100, score))

PRODUCTS = [
    # PHARMACEUTICAL/OTC
    {"name": "Liv.52 Tablets", "brand": "Himalaya Wellness", "category": "Pharmaceutical/OTC",
     "raw": "Himsra (Capparis spinosa) 65mg, Kasani (Cichorium intybus) 65mg, Mandur bhasma 33mg, Kakamachi (Solanum nigrum) 32mg, Arjuna (Terminalia arjuna) 32mg, Kasamarda (Cassia occidentalis) 16mg, Biranjasipha (Achillea millefolium) 16mg, Jhavuka (Tamarix gallica) 16mg.",
     "type": "Hepatoprotective"},
    {"name": "Septilin Tablets", "brand": "Himalaya Wellness", "category": "Pharmaceutical/OTC",
     "raw": "Guggulu (Balsamodendron mukul) 0.324g, Shankh bhasma 64mg, Maharasnadi quath 130mg, Guduchi (Tinospora cordifolia) 98mg, Manjishtha (Rubia cordifolia) 64mg, Amalaki (Emblica officinalis) 32mg, Shigru (Moringa pterygosperma) 32mg, Yashti-madhu (Glycyrrhiza glabra) 12mg.",
     "type": "Immune booster"},
    {"name": "Cystone Tablets", "brand": "Himalaya Wellness", "category": "Pharmaceutical/OTC",
     "raw": "Shilapushpa (Didymocarpus pedicellata) 130mg, Pasanabheda (Saxifraga ligulata) 98mg, Manjishtha (Rubia cordifolia) 32mg, Nagarmusta (Cyperus scariosus) 32mg, Apamarga (Achyranthes aspera) 32mg, Gojiha (Onosma bracteatum) 32mg, Sahadevi (Vernonia cinerea) 32mg, Hajrul yahood bhasma 32mg, Shilajeet (Purified) 26mg.",
     "type": "Anti-urolithiatic"},
    {"name": "Himalaya Gasex Tablets", "brand": "Himalaya Wellness", "category": "Pharmaceutical/OTC",
     "raw": "Prativisha (Aconitum palmatum) 65mg, Cowrie Bhasma 32mg, Shankh Bhasma 32mg, Vidanga (Emblica ribes) 32mg, Maricha (Piper nigrum) 32mg, Triphala 32mg, Ginger (Zingiber officinale) 32mg.",
     "type": "Digestive stimulant"},
    # PERSONAL CARE
    {"name": "Purifying Neem Face Wash", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Aqua, Ammonium Lauryl Sulfate, Melia Azadirachta (Neem) Leaf Extract, Cocamidopropyl Betaine, Sodium Cocoyl Glycinate, Glycerin, Acrylates/C10-30 Alkyl Acrylate Crosspolymer, Phenoxyethanol, Fragrance, Curcuma Longa (Turmeric) Root Extract, Sodium Hydroxide, Butylphenyl Methylpropional, Disodium EDTA, Citric Acid, CI 19140, CI 42090.",
     "type": "Face Wash"},
    {"name": "Anti-Hair Fall Shampoo", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Dimethiconol, Glycol Distearate, Fragrance, Glycerin, Sodium Chloride, Butea Monosperma (Palasha) Flower Extract, Eclipta Prostrata (Bhringaraja) Extract, Guar Hydroxypropyltrimonium Chloride, Salicylic Acid, Sodium Benzoate, TEA-Dodecylbenzenesulfonate, Sodium Hydroxide.",
     "type": "Shampoo"},
    {"name": "Herbals Anti-Dandruff Shampoo", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Aqua, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Dimethiconol, Glycol Distearate, Tea Tree Oil, Rosmarinus Officinalis (Rosemary) Leaf Oil, Zinc Pyrithione, Vitis Vinifera (Grape) Seed Extract, Fragrance, Citric Acid, Sodium Hydroxide, Methylisothiazolinone.",
     "type": "Shampoo"},
    {"name": "Himalaya Neem & Turmeric Soap", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Sodium Palmate, Sodium Palm Kernelate, Aqua, Glycerin, Fragrance, Melia Azadirachta (Neem) Seed Oil, Tetrasodium EDTA, Curcuma Longa (Turmeric) Root Oil, Pentaerythrityl Tetra-di-t-butyl Hydroxyhydrocinnamate, CI 47000, CI 61565.",
     "type": "Soap"},
    {"name": "Himalaya Baby Powder", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Talc, Zinc Oxide, Fragrance, Olea Europaea (Olive) Fruit Oil, Prunus Amygdalus Dulcis (Sweet Almond) Oil, Vetiveria Zizanioides (Vetiver) Root Extract, Yashada Bhasma.",
     "type": "Powder"},
    {"name": "Complete Care Toothpaste", "brand": "Himalaya Wellness", "category": "Personal Care",
     "raw": "Sorbitol, Aqua, Hydrated Silica, Glycerin, Sodium Lauryl Sulfate, Flavor, Carrageenan, Sodium Saccharin, Punica Granatum (Pomegranate) Pericarp Extract, Azadirachta Indica (Neem) Bark Extract, Acacia Arabica (Babool) Bark Extract, Terminalia Chebula (Chebulic Myrobalan) Fruit Extract, Terminalia Bellerica Fruit Extract, Emblica Officinalis Fruit Extract.",
     "type": "Toothpaste"},
    # CONSUMER HEALTH
    {"name": "Koflet Syrup", "brand": "Himalaya Wellness", "category": "Consumer Health",
     "raw": "Madhu (Honey) 1.25g, Guggulu (Balsamodendron mukul) 35mg, Draksha (Vitis vinifera) 35mg, Vishnupriya (Ocimum sanctum) 25mg, Juvantika (Adhatoda vasica) 15mg, Yashtimadhu (Glycyrrhiza glabra) 15mg, Gojiha (Onosma bracteatum) 10mg, Vidanga (Emblica ribes) 10mg.",
     "type": "Cough syrup"},
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
            'awareness_score': score, 'summary': f"{name} by {p['brand']}. {p['type']}. Himalaya Wellness product. Score: {score}/100.",
            'fssai_note': 'Himalaya product - certified and approved for use in India.',
            'verdict': 'Ayurvedic formulation with traditional ingredients' if score >= 80 else 'Contains synthetic and natural ingredients',
            'recommendation': 'Follow package directions. Consult healthcare professional for extended use.',
            'ingredients': ingredient_objs, 'ingredients_raw': raw, 'status': 'active',
        }).execute()
        print(f"  + {name} | score {score} | {len(ingredient_objs)} ingredients")
        return True
    except Exception as e:
        print(f"  ERROR '{name}': {e}")
        return False

def main():
    print(f"Inserting {len(PRODUCTS)} Himalaya Wellness products...")
    inserted = sum(1 for p in PRODUCTS if insert(p))
    for _ in range(len(PRODUCTS)): time.sleep(0.05)
    print(f"\nDone: {inserted} new / {len(PRODUCTS) - inserted} already existed")

if __name__ == '__main__':
    main()
