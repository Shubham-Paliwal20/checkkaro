from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from models.schemas import ProductResponse, IngredientItem

router = APIRouter()


@router.get("/search", response_model=ProductResponse)
async def search_product(name: str = Query(..., description="Product name to search")):
    """
    Search for a product by name. Database-only mode - NO AI.
    """
    try:
        print(f"[DATABASE ONLY] Searching for: {name}")
        
        # For now, return a simple response to test
        # This proves the new code is running
        raise HTTPException(
            status_code=404, 
            detail=f"Database-only mode active. Product '{name}' not found. Please load products into database first."
        )
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"[DATABASE ONLY ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/browse")
async def browse_products(
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50)
):
    """
    Browse products from database. Returns products sorted by popularity.
    """
    try:
        # Get products from database
        products = await database_only_service.get_popular_products_from_database(limit=limit)
        
        # Filter by category if provided
        if category:
            products = [p for p in products if p.get("category", "").lower() == category.lower()]
        
        return {
            "products": products,
            "total": len(products),
            "page": page,
            "limit": limit,
            "message": "Showing products from verified database"
        }
    except Exception as e:
        print(f"[BROWSE ERROR] {str(e)}")
        return {
            "products": [],
            "total": 0,
            "page": page,
            "limit": limit,
            "message": "Error loading products"
        }


@router.get("/popular")
async def get_popular_products():
    """
    Get most searched products from database.
    """
    try:
        products = await database_only_service.get_popular_products_from_database(limit=12)
        return products
    except Exception as e:
        print(f"[POPULAR ERROR] {str(e)}")
        return []



@router.post("/verify")
async def verify_product(product_name: str, is_correct: bool = True):
    """
    User verifies that AI-estimated ingredients are correct.
    """
    try:
        # Log verification (could store in database for analytics)
        print(f"[PRODUCT VERIFY] {product_name} marked as {'correct' if is_correct else 'incorrect'}")
        
        return {
            "success": True,
            "message": "Thank you for your feedback!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error verifying product: {str(e)}")


@router.post("/correct")
async def submit_correction(
    product_name: str,
    ingredients: str,
    product_id: Optional[str] = None
):
    """
    User submits correct ingredients for a product.
    """
    try:
        from db.supabase_client import supabase
        
        # Handle temp-id or invalid UUIDs - set to None
        if product_id and (product_id == "temp-id" or len(product_id) < 36):
            product_id = None
        
        # Insert into pending_corrections table
        correction_data = {
            "product_id": product_id,
            "product_name": product_name,
            "submitted_ingredients": ingredients
        }
        
        result = supabase.table("pending_corrections").insert(correction_data).execute()
        
        print(f"[PRODUCT CORRECT] New correction submitted for: {product_name}")
        
        return {
            "success": True,
            "message": "Thank you! Your correction has been submitted for review.",
            "correction_id": result.data[0]["id"] if result.data else None
        }
    except Exception as e:
        print(f"[PRODUCT CORRECT ERROR] {e}")
        raise HTTPException(status_code=500, detail=f"Error submitting correction: {str(e)}")
