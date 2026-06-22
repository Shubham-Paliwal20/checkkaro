import logging
import re
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, conint
from typing import Optional
from db.supabase_client import supabase_admin
from utils.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

_SAFE_ID = re.compile(r'^[a-zA-Z0-9_\-]{1,128}$')
_UUID_RE  = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

def _validate_id(val: str) -> str:
    if not _SAFE_ID.match(val) and not _UUID_RE.match(val):
        raise HTTPException(status_code=400, detail="Invalid id format")
    return val.strip()


# ── GET /api/reviews/{product_id} ────────────────────────────────────────────
@router.get("/{product_id}")
async def get_reviews(product_id: str):
    """Return all reviews for a product. Public."""
    norm_id = _validate_id(product_id)  # S2 fix
    try:
        res = supabase_admin.table("product_reviews") \
            .select("*") \
            .eq("product_id", norm_id) \
            .order("created_at", desc=True) \
            .execute()
        return {"reviews": res.data or []}
    except Exception as e:
        logger.error("get_reviews failed product_id=%s: %s", norm_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch reviews")  # S4 fix


# ── POST /api/reviews ─────────────────────────────────────────────────────────
class ReviewBody(BaseModel):
    product_id: str
    product_name: str
    reviewer_name: str
    rating: conint(ge=1, le=5)
    review_text: Optional[str] = ""

@router.post("")
async def upsert_review(body: ReviewBody, request: Request):
    """Insert or update the caller's review for a product. Auth required."""
    user = await get_current_user(request)
    _validate_id(body.product_id)

    payload = {
        "product_id": body.product_id.strip(),
        "product_name": body.product_name[:200],
        "user_id": str(user.id),
        "reviewer_name": body.reviewer_name.strip()[:100],
        "rating": body.rating,
        "review_text": (body.review_text or "").strip()[:2000],
    }
    try:
        supabase_admin.table("product_reviews") \
            .upsert(payload, on_conflict="product_id,user_id") \
            .execute()
        return {"message": "Review saved"}
    except Exception as e:
        logger.error("upsert_review failed user=%s: %s", user.id, e)
        raise HTTPException(status_code=500, detail="Failed to save review")  # S4 fix


# ── PUT /api/reviews/{review_id} ─────────────────────────────────────────────
class ReviewUpdateBody(BaseModel):
    reviewer_name: str
    rating: conint(ge=1, le=5)
    review_text: Optional[str] = ""

@router.put("/{review_id}")
async def update_review(review_id: str, body: ReviewUpdateBody, request: Request):
    """Update reviewer's own review. Only the owner can update."""
    user = await get_current_user(request)
    _validate_id(review_id)
    try:
        supabase_admin.table("product_reviews") \
            .update({
                "reviewer_name": body.reviewer_name.strip()[:100],
                "rating": body.rating,
                "review_text": (body.review_text or "").strip()[:2000],
            }) \
            .eq("id", review_id) \
            .eq("user_id", str(user.id)) \
            .execute()
        return {"message": "Review updated"}
    except Exception as e:
        logger.error("update_review failed review_id=%s user=%s: %s", review_id, user.id, e)
        raise HTTPException(status_code=500, detail="Failed to update review")  # S4 fix
