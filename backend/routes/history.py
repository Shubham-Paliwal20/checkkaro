from fastapi import APIRouter, Query, HTTPException
from typing import List
from models.schemas import SearchHistoryItem

router = APIRouter()


@router.get("", response_model=List[SearchHistoryItem])
async def get_search_history(limit: int = Query(20, ge=1, le=100)):
    """Get search history - stub implementation"""
    return []
    """
    Get recent search history with product names.
    """
    try:
        # Fetch search history with product join
        response = supabase.table("search_history").select(
            "query, searched_at, products(name)"
        ).order("searched_at", desc=True).limit(limit).execute()
        
        history = [
            SearchHistoryItem(
                query=item["query"],
                product_name=item["products"]["name"] if item.get("products") else None,
                searched_at=item["searched_at"]
            )
            for item in response.data
        ]
        
        return history
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching search history: {str(e)}")
