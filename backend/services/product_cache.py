"""
Product Cache Service
Saves and retrieves product data from database to avoid repeated AI calls
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


async def get_cached_product(product_name: str) -> Optional[Dict]:
    """
    Check if product exists in database and return it.
    Returns None if not found.
    """
    try:
        normalized_name = normalize_product_name(product_name)
        
        print(f"[CACHE] Looking for: {normalized_name}")
        
        # Search for product by normalized name
        response = supabase.table("products").select(
            "*, product_ingredients(*)"
        ).eq("name_normalized", normalized_name).execute()
        
        if response.data and len(response.data) > 0:
            product = response.data[0]
            
            # Increment search count
            supabase.table("products").update({
                "search_count": product["search_count"] + 1
            }).eq("id", product["id"]).execute()
            
            print(f"[CACHE] OK Found in database! ID: {product['id']}, Searches: {product['search_count'] + 1}")
            
            # Format ingredients
            ingredients = []
            for ing in product.get("product_ingredients", []):
                ingredients.append({
                    "name": ing["ingredient_name"],
                    "aliases": ing["aliases"],
                    "classification": ing["classification"],
                    "one_line_note": ing["one_line_note"],
                    "regulatory_note": ing["regulatory_note"]
                })
            
            return {
                "id": product["id"],
                "name": product["name"],
                "brand": product["brand"],
                "category": product["category"],
                "image_url": product["image_url"],
                "awareness_score": product["awareness_score"],
                "summary": product["summary"],
                "fssai_note": product["fssai_note"],
                "verdict": product.get("verdict", ""),
                "recommendation": product.get("recommendation", ""),
                "ingredients": ingredients,
                "from_cache": True,
                "search_count": product["search_count"] + 1
            }
        
        print(f"[CACHE] FAIL Not found in database")
        return None
        
    except Exception as e:
        print(f"[CACHE ERROR] {str(e)}")
        return None


async def save_product_to_cache(
    product_name: str,
    brand: str,
    category: str,
    image_url: Optional[str],
    awareness_score: int,
    summary: str,
    fssai_note: str,
    verdict: str,
    recommendation: str,
    ingredients: List[Dict]
) -> Optional[str]:
    """
    Save product and its ingredients to database.
    Returns product_id if successful, None otherwise.
    """
    try:
        normalized_name = normalize_product_name(product_name)
        
        print(f"[CACHE] Saving product: {product_name} ({len(ingredients)} ingredients)")
        
        # Insert product
        product_data = {
            "name": product_name,
            "name_normalized": normalized_name,
            "brand": brand,
            "category": category,
            "image_url": image_url,
            "awareness_score": awareness_score,
            "summary": summary,
            "fssai_note": fssai_note,
            "verdict": verdict,
            "recommendation": recommendation,
            "search_count": 1
        }
        
        product_response = supabase.table("products").insert(product_data).execute()
        
        if not product_response.data or len(product_response.data) == 0:
            print(f"[CACHE ERROR] Failed to insert product")
            return None
        
        product_id = product_response.data[0]["id"]
        print(f"[CACHE] OK Product saved with ID: {product_id}")
        
        # Insert ingredients
        if ingredients and len(ingredients) > 0:
            ingredient_data = []
            for ing in ingredients:
                ingredient_data.append({
                    "product_id": product_id,
                    "ingredient_name": ing.get("name", "Unknown"),
                    "aliases": ing.get("aliases", ""),
                    "classification": ing.get("classification", "worth_knowing"),
                    "one_line_note": ing.get("one_line_note", ""),
                    "regulatory_note": ing.get("regulatory_note", "")
                })
            
            supabase.table("product_ingredients").insert(ingredient_data).execute()
            print(f"[CACHE] OK Saved {len(ingredient_data)} ingredients")
        
        return product_id
        
    except Exception as e:
        print(f"[CACHE ERROR] Failed to save product: {str(e)}")
        return None


async def update_product_image(product_id: str, image_url: str):
    """Update product image URL if we get it from external source"""
    try:
        if image_url:
            supabase.table("products").update({
                "image_url": image_url
            }).eq("id", product_id).execute()
            print(f"[CACHE] OK Updated image for product {product_id}")
    except Exception as e:
        print(f"[CACHE ERROR] Failed to update image: {str(e)}")


async def get_popular_products(limit: int = 12) -> List[Dict]:
    """Get most searched products from cache"""
    try:
        response = supabase.table("products").select(
            "id, name, brand, category, image_url, awareness_score, search_count"
        ).order("search_count", desc=True).limit(limit).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"[CACHE ERROR] Failed to get popular products: {str(e)}")
        return []


async def search_products_in_cache(query: str, limit: int = 20) -> List[Dict]:
    """Search for products in cache by name"""
    try:
        normalized_query = normalize_product_name(query)
        
        # Search using ILIKE for partial matches
        response = supabase.table("products").select(
            "id, name, brand, category, image_url, awareness_score, search_count"
        ).ilike("name_normalized", f"%{normalized_query}%").limit(limit).execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"[CACHE ERROR] Failed to search products: {str(e)}")
        return []
