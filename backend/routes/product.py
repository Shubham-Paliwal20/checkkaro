from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from models.schemas import ProductResponse, IngredientItem
from db.supabase_client import supabase
from services import groq_service, openfoodfacts_service, ingredient_matcher

router = APIRouter()


@router.get("/search", response_model=ProductResponse)
async def search_product(name: str = Query(..., description="Product name to search")):
    """
    Search for a product by name. Returns cached data if available and fresh,
    otherwise fetches new analysis from Groq and Open Food Facts.
    """
    try:
        # Normalize query
        normalized = name.lower().strip()
        
        # Check if product exists in database
        response = supabase.table("products").select("*").ilike("name_normalized", f"%{normalized}%").execute()
        
        product_data = None
        product_id = None
        
        if response.data and len(response.data) > 0:
            product_data = response.data[0]
            product_id = product_data["id"]
            
            # Check if data is fresh (less than 6 months old)
            last_verified = datetime.fromisoformat(product_data["last_verified"].replace("Z", "+00:00"))
            if datetime.now(last_verified.tzinfo) - last_verified < timedelta(days=180):
                # Increment search count
                supabase.table("products").update({
                    "search_count": product_data["search_count"] + 1
                }).eq("id", product_id).execute()
                
                # Fetch ingredients
                ing_response = supabase.table("product_ingredients").select("*").eq("product_id", product_id).execute()
                
                ingredients = [
                    IngredientItem(
                        name=ing["ingredient_name"],
                        aliases=ing.get("aliases"),
                        classification=ing["classification"],
                        one_line_note=ing.get("one_line_note"),
                        regulatory_note=ing.get("regulatory_note")
                    )
                    for ing in ing_response.data
                ]
                
                # Record search history
                supabase.table("search_history").insert({
                    "query": name,
                    "product_id": product_id
                }).execute()
                
                return ProductResponse(
                    id=product_data["id"],
                    name=product_data["name"],
                    brand=product_data.get("brand"),
                    category=product_data.get("category"),
                    image_url=product_data.get("image_url"),
                    awareness_score=product_data["awareness_score"],
                    summary=product_data.get("summary"),
                    fssai_note=product_data.get("fssai_note"),
                    ingredients=ingredients,
                    search_count=product_data["search_count"] + 1
                )
        
        # Data not found or stale - fetch new analysis
        # Get product image from Open Food Facts
        image_url = await openfoodfacts_service.get_product_image(name)
        
        # Analyze product with Groq
        analysis = await groq_service.analyze_product(name)
        
        # Prepare product data for upsert
        product_insert = {
            "name": name,
            "name_normalized": normalized,
            "brand": analysis.get("brand"),
            "category": analysis.get("category"),
            "image_url": image_url,
            "awareness_score": analysis.get("awareness_score", 50),
            "summary": analysis.get("summary"),
            "fssai_note": analysis.get("fssai_note"),
            "search_count": (product_data["search_count"] + 1) if product_data else 1,
            "last_verified": datetime.now().isoformat()
        }
        
        # Upsert product
        if product_id:
            supabase.table("products").update(product_insert).eq("id", product_id).execute()
        else:
            insert_response = supabase.table("products").insert(product_insert).execute()
            product_id = insert_response.data[0]["id"]
        
        # Delete old ingredients and insert new ones
        supabase.table("product_ingredients").delete().eq("product_id", product_id).execute()
        
        ingredients = []
        for ing in analysis.get("ingredients", []):
            # Try to match with existing ingredient rules
            matched = await ingredient_matcher.match_ingredient(ing.get("name", ""))
            
            ingredient_insert = {
                "product_id": product_id,
                "ingredient_name": ing.get("name"),
                "aliases": ing.get("aliases"),
                "classification": ing.get("classification", "worth_knowing"),
                "one_line_note": ing.get("one_line_note"),
                "regulatory_note": ing.get("regulatory_note")
            }
            
            supabase.table("product_ingredients").insert(ingredient_insert).execute()
            
            ingredients.append(IngredientItem(
                name=ing.get("name"),
                aliases=ing.get("aliases"),
                classification=ing.get("classification", "worth_knowing"),
                one_line_note=ing.get("one_line_note"),
                regulatory_note=ing.get("regulatory_note")
            ))
        
        # Record search history
        supabase.table("search_history").insert({
            "query": name,
            "product_id": product_id
        }).execute()
        
        return ProductResponse(
            id=product_id,
            name=name,
            brand=analysis.get("brand"),
            category=analysis.get("category"),
            image_url=image_url,
            awareness_score=analysis.get("awareness_score", 50),
            summary=analysis.get("summary"),
            fssai_note=analysis.get("fssai_note"),
            ingredients=ingredients,
            search_count=product_insert["search_count"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching product: {str(e)}")


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    """
    Get product details by UUID.
    """
    try:
        # Fetch product
        response = supabase.table("products").select("*").eq("id", product_id).execute()
        
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product_data = response.data[0]
        
        # Fetch ingredients
        ing_response = supabase.table("product_ingredients").select("*").eq("product_id", product_id).execute()
        
        ingredients = [
            IngredientItem(
                name=ing["ingredient_name"],
                aliases=ing.get("aliases"),
                classification=ing["classification"],
                one_line_note=ing.get("one_line_note"),
                regulatory_note=ing.get("regulatory_note")
            )
            for ing in ing_response.data
        ]
        
        return ProductResponse(
            id=product_data["id"],
            name=product_data["name"],
            brand=product_data.get("brand"),
            category=product_data.get("category"),
            image_url=product_data.get("image_url"),
            awareness_score=product_data["awareness_score"],
            summary=product_data.get("summary"),
            fssai_note=product_data.get("fssai_note"),
            ingredients=ingredients,
            search_count=product_data["search_count"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching product: {str(e)}")


@router.get("/browse", response_model=dict)
async def browse_products(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50)
):
    """
    Browse products with optional category filter and pagination.
    """
    try:
        offset = (page - 1) * limit
        
        # Build query
        query = supabase.table("products").select("*", count="exact")
        
        if category:
            query = query.eq("category", category)
        
        # Order by search count and paginate
        response = query.order("search_count", desc=True).range(offset, offset + limit - 1).execute()
        
        products = [
            {
                "id": p["id"],
                "name": p["name"],
                "brand": p.get("brand"),
                "category": p.get("category"),
                "image_url": p.get("image_url"),
                "awareness_score": p["awareness_score"],
                "search_count": p["search_count"]
            }
            for p in response.data
        ]
        
        return {
            "products": products,
            "total": response.count,
            "page": page,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error browsing products: {str(e)}")


@router.get("/popular", response_model=list)
async def get_popular_products():
    """
    Get top 12 most searched products.
    """
    try:
        response = supabase.table("products").select("*").order("search_count", desc=True).limit(12).execute()
        
        products = [
            {
                "id": p["id"],
                "name": p["name"],
                "brand": p.get("brand"),
                "category": p.get("category"),
                "image_url": p.get("image_url"),
                "awareness_score": p["awareness_score"],
                "search_count": p["search_count"]
            }
            for p in response.data
        ]
        
        return products
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching popular products: {str(e)}")
