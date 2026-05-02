import os
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase_admin

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "shubhampaliwal5@gmail.com")


def _verify_admin(authorization: Optional[str]) -> None:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization token")
    token = authorization.split(" ", 1)[1]
    try:
        resp = supabase_admin.auth.get_user(token)
        email = resp.user.email if resp and resp.user else None
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")
    if email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail=f"Admin access required (got {email})")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


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

    res = supabase_admin.from_("ai_extracted_products") \
        .update({"ingredients_raw": payload.reported_ingredients, "ingredients": []}) \
        .eq("id", payload.product_id) \
        .execute()

    if not res.data:
        raise HTTPException(
            status_code=404,
            detail=f"Product id '{payload.product_id}' not found in ai_extracted_products"
        )

    supabase_admin.from_("ingredient_reports") \
        .update({"status": "approved", "reviewed_at": _now_iso()}) \
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
        .update({"status": "rejected", "reviewed_at": _now_iso()}) \
        .eq("id", report_id) \
        .execute()

    return {"ok": True}
