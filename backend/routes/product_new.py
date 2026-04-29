from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from models.schemas import ProductResponse, IngredientItem
import re
from routes.product_all_data import ALL_PRODUCTS
from routes.product_ingredients_full import get_ingredients
from routes.product_images import PRODUCT_IMAGES
from db.supabase_client import supabase

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
async def search_product(name: str = Query(..., description="Product name to search", min_length=1, max_length=120)):
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
    
    # Check Supabase ai_extracted_products for community-submitted products
    try:
        db_result = supabase.from_("ai_extracted_products") \
            .select("*") \
            .ilike("name", f"%{name}%") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        if db_result.data:
            p = db_result.data[0]
            raw_ingredients = p.get("ingredients") or []
            ingredients = [
                IngredientItem(
                    name=ing.get("name", ""),
                    aliases=ing.get("aliases", ""),
                    classification=ing.get("classification", "generally_recognised"),
                    one_line_note=ing.get("one_line_note", ""),
                    regulatory_note=ing.get("regulatory_note", ""),
                )
                for ing in raw_ingredients
            ]
            print(f"[SUPABASE] Found AI-extracted product: {p['name']}")
            raw_images = p.get("images") or []
            if not raw_images and p.get("image_url"):
                raw_images = [p["image_url"]]
            return ProductResponse(
                id=str(p.get("id", "")),
                name=p["name"],
                brand=p.get("brand") or "Unknown",
                category=p.get("category") or "General",
                image_url=p.get("image_url"),
                images=raw_images if raw_images else None,
                awareness_score=int(p.get("awareness_score") or 50),
                summary=p.get("summary") or "",
                fssai_note=p.get("fssai_note") or "",
                verdict=p.get("verdict") or "",
                recommendation=p.get("recommendation") or "",
                ingredients=ingredients,
                search_count=1,
                data_source="community_verified",
                confidence="medium",
                is_complete=True,
            )
    except Exception as e:
        print(f"[SUPABASE SEARCH ERROR] {e}")

    # Product not found anywhere
    available_products = list(SAMPLE_PRODUCTS.keys())
    raise HTTPException(
        status_code=404,
        detail=f"Product '{name}' not found in database. Available sample products: {', '.join(available_products[:20])}... ({len(available_products)} total products). Load full database with detailed ingredients using the SQL files."
    )


@router.get("/browse")
async def browse_products(
    category: str = Query(None, description="Filter by category"),
    brand: str = Query(None, description="Filter by brand"),
    q: str = Query(None, description="Search within results"),
    page: int = Query(1, ge=1),
    limit: int = Query(24, ge=1, le=100),
    sort: str = Query("score", description="sort: score | name | brand"),
):
    """Browse all products with category/brand filters and pagination."""
    # Start with static products
    items = list(SAMPLE_PRODUCTS.values())

    # Add community-submitted products from Supabase
    try:
        community = supabase.from_("ai_extracted_products") \
            .select("id, name, brand, category, image_url, awareness_score, verdict") \
            .order("created_at", desc=True) \
            .limit(500) \
            .execute()
        for p in (community.data or []):
            items.append({
                "id":              str(p.get("id", "")),
                "name":            p.get("name", ""),
                "brand":           p.get("brand") or "Unknown",
                "category":        p.get("category") or "General",
                "image_url":       p.get("image_url"),
                "awareness_score": int(p.get("awareness_score") or 50),
                "verdict":         p.get("verdict") or "",
            })
    except Exception as e:
        print(f"[BROWSE SUPABASE ERROR] {e}")

    # Filter
    if category and category != "All":
        items = [p for p in items if p["category"] == category]
    if brand and brand != "All":
        items = [p for p in items if p["brand"] == brand]
    if q:
        q_lower = q.lower()
        items = [
            p for p in items
            if q_lower in p["name"].lower() or q_lower in p["brand"].lower()
        ]

    # Sort
    if sort == "name":
        items.sort(key=lambda p: p["name"].lower())
    elif sort == "brand":
        items.sort(key=lambda p: (p["brand"].lower(), p["name"].lower()))
    else:
        items.sort(key=lambda p: p["awareness_score"], reverse=True)

    total = len(items)

    # Paginate
    start = (page - 1) * limit
    page_items = items[start: start + limit]

    # Categories and brands from all items (static + community)
    all_items = list(SAMPLE_PRODUCTS.values())
    try:
        all_cats   = sorted({p["category"] for p in all_items} | {p["category"] for p in (community.data or []) if p.get("category")})
        base_brand = {p["brand"] for p in all_items}
        comm_brand = {p.get("brand") for p in (community.data or []) if p.get("brand")}
        if category and category != "All":
            avail_brands = sorted(
                {p["brand"] for p in all_items if p["category"] == category} |
                {p.get("brand") for p in (community.data or []) if p.get("category") == category and p.get("brand")}
            )
        else:
            avail_brands = sorted(base_brand | comm_brand)
    except Exception:
        all_cats     = sorted({p["category"] for p in all_items})
        avail_brands = sorted({p["brand"] for p in all_items})

    return {
        "products": [
            {
                "id":              p["id"],
                "name":            p["name"],
                "brand":           p["brand"],
                "category":        p["category"],
                "image_url":       p["image_url"],
                "awareness_score": p["awareness_score"],
                "verdict":         p["verdict"],
            }
            for p in page_items
        ],
        "total": total,
        "page": page,
        "pages": max(1, -(-total // limit)),
        "categories": all_cats,
        "brands": avail_brands,
    }


@router.get("/suggestions")
async def get_search_suggestions(q: str = Query(..., description="Search query for suggestions", min_length=1, max_length=80)):
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
