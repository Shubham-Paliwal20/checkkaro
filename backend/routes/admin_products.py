import logging
import re
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db.supabase_client import supabase_admin
from utils.auth import get_current_user, require_admin

logger = logging.getLogger(__name__)
router = APIRouter()

_SAFE_ID = re.compile(r'^[a-zA-Z0-9_\-]{1,128}$')

def _validate_product_id(pid: str) -> str:
    if not _SAFE_ID.match(pid):
        raise HTTPException(status_code=400, detail="Invalid product_id format")
    return pid


# ── PATCH /api/admin-products/{product_id}/name ──────────────────────────────
class NameUpdateBody(BaseModel):
    name: str

@router.patch("/{product_id}/name")
async def update_product_name(product_id: str, body: NameUpdateBody, request: Request):
    """Admin: rename a product in ai_extracted_products."""
    await require_admin(request)
    _validate_product_id(product_id)
    name = body.name.strip()[:300]
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    try:
        supabase_admin.table("ai_extracted_products") \
            .update({"name": name}) \
            .eq("id", product_id) \
            .execute()
        return {"updated": product_id, "name": name}
    except Exception as e:
        logger.error("update_product_name failed id=%s: %s", product_id, e)
        raise HTTPException(status_code=500, detail="Failed to update product name")  # S4


# ── PATCH /api/admin-products/{product_id}/ingredients ───────────────────────
class IngredientsUpdateBody(BaseModel):
    ingredients_raw: Optional[str] = None
    ingredients: Optional[list] = None
    grade: Optional[str] = None

@router.patch("/{product_id}/ingredients")
async def update_product_ingredients(product_id: str, body: IngredientsUpdateBody, request: Request):
    """Admin: update ingredients_raw, classified ingredients, and/or grade."""
    await require_admin(request)
    _validate_product_id(product_id)
    payload = {}
    if body.ingredients_raw is not None:
        payload["ingredients_raw"] = body.ingredients_raw
    if body.ingredients is not None:
        payload["ingredients"] = body.ingredients
    if body.grade is not None:
        if body.grade not in ("A", "B", "C", "D"):
            raise HTTPException(status_code=400, detail="grade must be A, B, C, or D")
        payload["grade"] = body.grade
    if not payload:
        raise HTTPException(status_code=400, detail="Nothing to update")
    try:
        supabase_admin.table("ai_extracted_products") \
            .update(payload) \
            .eq("id", product_id) \
            .execute()
        return {"updated": product_id}
    except Exception as e:
        logger.error("update_product_ingredients failed id=%s: %s", product_id, e)
        raise HTTPException(status_code=500, detail="Failed to update ingredients")  # S4


# ── POST /api/admin-products/lookup-or-insert ────────────────────────────────
class LookupOrInsertBody(BaseModel):
    name: str
    ingredients_raw: Optional[str] = None
    ingredients: Optional[list] = None
    grade: Optional[str] = None

@router.post("/lookup-or-insert")
async def lookup_or_insert_product(body: LookupOrInsertBody, request: Request):
    """Admin: look up a product by name; insert if not found. Returns the record ID."""
    await require_admin(request)
    name = body.name.strip()[:300]
    if not name:
        raise HTTPException(status_code=400, detail="Name required")

    payload = {}
    if body.ingredients_raw is not None: payload["ingredients_raw"] = body.ingredients_raw
    if body.ingredients is not None: payload["ingredients"] = body.ingredients
    if body.grade is not None: payload["grade"] = body.grade

    try:
        found = supabase_admin.table("ai_extracted_products") \
            .select("id") \
            .ilike("name", name) \
            .limit(1) \
            .execute()
        if found.data:
            record_id = found.data[0]["id"]
            if payload:
                supabase_admin.table("ai_extracted_products") \
                    .update(payload) \
                    .eq("id", record_id) \
                    .execute()
            return {"id": record_id, "action": "updated"}
        else:
            inserted = supabase_admin.table("ai_extracted_products") \
                .insert({"name": name, **payload}) \
                .select("id") \
                .execute()
            return {"id": inserted.data[0]["id"], "action": "inserted"}
    except Exception as e:
        logger.error("lookup_or_insert failed name=%s: %s", name, e)
        raise HTTPException(status_code=500, detail="Failed to lookup or insert product")  # S4


# ── POST /api/admin-products/reports ─────────────────────────────────────────
class IngredientReportBody(BaseModel):
    product_id: str
    product_name: str
    reported_ingredients: str
    reason: Optional[str] = None

@router.post("/reports")
async def submit_ingredient_report(body: IngredientReportBody, request: Request):
    """Authenticated user: submit an ingredient correction report."""
    user = await get_current_user(request)
    _validate_product_id(body.product_id)  # S7: validate product_id format

    reported = body.reported_ingredients.strip()[:5000]
    if not reported:
        raise HTTPException(status_code=400, detail="reported_ingredients cannot be empty")

    try:
        supabase_admin.table("ingredient_reports").insert({
            "product_id": body.product_id,
            "product_name": body.product_name[:200],
            "user_id": str(user.id),
            "user_email": user.email,
            "reported_ingredients": reported,
            "reason": (body.reason or "").strip()[:1000] or None,
            "status": "pending",
        }).execute()
        return {"message": "Report submitted. Thank you for helping improve our database!"}
    except Exception as e:
        logger.error("submit_ingredient_report failed user=%s: %s", user.id, e)
        raise HTTPException(status_code=500, detail="Failed to submit report")  # S4
