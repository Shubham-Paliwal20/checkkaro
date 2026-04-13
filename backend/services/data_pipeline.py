"""
Multi-source data pipeline for product ingredient information.
Tries multiple sources in order of reliability and stops when good data is found.
"""
from typing import Dict
from services import openfoodfacts_service, edamam_service, bigbasket_service


async def get_product_data(product_name: str) -> dict:
    """
    Master function that tries multiple data sources in order.
    Returns the first source with good quality data (>3 ingredients).
    
    Priority order:
    1. Open Food Facts (highest reliability)
    2. Edamam API (high reliability)
    3. BigBasket scraper (medium reliability)
    4. AI estimation (lowest reliability - fallback only)
    """
    result = {
        "found": False,
        "source": None,
        "product_name": product_name,
        "brand": None,
        "category": None,
        "image_url": None,
        "ingredients_text": "",
        "ingredients_list": [],
        "confidence": "low"
    }
    
    print(f"[DATA PIPELINE] Starting search for: {product_name}")
    
    # SOURCE 1: Open Food Facts
    print("[DATA PIPELINE] Trying Open Food Facts...")
    try:
        off_data = await openfoodfacts_service.search(product_name)
        if off_data["found"] and len(off_data["ingredients_list"]) > 3:
            result.update(off_data)
            result["source"] = "open_food_facts"
            result["confidence"] = "high"
            print(f"[DATA PIPELINE] ✓ Found in Open Food Facts: {len(off_data['ingredients_list'])} ingredients")
            return result
        print(f"[DATA PIPELINE] ✗ Open Food Facts: insufficient data")
    except Exception as e:
        print(f"[DATA PIPELINE] ✗ Open Food Facts error: {e}")
    
    # SOURCE 2: Edamam API
    print("[DATA PIPELINE] Trying Edamam API...")
    try:
        edamam_data = await edamam_service.search(product_name)
        if edamam_data["found"] and len(edamam_data["ingredients_list"]) > 3:
            result.update(edamam_data)
            result["source"] = "edamam"
            result["confidence"] = "high"
            print(f"[DATA PIPELINE] ✓ Found in Edamam: {len(edamam_data['ingredients_list'])} ingredients")
            return result
        print(f"[DATA PIPELINE] ✗ Edamam: insufficient data")
    except Exception as e:
        print(f"[DATA PIPELINE] ✗ Edamam error: {e}")
    
    # SOURCE 3: BigBasket scraper
    print("[DATA PIPELINE] Trying BigBasket scraper...")
    try:
        bb_data = await bigbasket_service.search(product_name)
        if bb_data["found"] and len(bb_data["ingredients_list"]) > 3:
            result.update(bb_data)
            result["source"] = "bigbasket"
            result["confidence"] = "medium"
            print(f"[DATA PIPELINE] ✓ Found in BigBasket: {len(bb_data['ingredients_list'])} ingredients")
            return result
        print(f"[DATA PIPELINE] ✗ BigBasket: insufficient data")
    except Exception as e:
        print(f"[DATA PIPELINE] ✗ BigBasket error: {e}")
    
    # SOURCE 4: AI estimation (fallback)
    print("[DATA PIPELINE] ⚠ Using AI estimation as fallback")
    result["source"] = "ai_estimated"
    result["confidence"] = "low"
    result["found"] = True
    
    return result
