from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from db.supabase_client import supabase_admin
from utils.auth import get_current_user, require_admin

router = APIRouter()


# ── PATCH /api/admin-products/{product_id}/name ──────────────────────────────
class NameUpdateBody(BaseModel):
    name: str

@router.patch("/{product_id}/name")
async def update_product_name(product_id: str, body: NameUpdateBody, request: Request):
    """Admin: rename a product in ai_extracted_products."""
    await require_admin(request)
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    try:
        supabase_admin.table("ai_extracted_products") \
            .update({"name": name}) \
            .eq("id", product_id) \
            .execute()
        return {"updated": product_id, "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── PATCH /api/admin-products/{product_id}/ingredients ───────────────────────
class IngredientsUpdateBody(BaseModel):
    ingredients_raw: Optional[str] = None
    ingredients: Optional[list] = None
    grade: Optional[str] = None

@router.patch("/{product_id}/ingredients")
async def update_product_ingredients(product_id: str, body: IngredientsUpdateBody, request: Request):
    """Admin: update ingredients_raw, classified ingredients, and/or grade."""
    await require_admin(request)
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
        raise HTTPException(status_code=500, detail=str(e))


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
    name = body.name.strip()
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
        raise HTTPException(status_code=500, detail=str(e))


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
    if not body.reported_ingredients.strip():
        raise HTTPException(status_code=400, detail="reported_ingredients cannot be empty")
    try:
        supabase_admin.table("ingredient_reports").insert({
            "product_id": body.product_id,
            "product_name": body.product_name,
            "user_id": str(user.id),
            "user_email": user.email,
            "reported_ingredients": body.reported_ingredients.strip(),
            "reason": (body.reason or "").strip() or None,
            "status": "pending",
        }).execute()
        return {"message": "Report submitted. Thank you for helping improve our database!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
