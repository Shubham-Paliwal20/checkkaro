import re
from fastapi import APIRouter, Query, HTTPException
from models.schemas import IngredientRuleResponse
from routes.ingredient_database import get_ingredient_details, classify_ingredient, INGREDIENT_DESCRIPTIONS, _normalize_ins
from typing import List, Dict

router = APIRouter()

_popular_cache = None  # computed once, never changes

# Build a sorted master list of (key, display_name) once at import time
def _build_master_list():
    result = []
    for key in INGREDIENT_DESCRIPTIONS:
        if re.match(r'^e\d+', key):
            display = key.upper()          # e200 → E200
        elif re.match(r'^ci \d+', key):
            display = key.upper()          # ci 19140 → CI 19140
        else:
            display = key.title()          # sorbic acid → Sorbic Acid
        result.append((key, display))
    return result

_MASTER_LIST = _build_master_list()


@router.get("/search", response_model=IngredientRuleResponse)
async def search_ingredient(name: str = Query(..., description="Ingredient name to search", min_length=1, max_length=100)):
    """
    Search for ingredient information using centralized database
    Ensures consistency with product search results
    """
    try:
        # Normalize INS numbers (INS 200 → E200) before lookup
        name = _normalize_ins(name).upper() if re.match(r'^ins[\s\-]*\d+', name.strip(), re.I) else name
        # Get ingredient details from centralized database
        ingredient_data = get_ingredient_details(name)
        
        return IngredientRuleResponse(
            name=ingredient_data['name'],
            classification=ingredient_data['classification'],
            what_it_is=ingredient_data['what_it_is'],
            commonly_found_in=ingredient_data['commonly_found_in'],
            one_line_note=ingredient_data['one_line_note'],
            regulatory_note=ingredient_data['regulatory_note'],
            recommendation=ingredient_data.get('recommendation'),
            health_effects=ingredient_data.get('health_effects'),
            countries_restricted=ingredient_data.get('countries_restricted', []),
            fssai_position=ingredient_data.get('fssai_position'),
            related_ingredients=ingredient_data.get('related_ingredients', []),
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredient: {str(e)}")


@router.get("/suggestions")
async def get_ingredient_suggestions(
    q: str = Query(..., description="Search term for ingredient suggestions", min_length=1),
    limit: int = Query(10, description="Maximum number of suggestions", ge=1, le=20)
) -> List[Dict]:
    """
    Get ingredient suggestions for auto-complete from all 400+ INGREDIENT_DESCRIPTIONS entries.
    Supports E-numbers (e200, E200), INS numbers (INS 200, INS200), and plain names.
    """
    try:
        q_stripped = q.strip()
        if not q_stripped:
            return []

        # Normalize INS query → E-number key  (INS 200 → e200, ins2 → e2)
        q_lower = _normalize_ins(q_stripped)

        # If user typed just "ins" with no digit, treat as prefix "e" to show E-number entries
        if q_stripped.lower().startswith('ins') and q_lower == q_stripped.lower():
            q_lower = 'e'

        starts: List[tuple] = []
        contains: List[tuple] = []

        for key, display in _MASTER_LIST:
            if key.startswith(q_lower):
                starts.append((key, display))
            elif q_lower in key:
                contains.append((key, display))

        # starts-with first, then contains; both sorted alphabetically
        starts.sort(key=lambda x: x[0])
        contains.sort(key=lambda x: x[0])
        matched = (starts + contains)[:limit]

        results = []
        for key, display in matched:
            cls = classify_ingredient(key)
            results.append({
                'id': key,
                'name': display,
                'classification': cls['classification'],
                'what_it_is': cls['what_it_is'],
                'aliases': []
            })

        return results

    except Exception as e:
        print(f"Error getting ingredient suggestions: {str(e)}")
        return []


@router.get("/popular")
async def get_popular_ingredients(
    limit: int = Query(20, description="Maximum number of popular ingredients", ge=1, le=50)
) -> List[Dict]:
    global _popular_cache
    if _popular_cache is None:
        popular_names = [
            'TBHQ', 'Tartrazine', 'MSG', 'Sodium Benzoate',
            'Sunset Yellow', 'Allura Red', 'Phosphoric Acid',
            'Sodium Nitrite', 'Sulfur Dioxide', 'Methylparaben',
            'Propylparaben', 'Carrageenan', 'High Fructose Corn Syrup',
            'Palm Oil', 'Sodium Lauryl Sulfate', 'Fragrance',
        ]
        try:
            _popular_cache = [
                {
                    'id': n.lower().replace(' ', '-'),
                    'name': n,
                    'classification': classify_ingredient(n)['classification'],
                    'what_it_is': classify_ingredient(n)['what_it_is'],
                }
                for n in popular_names
            ]
        except Exception as e:
            print(f"Error building popular cache: {e}")
            _popular_cache = []
    return _popular_cache[:limit]
