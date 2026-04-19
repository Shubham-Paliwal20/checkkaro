from fastapi import APIRouter, Query, HTTPException
from models.schemas import IngredientRuleResponse
from routes.ingredient_database import get_ingredient_details, classify_ingredient
from typing import List, Dict

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
            health_effects=ingredient_data.get('health_effects'),
            countries_restricted=ingredient_data.get('countries_restricted', []),
            fssai_position=ingredient_data.get('fssai_position'),
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredient: {str(e)}")


@router.get("/suggestions")
async def get_ingredient_suggestions(
    q: str = Query(..., description="Search term for ingredient suggestions", min_length=1),
    limit: int = Query(10, description="Maximum number of suggestions", ge=1, le=20)
) -> List[Dict]:
    """
    Get ingredient suggestions for auto-complete functionality
    Returns matching ingredients from hardcoded patterns
    """
    try:
        if len(q) < 1:
            return []
        
        # Get all ingredient patterns from the classify_ingredient function
        from routes.ingredient_database import classify_ingredient
        
        # Common ingredients list for suggestions
        common_ingredients = [
            # Commonly Questioned
            'Triclosan', 'Sodium Benzoate', 'Sodium Metabisulphite', 'Sodium Nitrite', 
            'Sodium Nitrate', 'Sulfur Dioxide', 'Methylparaben', 'Propylparaben', 
            'Butylparaben', 'Tartrazine', 'Sunset Yellow', 'Allura Red', 'Ponceau 4R',
            'Carmoisine', 'Brilliant Blue', 'Indigo Carmine', 'Erythrosine', 
            'Quinoline Yellow', 'Brown HT', 'Disodium Guanylate', 'Disodium Inosinate',
            'Monosodium Glutamate', 'MSG', 'Phosphoric Acid', 'Caramel Colour',
            'Methylchloroisothiazolinone', 'Methylisothiazolinone', 'Fragrance',
            'Perfume', 'Artificial Flavor',
            
            # Worth Knowing
            'Sugar', 'High Fructose Corn Syrup', 'Glucose Syrup', 'Invert Sugar',
            'Maltodextrin', 'Palm Oil', 'Palmolein', 'Hydrogenated Oil',
            'Partially Hydrogenated Oil', 'Soy Lecithin', 'Mono and Diglycerides',
            'Polyglycerol Polyricinoleate', 'Ammonium Phosphatides', 'Carrageenan',
            'Sodium Laureth Sulfate', 'Sodium Lauryl Sulfate', 'Cocamidopropyl Betaine',
            'Dimethiconol', 'Dimethicone', 'Tetrasodium EDTA', 'Disodium EDTA',
            'Potassium Sorbate', 'Citric Acid', 'Titanium Dioxide', 'Beta Carotene',
            'Guar Gum', 'Xanthan Gum', 'Propylene Glycol', 'Glycerin', 'Sorbitol',
            'Caffeine', 'Alcohol', 'Ethanol', 'Salt', 'Sodium Chloride',
            
            # Generally Recognised
            'Ascorbic Acid', 'Vitamin C', 'Tocopherol', 'Vitamin E', 'Water',
            'Lactic Acid', 'Malic Acid', 'Annatto', 'Turmeric', 'Paprika',
            'Beetroot', 'Shellac', 'Beeswax', 'Carnauba Wax'
        ]
        
        # Filter ingredients that match the query
        query_lower = q.lower()
        matching = []
        
        for ingredient in common_ingredients:
            if query_lower in ingredient.lower():
                # Get classification for this ingredient
                classification_data = classify_ingredient(ingredient)
                matching.append({
                    'id': ingredient.lower().replace(' ', '-'),
                    'name': ingredient,
                    'classification': classification_data['classification'],
                    'what_it_is': classification_data['what_it_is'],
                    'aliases': []
                })
                
                if len(matching) >= limit:
                    break
        
        # Sort by relevance (starts with query first)
        matching.sort(key=lambda x: (
            not x['name'].lower().startswith(query_lower),
            x['name'].lower()
        ))
        
        return matching[:limit]
        
    except Exception as e:
        print(f"Error getting ingredient suggestions: {str(e)}")
        return []


@router.get("/popular")
async def get_popular_ingredients(
    limit: int = Query(20, description="Maximum number of popular ingredients", ge=1, le=50)
) -> List[Dict]:
    """
    Get popular/commonly searched ingredients
    """
    try:
        # Return commonly questioned ingredients (most interesting)
        popular = [
            'TBHQ', 'Tartrazine', 'MSG', 'Sodium Benzoate',
            'Sunset Yellow', 'Allura Red', 'Phosphoric Acid',
            'Sodium Nitrite', 'Sulfur Dioxide', 'Methylparaben',
            'Propylparaben', 'Carrageenan', 'High Fructose Corn Syrup',
            'Palm Oil', 'Sodium Lauryl Sulfate', 'Fragrance'
        ]
        
        result = []
        for ingredient in popular[:limit]:
            classification_data = classify_ingredient(ingredient)
            result.append({
                'id': ingredient.lower().replace(' ', '-'),
                'name': ingredient,
                'classification': classification_data['classification'],
                'what_it_is': classification_data['what_it_is']
            })
        
        return result
        
    except Exception as e:
        print(f"Error getting popular ingredients: {str(e)}")
        return []
