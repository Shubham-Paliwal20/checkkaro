import os
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase_admin

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "shubhampaliwal5@gmail.com")


def _verify_admin(authorization: Optional[str]) -> None:
    """Verify the caller is the admin via their Supabase JWT."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization token")
    token = authorization.split(" ", 1)[1]
    try:
        user = supabase_admin.auth.get_user(token)
        email = user.user.email if user and user.user else None
        if email != ADMIN_EMAIL:
            raise HTTPException(status_code=403, detail="Admin access required")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class ApprovePayload(BaseModel):
    report_id: str
    product_id: str
    reported_ingredients: str


@router.post("/reports/approve")
async def approve_report(
    payload: ApprovePayload,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    # Update the product's ingredients_raw with the approved text
    res = supabase_admin.from_("ai_extracted_products") \
        .update({"ingredients_raw": payload.reported_ingredients, "ingredients": []}) \
        .eq("id", payload.product_id) \
        .execute()

    if not res.data:
        raise HTTPException(status_code=404, detail=f"Product {payload.product_id} not found in database")

    # Mark the report as approved
    supabase_admin.from_("ingredient_reports") \
        .update({"status": "approved", "reviewed_at": "now()"}) \
        .eq("id", payload.report_id) \
        .execute()

    return {"ok": True, "updated": len(res.data)}


@router.post("/reports/reject")
async def reject_report(
    report_id: str,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    supabase_admin.from_("ingredient_reports") \
        .update({"status": "rejected", "reviewed_at": "now()"}) \
        .eq("id", report_id) \
        .execute()

    return {"ok": True}
