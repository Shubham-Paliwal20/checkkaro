from fastapi import APIRouter, Query, HTTPException
from models.schemas import IngredientRuleResponse
from db.supabase_client import supabase
from services import groq_service, ingredient_matcher

router = APIRouter()


@router.get("/search", response_model=IngredientRuleResponse)
async def search_ingredient(name: str = Query(..., description="Ingredient name to search")):
    """
    Search for ingredient information. Checks database first, then queries Groq if not found.
    """
    try:
        # Try to match with existing ingredient rules
        matched = await ingredient_matcher.match_ingredient(name)
        
        if matched:
            return IngredientRuleResponse(
                name=matched["name"],
                aliases=matched.get("aliases", []),
                classification=matched["classification"],
                what_it_is=matched.get("what_it_is"),
                commonly_found_in=matched.get("commonly_found_in"),
                one_line_note=matched.get("one_line_note"),
                countries_restricted=matched.get("countries_restricted", []),
                fssai_position=matched.get("fssai_position")
            )
        
        # Not found in database - analyze with Groq
        analysis = await groq_service.analyze_ingredient(name)
        
        # Save new rule to database
        try:
            ingredient_insert = {
                "name": analysis.get("name", name),
                "aliases": analysis.get("aliases", []),
                "classification": analysis.get("classification", "worth_knowing"),
                "what_it_is": analysis.get("what_it_is"),
                "commonly_found_in": analysis.get("commonly_found_in"),
                "one_line_note": analysis.get("one_line_note"),
                "countries_restricted": analysis.get("countries_restricted", []),
                "fssai_position": analysis.get("fssai_position"),
                "applies_to": "both"
            }
            
            supabase.table("ingredient_rules").insert(ingredient_insert).execute()
        except Exception as db_error:
            # If insert fails (e.g., duplicate), continue anyway
            print(f"Could not save ingredient rule: {db_error}")
        
        return IngredientRuleResponse(
            name=analysis.get("name", name),
            aliases=analysis.get("aliases", []),
            classification=analysis.get("classification", "worth_knowing"),
            what_it_is=analysis.get("what_it_is"),
            commonly_found_in=analysis.get("commonly_found_in"),
            one_line_note=analysis.get("one_line_note"),
            countries_restricted=analysis.get("countries_restricted", []),
            fssai_position=analysis.get("fssai_position")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching ingredient: {str(e)}")
