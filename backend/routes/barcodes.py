import re
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase_admin
from utils.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

_BARCODE_RE = re.compile(r'^\d{8,14}$')


class SubmitBarcodeBody(BaseModel):
    barcode: str
    product_id: str
    product_name: str
    variant_label: Optional[str] = None


@router.post("/submit")
async def submit_barcode(body: SubmitBarcodeBody, request: Request):
    if not _BARCODE_RE.match(body.barcode):
        raise HTTPException(status_code=400, detail="Invalid barcode format.")

    user = await get_current_user(request)

    # Block if already approved for this barcode
    existing = supabase_admin.table("product_barcodes").select("id").eq("barcode", body.barcode).eq("status", "approved").limit(1).execute()
    if existing.data:
        raise HTTPException(status_code=409, detail="This barcode is already linked to a product.")

    # Block duplicate pending from same user
    dup = supabase_admin.table("product_barcodes").select("id").eq("barcode", body.barcode).eq("submitted_by", str(user.id)).eq("status", "pending").limit(1).execute()
    if dup.data:
        raise HTTPException(status_code=409, detail="You already submitted this barcode. Wait for it to be reviewed.")

    supabase_admin.table("product_barcodes").insert({
        "barcode": body.barcode,
        "product_id": body.product_id,
        "product_name": body.product_name,
        "variant_label": body.variant_label or None,
        "submitted_by": str(user.id),
        "submitted_by_email": user.email,
        "status": "pending",
    }).execute()

    return {"ok": True, "message": "Barcode submitted! You'll earn ₹1 once it's approved."}
