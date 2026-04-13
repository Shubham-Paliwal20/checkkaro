from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class IngredientItem(BaseModel):
    name: str
    aliases: Optional[str] = None
    classification: str
    one_line_note: Optional[str] = None
    regulatory_note: Optional[str] = None
    detailed_effects: Optional[str] = None  # New field for detailed harmful effects


class ProductResponse(BaseModel):
    id: Optional[str] = None
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    awareness_score: int = 50
    summary: Optional[str] = None
    fssai_note: Optional[str] = None
    verdict: Optional[str] = None  # New field for final verdict
    recommendation: Optional[str] = None  # New field for usage recommendation
    ingredients: List[IngredientItem] = []
    search_count: int = 1
    data_source: Optional[str] = None  # Where data came from
    confidence: Optional[str] = None  # high | medium | low
    is_complete: bool = False  # Whether ingredient list is complete


class IngredientRuleResponse(BaseModel):
    name: str
    aliases: List[str] = []
    classification: str
    what_it_is: Optional[str] = None
    commonly_found_in: Optional[str] = None
    one_line_note: Optional[str] = None
    regulatory_note: Optional[str] = None  # Added for consistency
    countries_restricted: List[str] = []
    fssai_position: Optional[str] = None
    health_effects: Optional[dict] = None  # Added for detailed health information


class SearchHistoryItem(BaseModel):
    query: str
    product_name: Optional[str] = None
    searched_at: datetime


class RecommendationItem(BaseModel):
    recommended_name: str
    recommended_brand: Optional[str] = None
    recommended_image: Optional[str] = None
    buy_link: Optional[str] = None
    is_sponsored: bool = False
