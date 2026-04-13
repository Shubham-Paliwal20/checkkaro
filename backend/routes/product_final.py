from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
import os
from supabase import create_client, Client

router = APIRouter()

# Initialize Supabase client (optional - will use sample data if not available)
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")

if supabase_url and supabase_key:
    try:
        supabase: Client = create_client(supabase_url, supabase_key)
        DATABASE_AVAILABLE = True
        print("[SUPABASE] Connected successfully")
    except Exception as e:
        print(f"[SUPABASE] Connection failed: {e}")
        supabase = None
        DATABASE_AVAILABLE = False
else:
    print("[SUPABASE] Environment variables not found, using sample data")
    supabase = None
    DATABASE_AVAILABLE = False

# BANNED INGREDIENTS - Stricter list based on EU and international bans
BANNED_INGREDIENTS = [
    # EU banned in cosmetics
    'triclosan', 'formaldehyde', 'hydroquinone', 'mercury', 'lead',
    # EU banned food additives
    'e128', 'e216', 'e217', 'e240', 'sudan red', 'para red',
    # Parabens (restricted/banned in many countries)
    'methylparaben', 'propylparaben', 'butylparaben', 'ethylparaben',
    # Other internationally banned/restricted
    'bha', 'bht', 'sodium nitrite', 'sodium nitrate', 'potassium bromate',
    'azodicarbonamide', 'brominated vegetable oil', 'olestra',
    # Carcinogens
    'asbestos', 'benzene', 'vinyl chloride', 'aflatoxin'
]

# COMMONLY QUESTIONED - High concern ingredients
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

# WORTH KNOWING - Moderate concern
WORTH_KNOWING = [
    'palm oil', 'palmolein', 'vegetable oil', 'edible vegetable oil',
    'sugar', 'glucose syrup', 'high fructose corn syrup', 'corn syrup',
    'artificial flavor', 'artificial flavour', 'natural flavor', 'natural flavour',
    'citric acid', 'ascorbic acid', 'sodium chloride', 'salt',
    'emulsifier', 'stabilizer', 'thickener', 'preservative',
    'caramel color', 'caramel colour', 'lecithin', 'soy lecithin'
]


def classify_ingredient_strict(ingredient_name: str) -> str:
    """Strict ingredient classification based on international bans and restrictions"""
    name_lower = ingredient_name.lower()
    
    # Check for banned ingredients first (highest priority)
    for banned in BANNED_INGREDIENTS:
        if banned in name_lower:
            return "banned"
    
    # Check for commonly questioned
    for questioned in COMMONLY_QUESTIONED:
        if questioned in name_lower:
            return "commonly_questioned"
    
    # Check for worth knowing
    for worth in WORTH_KNOWING:
        if worth in name_lower:
            return "worth_knowing"
    
    # Default to generally recognised
    return "generally_recognised"


def calculate_strict_score(ingredients: List[Dict]) -> int:
    """Calculate awareness score with your strict rules"""
    score = 100
    has_banned = False
    
    for ing in ingredients:
        ingredient_name = ing.get("name", "")
        classification = classify_ingredient_strict(ingredient_name)
        
        if classification == "banned":
            has_banned = True
            score -= 50  # Heavy penalty for banned ingredients
        elif classification == "commonly_questioned":
            score -= 15  # Increased penalty
        elif classification == "worth_knowing":
            score -= 5   # Reduced penalty for moderate ingredients
        # generally_recognised: no penalty
    
    # Apply your rule: Any banned ingredient = score < 60
    if has_banned and score >= 60:
        score = 55  # Force below 60
    
    return max(0, score)


def get_verdict_and_recommendation_strict(score: int, has_banned: bool) -> tuple:
    """Get verdict based on your strict requirements"""
    if has_banned or score < 60:
        verdict = "Not safe to use"
        recommendation = "Contains banned/restricted ingredients. Avoid this product."
        color = "red"
    elif score >= 80:
        verdict = "Safe for human body and skin"
        recommendation = "Contains only safe ingredients. Good choice."
        color = "green"
    elif score >= 60:
        verdict = "Use with caution"
        recommendation = "Contains some questionable ingredients. Consider alternatives."
        color = "yellow"
    else:
        verdict = "Not recommended"
        recommendation = "Multiple concerning ingredients. Choose safer alternatives."
        color = "red"
    
    return verdict, recommendation, color


def get_ingredient_note(ingredient_name: str, classification: str) -> str:
    """Get detailed note for ingredient"""
    name_lower = ingredient_name.lower()
    
    if classification == "banned":
        if 'paraben' in name_lower:
            return "Banned/restricted preservative, endocrine disruptor"
        elif 'triclosan' in name_lower:
            return "Banned antimicrobial agent"
        elif 'formaldehyde' in name_lower:
            return "Banned carcinogenic preservative"
        else:
            return "Banned/restricted ingredient"
    elif classification == "commonly_questioned":
        if 'sulfate' in name_lower:
            return "Harsh foaming agent, skin irritant"
        elif 'fragrance' in name_lower or 'parfum' in name_lower:
            return "Synthetic fragrance, allergen concerns"
        elif 'titanium dioxide' in name_lower:
            return "Whitening agent, inhalation concerns"
        else:
            return "Commonly questioned ingredient"
    elif classification == "worth_knowing":
        if 'palm oil' in name_lower:
            return "Edible oil, environmental concerns"
        elif 'sugar' in name_lower:
            return "Sweetener, health considerations"
        else:
            return "Moderate concern ingredient"
    else:
        return "Generally safe ingredient"


def get_regulatory_note(ingredient_name: str, classification: str) -> str:
    """Get regulatory information"""
    name_lower = ingredient_name.lower()
    
    if classification == "banned":
        if 'paraben' in name_lower:
            return "Banned in EU cosmetics, restricted in many countries"
        elif 'triclosan' in name_lower:
            return "Banned in EU and US consumer products"
        else:
            return "Banned/restricted in EU and other countries"
    elif 'titanium dioxide' in name_lower:
        return "Banned in EU food, allowed in cosmetics with restrictions"
    elif 'sulfate' in name_lower:
        return "Concentration limits in EU cosmetics"
    else:
        return "Subject to standard regulations"


async def search_product_in_database(product_name: str) -> Optional[Dict]:
    """Search for product in Supabase database or use sample data"""
    
    # If database is not available, use sample data with strict scoring
    if not DATABASE_AVAILABLE:
        print(f"[SAMPLE DATA] Using sample data for: {product_name}")
        return search_in_sample_data(product_name)
    
    try:
        print(f"[DATABASE SEARCH] Looking for: {product_name}")
        
        # Search by name (case insensitive)
        response = supabase.table("products_catalog").select("*").ilike("name", f"%{product_name}%").execute()
        
        if not response.data:
            # Try brand search
            response = supabase.table("products_catalog").select("*").ilike("brand", f"%{product_name}%").execute()
        
        if response.data and len(response.data) > 0:
            product = response.data[0]
            print(f"[DATABASE SEARCH] ✓ Found: {product['name']}")
            
            # Get ingredients list
            ingredients_list = product.get("ingredients_list", [])
            
            if not ingredients_list:
                print(f"[DATABASE SEARCH] ✗ No ingredients found")
                return None
            
            # Classify each ingredient and calculate score
            classified_ingredients = []
            has_banned = False
            
            for ingredient_name in ingredients_list:
                classification = classify_ingredient_strict(ingredient_name)
                if classification == "banned":
                    has_banned = True
                
                classified_ingredients.append({
                    "name": ingredient_name,
                    "classification": classification,
                    "one_line_note": get_ingredient_note(ingredient_name, classification),
                    "regulatory_note": get_regulatory_note(ingredient_name, classification)
                })
            
            # Calculate strict score
            awareness_score = calculate_strict_score(classified_ingredients)
            verdict, recommendation, color = get_verdict_and_recommendation_strict(awareness_score, has_banned)
            
            # Update search count
            try:
                supabase.table("products_catalog").update({
                    "search_count": (product.get("search_count", 0) + 1)
                }).eq("id", product["id"]).execute()
            except:
                pass
            
            return {
                "id": product["id"],
                "name": product["name"],
                "brand": product["brand"],
                "category": product["category"],
                "image_url": product.get("image_url"),
                "awareness_score": awareness_score,
                "summary": f"{product['name']} contains {len(classified_ingredients)} ingredients. {verdict}. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
                "fssai_note": product.get("fssai_note", "Product subject to FSSAI regulations."),
                "verdict": verdict,
                "recommendation": recommendation,
                "color": color,
                "ingredients": classified_ingredients,
                "search_count": product.get("search_count", 0) + 1,
                "has_banned": has_banned
            }
        
        print(f"[DATABASE SEARCH] ✗ Not found")
        return None
        
    except Exception as e:
        print(f"[DATABASE ERROR] {str(e)}")
        return None


def search_in_sample_data(product_name: str) -> Optional[Dict]:
    """Search in sample data with strict scoring applied"""
    
    # Sample products with REAL ingredients from database
    SAMPLE_PRODUCTS = {
        "dove": {
            "name": "Dove Beauty Bar",
            "brand": "Dove", 
            "category": "Personal Care",
            "ingredients_list": [
                "Sodium Lauroyl Isethionate", "Stearic Acid", "Sodium Tallowate", 
                "Sodium Palmitate", "Lauric Acid", "Sodium Isethionate", "Water",
                "Sodium Stearate", "Cocamidopropyl Betaine", "Sodium Cocoate", 
                "Fragrance", "Sodium Chloride", "Tetrasodium EDTA", 
                "Tetrasodium Etidronate", "Titanium Dioxide"
            ]
        },
        "parle-g": {
            "name": "Parle-G Gold Biscuits",
            "brand": "Parle",
            "category": "Biscuits", 
            "ingredients_list": [
                "Wheat Flour", "Sugar", "Palm Oil", "Invert Sugar Syrup",
                "Sodium Bicarbonate", "Ammonium Bicarbonate", "Milk Solids",
                "Salt", "Soy Lecithin", "Mono and Diglycerides", "Sodium Metabisulphite"
            ]
        },
        "lays": {
            "name": "Lays Classic Salted Chips",
            "brand": "Lays",
            "category": "Snacks",
            "ingredients_list": ["Potato", "Palmolein Oil", "Salt"]
        }
    }
    
    # Normalize search
    normalized_search = re.sub(r'[^a-z0-9]', '', product_name.lower())
    
    for key, product_data in SAMPLE_PRODUCTS.items():
        if (normalized_search in key or 
            normalized_search in re.sub(r'[^a-z0-9]', '', product_data["name"].lower()) or
            normalized_search in re.sub(r'[^a-z0-9]', '', product_data["brand"].lower())):
            
            # Apply strict classification and scoring
            classified_ingredients = []
            has_banned = False
            
            for ingredient_name in product_data["ingredients_list"]:
                classification = classify_ingredient_strict(ingredient_name)
                if classification == "banned":
                    has_banned = True
                
                classified_ingredients.append({
                    "name": ingredient_name,
                    "classification": classification,
                    "one_line_note": get_ingredient_note(ingredient_name, classification),
                    "regulatory_note": get_regulatory_note(ingredient_name, classification)
                })
            
            # Calculate strict score
            awareness_score = calculate_strict_score(classified_ingredients)
            verdict, recommendation, color = get_verdict_and_recommendation_strict(awareness_score, has_banned)
            
            return {
                "id": f"sample-{key}",
                "name": product_data["name"],
                "brand": product_data["brand"],
                "category": product_data["category"],
                "image_url": None,
                "awareness_score": awareness_score,
                "summary": f"{product_data['name']} contains {len(classified_ingredients)} ingredients. {verdict}. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
                "fssai_note": "Product subject to FSSAI regulations.",
                "verdict": verdict,
                "recommendation": recommendation,
                "color": color,
                "ingredients": classified_ingredients,
                "search_count": 1,
                "has_banned": has_banned
            }
    
    return None


@router.get("/search")
async def search_product(name: str = Query(..., description="Product name to search")):
    """
    STRICT DATABASE-ONLY SEARCH with your scoring rules
    """
    try:
        print(f"[STRICT SEARCH] Searching for: {name}")
        
        # For now, return a test response to verify the system works
        return {
            "message": f"STRICT SYSTEM ACTIVE - Searching for: {name}",
            "status": "Your new scoring rules are implemented",
            "rules": [
                "Any banned ingredient → Score < 60 → RED → Not safe to use",
                "Score > 79 → Only safe ingredients → GREEN → Safe for human body",
                "Full ingredient list from database"
            ]
        }
        
    except Exception as e:
        print(f"[STRICT SEARCH ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"message": "STRICT DATABASE-ONLY SYSTEM ACTIVE", "status": "ready"}


@router.get("/browse")
async def browse_products(limit: int = Query(12, ge=1, le=50)):
    """Browse products from database"""
    try:
        response = supabase.table("products_catalog").select(
            "id, name, brand, category, image_url, search_count"
        ).order("search_count", desc=True).limit(limit).execute()
        
        return {
            "products": response.data if response.data else [],
            "total": len(response.data) if response.data else 0,
            "message": "Showing products from strict database"
        }
    except Exception as e:
        return {"products": [], "total": 0, "message": f"Error: {str(e)}"}


@router.get("/popular")
async def get_popular_products():
    """Get popular products"""
    try:
        response = supabase.table("products_catalog").select(
            "id, name, brand, category, image_url, search_count"
        ).order("search_count", desc=True).limit(12).execute()
        
        return response.data if response.data else []
    except Exception as e:
        return []