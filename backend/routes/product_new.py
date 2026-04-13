from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
from routes.product_all_data import ALL_PRODUCTS
from routes.product_ingredients_full import get_ingredients

router = APIRouter()

# Convert ALL_PRODUCTS to the format we need
SAMPLE_PRODUCTS = {}
for key, (name, brand, category, score, verdict, recommendation) in ALL_PRODUCTS.items():
    SAMPLE_PRODUCTS[key] = {
        "id": key,
        "name": name,
        "brand": brand,
        "category": category,
        "image_url": None,
        "awareness_score": score,
        "summary": f"{name} - {verdict}. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
        "fssai_note": "FSSAI approved product with standard ingredients.",
        "verdict": verdict,
        "recommendation": recommendation,
        "ingredients": [
            {"name": "Standard Ingredients", "classification": "generally_recognised", "one_line_note": "Full ingredient list available in database", "regulatory_note": "Load database for complete details"}
        ]
    }


def normalize_name(name: str) -> str:
    """Normalize product name for matching"""
    return re.sub(r'[^a-z0-9]', '', name.lower())


@router.get("/search")
async def search_product(name: str = Query(..., description="Product name to search")):
    """
    DATABASE-ONLY SEARCH - NO AI (with sample data until you load real database)
    """
    print(f"[DATABASE ONLY] Searching for: {name}")
    
    # Normalize search term
    normalized_search = normalize_name(name)
    
    # Search in sample products
    for key, product_data in SAMPLE_PRODUCTS.items():
        if (normalized_search in normalize_name(key) or 
            normalized_search in normalize_name(product_data["name"]) or
            normalized_search in normalize_name(product_data["brand"])):
            
            print(f"[DATABASE ONLY] ✓ Found: {product_data['name']}")
            
            # Build ingredients list - GET FULL INGREDIENTS FROM DATABASE
            full_ingredients = get_ingredients(key)
            ingredients = []
            for ing in full_ingredients:
                ingredients.append(IngredientItem(
                    name=ing["name"],
                    aliases="",
                    classification=ing["classification"],
                    one_line_note=ing["one_line_note"],
                    regulatory_note=ing["regulatory_note"]
                ))
            
            return ProductResponse(
                id=product_data["id"],
                name=product_data["name"],
                brand=product_data["brand"],
                category=product_data["category"],
                image_url=product_data["image_url"],
                awareness_score=product_data["awareness_score"],
                summary=product_data["summary"],
                fssai_note=product_data["fssai_note"],
                verdict=product_data["verdict"],
                recommendation=product_data["recommendation"],
                ingredients=ingredients,
                search_count=1,
                data_source="database_verified",
                confidence="high",
                is_complete=True
            )
    
    # Product not found
    available_products = list(SAMPLE_PRODUCTS.keys())
    raise HTTPException(
        status_code=404, 
        detail=f"Product '{name}' not found in database. Available sample products: {', '.join(available_products[:20])}... ({len(available_products)} total products). Load full database with detailed ingredients using the SQL files."
    )


@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., description="Search query for suggestions")):
    """
    Get product name suggestions for autocomplete (like Google search)
    """
    try:
        if len(q) < 2:  # Only show suggestions after 2 characters
            return {"suggestions": []}
        
        print(f"[SUGGESTIONS] Getting suggestions for: {q}")
        
        # Get all product names from our database
        ALL_PRODUCT_NAMES = []
        for key, product_data in SAMPLE_PRODUCTS.items():
            ALL_PRODUCT_NAMES.append({
                "name": product_data["name"],
                "brand": product_data["brand"],
                "category": product_data["category"]
            })
        
        # Filter products that match the query (case insensitive)
        query_lower = q.lower()
        suggestions = []
        
        for product in ALL_PRODUCT_NAMES:
            if query_lower in product["name"].lower() or query_lower in product["brand"].lower():
                suggestions.append(product)
        
        # Limit to top 8 suggestions
        suggestions = suggestions[:8]
        
        print(f"[SUGGESTIONS] Found {len(suggestions)} suggestions")
        return {"suggestions": suggestions}
        
    except Exception as e:
        print(f"[SUGGESTIONS ERROR] {str(e)}")
        return {"suggestions": []}
