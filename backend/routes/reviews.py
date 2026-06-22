from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, conint
from typing import Optional
from db.supabase_client import supabase_admin
from utils.auth import get_current_user

router = APIRouter()


# ── GET /api/reviews/{product_id} ────────────────────────────────────────────
@router.get("/{product_id}")
async def get_reviews(product_id: str):
    """Return all reviews for a product. Public."""
    norm_id = product_id.strip()
    try:
        res = supabase_admin.table("product_reviews") \
            .select("*") \
            .eq("product_id", norm_id) \
            .order("created_at", desc=True) \
            .execute()
        return {"reviews": res.data or []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

    payload = {
        "product_id": body.product_id.strip(),
        "product_name": body.product_name,
        "user_id": str(user.id),
        "reviewer_name": body.reviewer_name.strip(),
        "rating": body.rating,
        "review_text": (body.review_text or "").strip(),
    }
    try:
        supabase_admin.table("product_reviews") \
            .upsert(payload, on_conflict="product_id,user_id") \
            .execute()
        return {"message": "Review saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── PUT /api/reviews/{review_id} ─────────────────────────────────────────────
class ReviewUpdateBody(BaseModel):
    reviewer_name: str
    rating: conint(ge=1, le=5)
    review_text: Optional[str] = ""

@router.put("/{review_id}")
async def update_review(review_id: str, body: ReviewUpdateBody, request: Request):
    """Update reviewer's own review. Only the owner can update."""
    user = await get_current_user(request)
    try:
        supabase_admin.table("product_reviews") \
            .update({
                "reviewer_name": body.reviewer_name.strip(),
                "rating": body.rating,
                "review_text": (body.review_text or "").strip(),
            }) \
            .eq("id", review_id) \
            .eq("user_id", str(user.id)) \
            .execute()
        return {"message": "Review updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
