from fastapi import APIRouter
from typing import List
from models.schemas import SearchHistoryItem

router = APIRouter()


@router.get("", response_model=List[SearchHistoryItem])
async def get_search_history():
    """Search history is not persisted server-side."""
    return []
