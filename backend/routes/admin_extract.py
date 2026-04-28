import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase
from services.gemini_service import extract_ingredients_from_image, analyze_ingredients_list

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def _verify_admin(authorization: Optional[str]) -> None:
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


def _build_product_data(sub: dict, analysis: dict, ingredients_text: str) -> dict:
    images: list = sub.get("images") or []
    product_name: str = (sub.get("product_name_searched") or "Unknown Product")[:200]
    return {
        "name": product_name,
        "brand": (analysis.get("brand") or "Unknown")[:100],
        "category": (analysis.get("category") or "General")[:100],
        "image_url": images[0] if images else None,
        "awareness_score": max(0, min(100, int(analysis.get("awareness_score") or 50))),
        "summary": (analysis.get("summary") or "")[:2000],
        "fssai_note": (analysis.get("fssai_note") or "")[:500],
        "verdict": (analysis.get("verdict") or "")[:200],
        "recommendation": (analysis.get("recommendation") or "")[:500],
        "ingredients": analysis.get("ingredients") or [],
        "ingredients_raw": ingredients_text[:5000],
        "submission_id": sub["id"],
    }


class ExtractRequest(BaseModel):
    submission_id: str
    # If provided, skip Gemini Vision and use this text directly
    ingredients_text: Optional[str] = None


@router.post("/extract-product")
async def extract_product(
    req: ExtractRequest,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    result = supabase.from_("product_submissions").select("*").eq("id", req.submission_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Submission not found")

    sub = result.data
    images: list = sub.get("images") or []
    product_name: str = (sub.get("product_name_searched") or "Unknown Product")[:200]

    # ── Path A: manual text provided by admin ────────────────────────────────
    if req.ingredients_text and req.ingredients_text.strip():
        ingredients_text = req.ingredients_text.strip()
        print(f"[EXTRACT-MANUAL] Product: {product_name} | Chars: {len(ingredients_text)}")

    # ── Path B: AI vision from images ────────────────────────────────────────
    else:
        if not images:
            raise HTTPException(status_code=400, detail="No images in this submission and no manual text provided")

        # Try back-label (index 1) first, then front, then rest
        ordered = ([images[1]] if len(images) > 1 else []) + [images[0]] + images[2:]
        ingredients_text = "NOT_VISIBLE"

        for url in ordered:
            text = await extract_ingredients_from_image(url, product_name)
            if text and text != "NOT_VISIBLE":
                ingredients_text = text
                break

        if ingredients_text == "NOT_VISIBLE":
            raise HTTPException(
                status_code=422,
                detail=(
                    "Could not read ingredients from any uploaded image. "
                    "Try the 'Enter manually' option and paste the ingredients text."
                ),
            )

        print(f"[EXTRACT-VISION] Product: {product_name} | Chars: {len(ingredients_text)}")

    # ── Classify with Gemini ──────────────────────────────────────────────────
    analysis = await analyze_ingredients_list(product_name, ingredients_text)

    product_data = _build_product_data(sub, analysis, ingredients_text)

    insert_res = supabase.from_("ai_extracted_products").insert(product_data).execute()
    if not insert_res.data:
        raise HTTPException(status_code=500, detail="Failed to save extracted product to database")

    supabase.from_("product_submissions").update({"status": "extracted"}).eq("id", req.submission_id).execute()

    return {
        "success": True,
        "product_name": product_name,
        "brand": analysis.get("brand"),
        "awareness_score": analysis.get("awareness_score"),
        "ingredients_count": len(analysis.get("ingredients") or []),
        "message": "Product extracted and added to database successfully",
    }
