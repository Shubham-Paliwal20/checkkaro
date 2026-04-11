from typing import Optional, Dict, List
from db.supabase_client import supabase


async def match_ingredient(name: str) -> Optional[Dict]:
    """
    Match an ingredient name against the ingredient_rules table.
    Matches by name (case insensitive) or any alias in the aliases array.
    Returns the full ingredient rule record or None.
    """
    try:
        # First try exact name match (case insensitive)
        response = supabase.table("ingredient_rules").select("*").ilike("name", name).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        
        # Try alias match using PostgreSQL array contains operator
        # Note: Supabase Python client may need raw query for array operations
        response = supabase.table("ingredient_rules").select("*").execute()
        
        if response.data:
            name_lower = name.lower()
            for rule in response.data:
                # Check if name matches any alias
                aliases = rule.get("aliases", [])
                if aliases:
                    for alias in aliases:
                        if alias.lower() == name_lower:
                            return rule
        
        return None
        
    except Exception as e:
        print(f"Ingredient matcher error: {e}")
        return None


async def match_all_ingredients(names: List[str]) -> Dict[str, List]:
    """
    Match multiple ingredient names.
    Returns dict with 'matched' and 'unmatched' lists.
    """
    matched = []
    unmatched = []
    
    for name in names:
        result = await match_ingredient(name)
        if result:
            matched.append({
                "name": name,
                "rule": result
            })
        else:
            unmatched.append(name)
    
    return {
        "matched": matched,
        "unmatched": unmatched
    }
