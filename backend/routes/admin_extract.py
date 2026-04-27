from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase_client import supabase
from services.gemini_service import extract_ingredients_from_image, analyze_ingredients_list

router = APIRouter()

ADMIN_EMAIL = "shubhampaliwal5@gmail.com"


class ExtractRequest(BaseModel):
    submission_id: str
    admin_email: str


@router.post("/extract-product")
async def extract_product(req: ExtractRequest):
    if req.admin_email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Fetch submission
    result = supabase.from_("product_submissions").select("*").eq("id", req.submission_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Submission not found")

    sub = result.data
    images: list = sub.get("images") or []
    product_name: str = sub.get("product_name_searched") or "Unknown Product"

    if not images:
        raise HTTPException(status_code=400, detail="No images in this submission")

    # Try back-label image first (index 1), then fall back to others
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
            detail="Could not read ingredients from any uploaded image. Try a clearer back-label photo."
        )

    print(f"[EXTRACT] Product: {product_name}")
    print(f"[EXTRACT] Ingredients text: {ingredients_text[:200]}")

    # Classify ingredients with Gemini
    analysis = await analyze_ingredients_list(product_name, ingredients_text)

    product_data = {
        "name": product_name,
        "brand": analysis.get("brand") or "Unknown",
        "category": analysis.get("category") or "General",
        "image_url": images[0],
        "awareness_score": int(analysis.get("awareness_score") or 50),
        "summary": analysis.get("summary") or "",
        "fssai_note": analysis.get("fssai_note") or "",
        "verdict": analysis.get("verdict") or "",
        "recommendation": analysis.get("recommendation") or "",
        "ingredients": analysis.get("ingredients") or [],
        "ingredients_raw": ingredients_text,
        "submission_id": req.submission_id,
    }

    # Save to ai_extracted_products
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
        "ingredients_raw": ingredients_text,
        "message": "Product extracted and added to database successfully",
    }
