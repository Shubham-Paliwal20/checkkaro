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
    product_name: str
    photos: list[str]           # URLs already uploaded to Supabase storage
    contact: str                # UPI ID or mobile number for ₹1 reward payment
    variant_label: Optional[str] = None


@router.post("/submit")
async def submit_barcode(body: SubmitBarcodeBody, request: Request):
    if not _BARCODE_RE.match(body.barcode):
        raise HTTPException(status_code=400, detail="Invalid barcode format.")
    if not body.product_name.strip():
        raise HTTPException(status_code=400, detail="Product name is required.")
    if not body.photos:
        raise HTTPException(status_code=400, detail="At least one photo is required.")
    if not body.contact.strip():
        raise HTTPException(status_code=400, detail="UPI ID or mobile number is required.")

    user = await get_current_user(request)

    # Block duplicate pending from same user for same barcode
    dup = supabase_admin.table("barcode_submissions") \
        .select("id") \
        .eq("barcode", body.barcode) \
        .eq("submitted_by", str(user.id)) \
        .eq("status", "pending") \
        .limit(1).execute()
    if dup.data:
        raise HTTPException(status_code=409, detail="You already submitted this barcode. Wait for it to be reviewed.")

    supabase_admin.table("barcode_submissions").insert({
        "barcode": body.barcode,
        "product_name": body.product_name.strip(),
        "variant_label": body.variant_label or None,
        "photos": body.photos,
        "contact": body.contact.strip(),
        "submitted_by": str(user.id),
        "submitted_by_email": user.email,
        "status": "pending",
    }).execute()

    return {"ok": True, "message": "Submitted! You'll earn ₹1 once it's approved."}
