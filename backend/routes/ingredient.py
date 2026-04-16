from fastapi import APIRouter, Query, HTTPException
from models.schemas import IngredientRuleResponse
from services.ingredient_service import ingredient_service
from routes.ingredient_database import get_ingredient_details  # Fallback for missing ingredients
from typing import List, Dict

router = APIRouter()


@router.get("/search", response_model=IngredientRuleResponse)
async def search_ingredient(name: str = Query(..., description="Ingredient name to search")):
    """
    Search for ingredient information using database first, fallback to hardcoded patterns
    """
    try:
        # Try database search first
        ingredient_data = ingredient_service.search_ingredient(name)
        
        # If not found in database, fallback to hardcoded patterns
        if not ingredient_data:
            ingredient_data = get_ingredient_details(name)
        
        return IngredientRuleResponse(
            name=ingredient_data['name'],
            classification=ingredient_data['classification'],
            what_it_is=ingredient_data['what_it_is'],
            commonly_found_in=ingredient_data['commonly_found_in'],
            one_line_note=ingredient_data['one_line_note'],
            regulatory_note=ingredient_data['regulatory_note'],
            health_effects=ingredient_data.get('health_effects'),
            countries_restricted=ingredient_data.get('countries_restricted', []),
            fssai_position=ingredient_data.get('fssai_position'),
            aliases=ingredient_data.get('aliases', [])
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredient: {str(e)}")


@router.get("/suggestions")
async def get_ingredient_suggestions(
    q: str = Query(..., description="Search term for ingredient suggestions", min_length=2),
    limit: int = Query(10, description="Maximum number of suggestions", ge=1, le=20)
) -> List[Dict]:
    """
    Get ingredient suggestions for auto-complete functionality
    """
    try:
        suggestions = ingredient_service.get_ingredient_suggestions(q, limit)
        return suggestions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting ingredient suggestions: {str(e)}")


@router.get("/popular")
async def get_popular_ingredients(
    limit: int = Query(20, description="Maximum number of popular ingredients", ge=1, le=50)
) -> List[Dict]:
    """
    Get popular/commonly searched ingredients
    """
    try:
        popular = ingredient_service.get_popular_ingredients(limit)
        return popular
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting popular ingredients: {str(e)}")
