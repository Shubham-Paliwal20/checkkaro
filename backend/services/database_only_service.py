"""
Database-Only Product Service
Only searches products from our database, no AI calls
"""
import re
from typing import Optional, Dict, List
from db.supabase_client import supabase


def normalize_product_name(name: str) -> str:
    """Normalize product name for matching (lowercase, remove special chars)"""
    # Convert to lowercase
    normalized = name.lower()
    # Remove special characters but keep spaces
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    # Remove extra spaces
    normalized = ' '.join(normalized.split())
    return normalized


async def search_product_in_database(product_name: str) -> Optional[Dict]:
    """
    Search for product in products_catalog table only.
    Returns product data if found, None otherwise.
    """
    try:
        normalized_name = normalize_product_name(product_name)
        
        print(f"[DATABASE ONLY] Searching for: {product_name} (normalized: {normalized_name})")
        
        # Try exact match first
        response = supabase.table("products_catalog").select("*").ilike("name", f"%{product_name}%").execute()
        
        if not response.data:
            # Try brand match
            response = supabase.table("products_catalog").select("*").ilike("brand", f"%{product_name}%").execute()
        
        if not response.data:
            # Try normalized search
            normalized_search = normalized_name.replace(' ', '%')
            response = supabase.table("products_catalog").select("*").ilike("name", f"%{normalized_search}%").execute()
        
        if response.data and len(response.data) > 0:
            product = response.data[0]  # Get first match
            
            # Increment search count
            try:
                supabase.table("products_catalog").update({
                    "search_count": (product.get("search_count", 0) + 1)
                }).eq("id", product["id"]).execute()
            except:
                pass  # Don't fail if search count update fails
            
            print(f"[DATABASE ONLY] OK Found: {product['name']} by {product['brand']}")
            
            # Parse ingredients list into proper format
            ingredients = []
            ingredients_list = product.get("ingredients_list", [])
            
            if ingredients_list:
                for idx, ingredient_name in enumerate(ingredients_list):
                    # Simple classification based on common knowledge
                    classification = classify_ingredient_simple(ingredient_name)
                    
                    ingredients.append({
                        "name": ingredient_name,
                        "aliases": "",
                        "classification": classification,
                        "one_line_note": get_simple_note(ingredient_name),
                        "regulatory_note": get_simple_regulatory_note(ingredient_name)
                    })
            
            # Calculate awareness score if not present
            awareness_score = product.get("awareness_score")
            if awareness_score is None:
                awareness_score = calculate_simple_score(ingredients)
            
            # Generate verdict and recommendation based on score
            verdict, recommendation = get_verdict_and_recommendation(awareness_score)
            
            return {
                "id": product["id"],
                "name": product["name"],
                "brand": product["brand"],
                "category": product["category"],
                "image_url": product.get("image_url"),
                "awareness_score": awareness_score,
                "summary": product.get("summary", f"{product['name']} contains {len(ingredients)} ingredients. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."),
                "fssai_note": product.get("fssai_note", "Product subject to FSSAI regulations."),
                "verdict": product.get("verdict", verdict),
                "recommendation": product.get("recommendation", recommendation),
                "ingredients": ingredients,
                "search_count": product.get("search_count", 0) + 1,
                "data_source": "database_only",
                "confidence": "high",
                "is_complete": True
            }
        
        print(f"[DATABASE ONLY] FAIL Not found in database")
        return None
        
    except Exception as e:
        print(f"[DATABASE ONLY ERROR] {str(e)}")
        return None


def classify_ingredient_simple(ingredient_name: str) -> str:
    """Simple ingredient classification without AI"""
    name_lower = ingredient_name.lower()
    
    # Commonly questioned ingredients
    questioned = [
        'sodium lauryl sulfate', 'sls', 'sodium laureth sulfate', 'sles',
        'paraben', 'methylparaben', 'propylparaben', 'butylparaben',
        'triclosan', 'formaldehyde', 'phthalate', 'bht', 'bha',
        'artificial color', 'artificial colour', 'tartrazine', 'sunset yellow',
        'carmoisine', 'allura red', 'brilliant blue', 'e102', 'e110', 'e122', 'e124', 'e133',
        'monosodium glutamate', 'msg', 'disodium guanylate', 'disodium inosinate',
        'sodium benzoate', 'potassium sorbate', 'sodium nitrite', 'sodium nitrate'
    ]
    
    # Worth knowing ingredients
    worth_knowing = [
        'palm oil', 'palmolein', 'vegetable oil', 'edible vegetable oil',
        'sugar', 'glucose syrup', 'high fructose corn syrup', 'corn syrup',
        'artificial flavor', 'artificial flavour', 'natural flavor', 'natural flavour',
        'citric acid', 'ascorbic acid', 'sodium chloride', 'salt',
        'emulsifier', 'stabilizer', 'thickener', 'preservative',
        'caramel color', 'caramel colour', 'titanium dioxide'
    ]
    
    # Check for commonly questioned
    for item in questioned:
        if item in name_lower:
            return "commonly_questioned"
    
    # Check for worth knowing
    for item in worth_knowing:
        if item in name_lower:
            return "worth_knowing"
    
    # Default to generally recognised
    return "generally_recognised"


def get_simple_note(ingredient_name: str) -> str:
    """Get simple one-line note for ingredient"""
    name_lower = ingredient_name.lower()
    
    notes = {
        'water': 'Main component of product',
        'sugar': 'Sweetening agent',
        'salt': 'Flavoring and preservative',
        'wheat flour': 'Main ingredient in baked goods',
        'palm oil': 'Edible vegetable oil',
        'milk solids': 'Dairy component for nutrition',
        'cocoa solids': 'Chocolate flavoring component',
        'sodium lauryl sulfate': 'Foaming agent, skin irritant',
        'sodium laureth sulfate': 'Foaming agent, milder than SLS',
        'paraben': 'Preservative, endocrine concerns',
        'artificial flavor': 'Synthetic flavoring agent',
        'citric acid': 'Natural preservative and flavor enhancer',
        'sodium benzoate': 'Common food preservative',
        'titanium dioxide': 'White coloring agent'
    }
    
    for key, note in notes.items():
        if key in name_lower:
            return note
    
    return "Common food ingredient"


def get_simple_regulatory_note(ingredient_name: str) -> str:
    """Get simple regulatory note for ingredient"""
    name_lower = ingredient_name.lower()
    
    if 'paraben' in name_lower:
        return "Restricted in some countries, subject to ongoing research"
    elif 'sulfate' in name_lower and ('lauryl' in name_lower or 'laureth' in name_lower):
        return "Concentration limits apply in EU"
    elif 'sodium benzoate' in name_lower:
        return "FSSAI approved preservative with usage limits"
    elif 'titanium dioxide' in name_lower:
        return "Banned in food in EU, allowed in cosmetics"
    elif 'artificial color' in name_lower or any(code in name_lower for code in ['e102', 'e110', 'e122', 'e124']):
        return "Requires labeling, some restrictions in children's products"
    else:
        return "No major regulatory restrictions"


def calculate_simple_score(ingredients: List[Dict]) -> int:
    """Calculate awareness score based on ingredient classifications"""
    score = 100
    
    for ing in ingredients:
        classification = ing.get("classification", "worth_knowing")
        
        if classification == "generally_recognised":
            score -= 0
        elif classification == "worth_knowing":
            score -= 8
        elif classification == "commonly_questioned":
            score -= 20
    
    return max(0, score)


def get_verdict_and_recommendation(score: int) -> tuple:
    """Get verdict and recommendation based on score"""
    if score >= 80:
        verdict = "Generally recognised ingredients"
        recommendation = "Can be used with general awareness"
    elif score >= 60:
        verdict = "Worth knowing about some ingredients"
        recommendation = "Use with awareness of flagged ingredients"
    elif score >= 40:
        verdict = "Several ingredients commonly questioned"
        recommendation = "Consider alternatives with fewer questioned ingredients"
    else:
        verdict = "Many ingredients subject to restrictions"
        recommendation = "Consider alternatives with fewer questioned ingredients"
    
    return verdict, recommendation


async def get_popular_products_from_database(limit: int = 12) -> List[Dict]:
    """Get most searched products from database"""
    try:
        response = supabase.table("products_catalog").select(
            "id, name, brand, category, image_url, awareness_score, search_count"
        ).order("search_count", desc=True).limit(limit).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to get popular products: {str(e)}")
        return []


async def search_products_by_name(query: str, limit: int = 20) -> List[Dict]:
    """Search for products in database by name or brand"""
    try:
        # Search by name
        response = supabase.table("products_catalog").select(
            "id, name, brand, category, image_url, awareness_score, search_count"
        ).ilike("name", f"%{query}%").limit(limit).execute()
        
        if not response.data:
            # Search by brand if no name matches
            response = supabase.table("products_catalog").select(
                "id, name, brand, category, image_url, awareness_score, search_count"
            ).ilike("brand", f"%{query}%").limit(limit).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"[DATABASE ERROR] Failed to search products: {str(e)}")
        return []