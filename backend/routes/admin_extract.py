import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase
from services.gemini_service import extract_ingredients_from_image, analyze_ingredients_list

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def _verify_admin(authorization: Optional[str]) -> None:
    """Verify Supabase JWT token and check admin role. Raises 401/403 on failure."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = authorization.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Empty token")

    try:
        resp = supabase.auth.get_user(token)
        user = resp.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    if not user or not user.email:
        raise HTTPException(status_code=401, detail="Could not identify user from token")

    if not ADMIN_EMAIL:
        raise HTTPException(status_code=500, detail="ADMIN_EMAIL not configured on server")

    if user.email.lower() != ADMIN_EMAIL.lower():
        raise HTTPException(status_code=403, detail="Forbidden")


class ExtractRequest(BaseModel):
    submission_id: str


@router.post("/extract-product")
async def extract_product(
    req: ExtractRequest,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    # Fetch submission
    result = supabase.from_("product_submissions").select("*").eq("id", req.submission_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Submission not found")

    sub = result.data
    images: list = sub.get("images") or []
    product_name: str = (sub.get("product_name_searched") or "Unknown Product")[:200]

    if not images:
        raise HTTPException(status_code=400, detail="No images in this submission")

    # Try back-label image first (index 1), then others
    ordered = ([images[1]] if len(images) > 1 else []) + [images[0]] + images[2:]
    ingredients_text = "NOT_VISIBLE"
    used_url = ordered[0]

    for url in ordered:
        text = await extract_ingredients_from_image(url, product_name)
        if text and text != "NOT_VISIBLE":
            ingredients_text = text
            used_url = url
            break

    if ingredients_text == "NOT_VISIBLE":
        raise HTTPException(
            status_code=422,
            detail="Could not read ingredients from any uploaded image. Try a clearer back-label photo.",
        )

    print(f"[EXTRACT] Product: {product_name} | Chars: {len(ingredients_text)}")

    # Classify ingredients with Gemini
    analysis = await analyze_ingredients_list(product_name, ingredients_text)

    product_data = {
        "name": product_name,
        "brand": (analysis.get("brand") or "Unknown")[:100],
        "category": (analysis.get("category") or "General")[:100],
        "image_url": images[0],
        "awareness_score": max(0, min(100, int(analysis.get("awareness_score") or 50))),
        "summary": (analysis.get("summary") or "")[:2000],
        "fssai_note": (analysis.get("fssai_note") or "")[:500],
        "verdict": (analysis.get("verdict") or "")[:200],
        "recommendation": (analysis.get("recommendation") or "")[:500],
        "ingredients": analysis.get("ingredients") or [],
        "ingredients_raw": ingredients_text[:5000],
        "submission_id": req.submission_id,
    }

    insert_res = supabase.from_("ai_extracted_products").insert(product_data).execute()
    if not insert_res.data:
        raise HTTPException(status_code=500, detail="Failed to save extracted product to database")

    # Mark submission as extracted
    supabase.from_("product_submissions").update({"status": "extracted"}).eq("id", req.submission_id).execute()

    return {
        "success": True,
        "product_name": product_name,
        "brand": analysis.get("brand"),
        "awareness_score": analysis.get("awareness_score"),
        "ingredients_count": len(analysis.get("ingredients") or []),
        "message": "Product extracted and added to database successfully",
    }
