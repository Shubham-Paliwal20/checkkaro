from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
from routes.product_all_data import ALL_PRODUCTS
from routes.product_ingredients_full import get_ingredients
from routes.product_images import PRODUCT_IMAGES

router = APIRouter()

# Convert ALL_PRODUCTS to the format we need
SAMPLE_PRODUCTS = {}
for key, (name, brand, category, score, verdict, recommendation) in ALL_PRODUCTS.items():
    SAMPLE_PRODUCTS[key] = {
        "id": key,
        "name": name,
        "brand": brand,
        "category": category,
        "image_url": PRODUCT_IMAGES.get(key),
        "awareness_score": score,
        "summary": f"{name} - {verdict}. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.",
        "fssai_note": "FSSAI approved product with standard ingredients.",
        "verdict": verdict,
        "recommendation": recommendation,
        "ingredients": [
            {"name": "Standard Ingredients", "classification": "generally_recognised", "one_line_note": "Full ingredient list available in database", "regulatory_note": "Load database for complete details"}
        ]
    }

# Pre-built search index — computed once at startup, never rebuilt per-request
SEARCH_INDEX = [
    {
        "name": p["name"],
        "brand": p["brand"],
        "category": p["category"],
        "name_lower": p["name"].lower(),
        "brand_lower": p["brand"].lower(),
    }
    for p in SAMPLE_PRODUCTS.values()
]


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
            
            print(f"[DATABASE ONLY] Found: {product_data['name']}")
            
            # Build ingredients list - GET FULL INGREDIENTS FROM DATABASE
            full_ingredients = get_ingredients(key, category=product_data["category"])
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
    if len(q) < 1:
        return {"suggestions": []}

    q_lower = q.lower()
    prefix = []
    substring = []

    for p in SEARCH_INDEX:
        name_match = q_lower in p["name_lower"]
        brand_match = q_lower in p["brand_lower"]
        if not name_match and not brand_match:
            continue
        entry = {"name": p["name"], "brand": p["brand"], "category": p["category"]}
        # Prefix matches in name rank first
        if p["name_lower"].startswith(q_lower):
            prefix.append(entry)
        else:
            substring.append(entry)

    suggestions = (prefix + substring)[:8]
    return {"suggestions": suggestions}
