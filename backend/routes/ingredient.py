from fastapi import APIRouter, Query, HTTPException
from models.schemas import IngredientRuleResponse
from routes.ingredient_database import get_ingredient_details

router = APIRouter()


@router.get("/search", response_model=IngredientRuleResponse)
async def search_ingredient(name: str = Query(..., description="Ingredient name to search")):
    """
    Search for ingredient information using centralized database
    Ensures consistency with product search results
    """
    try:
        # Get ingredient details from centralized database
        ingredient_data = get_ingredient_details(name)
        
        return IngredientRuleResponse(
            name=ingredient_data['name'],
            classification=ingredient_data['classification'],
            what_it_is=ingredient_data['what_it_is'],
            commonly_found_in=ingredient_data['commonly_found_in'],
            one_line_note=ingredient_data['one_line_note'],
            regulatory_note=ingredient_data['regulatory_note'],
            health_effects=ingredient_data.get('health_effects')
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredient: {str(e)}")
