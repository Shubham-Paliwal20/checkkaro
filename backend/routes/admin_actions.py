import logging
import datetime
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase_admin
from utils.auth import require_admin

logger = logging.getLogger(__name__)
router = APIRouter()


def _audit(admin_email: str, action: str, entity_type: str, entity_id: str, details: dict = {}):
    ts = datetime.datetime.utcnow().isoformat()
    print(f"[ADMIN AUDIT] {ts} | {admin_email} | {action} | {entity_type}:{entity_id} | {details}", flush=True)
    try:
        supabase_admin.table("admin_audit_log").insert({
            "admin_email": admin_email,
            "action": action,
            "entity_type": entity_type,
            "entity_id": str(entity_id),
            "details": details,
        }).execute()
    except Exception as e:
        logger.warning("Audit log insert failed (non-fatal): %s", e)


# ── Product Submissions ────────────────────────────────────────────────────────

@router.post("/product-submissions/{id}/approve")
async def approve_product_submission(id: str, request: Request):
    user = await require_admin(request)
    try:
        supabase_admin.table("product_submissions").update({"status": "approved"}).eq("id", id).execute()
        _audit(user.email, "approve", "product_submission", id)
        return {"ok": True}
    except Exception as e:
        logger.error("approve_product_submission failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/product-submissions/{id}/reject")
async def reject_product_submission(id: str, request: Request):
    user = await require_admin(request)
    try:
        supabase_admin.table("product_submissions").update({"status": "rejected"}).eq("id", id).execute()
        _audit(user.email, "reject", "product_submission", id)
        return {"ok": True}
    except Exception as e:
        logger.error("reject_product_submission failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


class SaveSubmissionBody(BaseModel):
    name: str
    brand: Optional[str] = None
    category: Optional[str] = None
    ingredients_raw: str
    ingredients: list
    awareness_score: int
    images: Optional[list] = None
    image_url: Optional[str] = None
    summary: Optional[str] = None
    fssai_note: Optional[str] = None
    verdict: Optional[str] = None
    recommendation: Optional[str] = None
    barcode: Optional[str] = None


@router.post("/product-submissions/{id}/save")
async def save_product_from_submission(id: str, body: SaveSubmissionBody, request: Request):
    """Create an ai_extracted_products record from a submission and mark it extracted."""
    user = await require_admin(request)
    try:
        supabase_admin.table("ai_extracted_products").insert({
            "name":            body.name,
            "brand":           (body.brand or "")[:100] or None,
            "category":        body.category or "Personal Care",
            "image_url":       body.image_url,
            "images":          body.images or [],
            "awareness_score": body.awareness_score,
            "summary":         body.summary or "",
            "fssai_note":      body.fssai_note or "Subject to applicable FSSAI regulations.",
            "verdict":         body.verdict or "",
            "recommendation":  body.recommendation or "",
            "ingredients":     body.ingredients,
            "ingredients_raw": body.ingredients_raw[:5000],
            "submission_id":   id,
            "barcode":         body.barcode or None,
            "status":          "active",
        }).execute()

        res = supabase_admin.table("ai_extracted_products").select("id").eq("submission_id", id).order("created_at", desc=True).limit(1).execute()
        product_id = res.data[0]["id"] if res.data else None
        supabase_admin.table("product_submissions").update({"status": "extracted"}).eq("id", id).execute()

        _audit(user.email, "save_from_submission", "product_submission", id, {
            "product_name": body.name,
            "new_product_id": product_id,
            "grade": "computed_client_side",
            "ingredients_count": len(body.ingredients),
        })
        return {"ok": True, "product_id": product_id}
    except Exception as e:
        logger.error("save_product_from_submission failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Photo Submissions ──────────────────────────────────────────────────────────

class ApprovePhotoBody(BaseModel):
    product_id: str
    user_id: str
    image_urls: list[str]


@router.post("/photo-submissions/{id}/approve")
async def approve_photo_submission(id: str, body: ApprovePhotoBody, request: Request):
    user = await require_admin(request)
    try:
        inserts = [
            {"product_id": body.product_id, "image_url": url, "added_by": body.user_id, "is_admin_added": False}
            for url in body.image_urls
        ]
        supabase_admin.table("product_photos").insert(inserts).execute()
        supabase_admin.rpc("increment_earnings", {"uid": body.user_id, "amount": len(body.image_urls)}).execute()
        supabase_admin.table("product_photo_submissions").update({"status": "approved"}).eq("id", id).execute()

        _audit(user.email, "approve", "photo_submission", id, {
            "product_id": body.product_id,
            "photo_count": len(body.image_urls),
            "credited_user": body.user_id,
        })
        return {"ok": True}
    except Exception as e:
        logger.error("approve_photo_submission failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/photo-submissions/{id}/reject")
async def reject_photo_submission(id: str, request: Request):
    user = await require_admin(request)
    try:
        supabase_admin.table("product_photo_submissions").update({"status": "rejected"}).eq("id", id).execute()
        _audit(user.email, "reject", "photo_submission", id)
        return {"ok": True}
    except Exception as e:
        logger.error("reject_photo_submission failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Ingredient Reports ─────────────────────────────────────────────────────────

class ApproveReportBody(BaseModel):
    product_id: str
    product_name: str
    reported_ingredients: str
    is_uuid: bool


@router.post("/reports/{id}/approve")
async def approve_ingredient_report(id: str, body: ApproveReportBody, request: Request):
    user = await require_admin(request)
    try:
        def _merge(existing: str | None, reported: str) -> str:
            if not existing:
                return reported
            existing_parts = [p.strip().lower() for p in existing.split(",")]
            new_parts = [
                s for s in [p.strip() for p in reported.split(",")]
                if s and s.lower() not in existing_parts
            ]
            return existing + (", " + ", ".join(new_parts) if new_parts else "")

        if body.is_uuid:
            row = supabase_admin.table("ai_extracted_products").select("ingredients_raw").eq("id", body.product_id).limit(1).execute()
            current_raw = (row.data[0]["ingredients_raw"] if row.data else None)
            merged = _merge(current_raw, body.reported_ingredients)
            supabase_admin.table("ai_extracted_products").update({"ingredients_raw": merged, "ingredients": []}).eq("id", body.product_id).execute()
            updated_id = body.product_id
        else:
            found = supabase_admin.table("ai_extracted_products").select("id, ingredients_raw").ilike("name", body.product_name).limit(1).execute()
            if found.data:
                merged = _merge(found.data[0]["ingredients_raw"], body.reported_ingredients)
                supabase_admin.table("ai_extracted_products").update({"ingredients_raw": merged, "ingredients": []}).eq("id", found.data[0]["id"]).execute()
                updated_id = found.data[0]["id"]
            else:
                res = supabase_admin.table("ai_extracted_products").insert({
                    "name": body.product_name, "ingredients_raw": body.reported_ingredients, "ingredients": []
                }).select("id").execute()
                updated_id = res.data[0]["id"] if res.data else None

        now = datetime.datetime.utcnow().isoformat()
        supabase_admin.table("ingredient_reports").update({"status": "approved", "reviewed_at": now}).eq("id", id).execute()

        _audit(user.email, "approve", "ingredient_report", id, {
            "product_id": body.product_id,
            "product_name": body.product_name,
            "updated_product_id": str(updated_id),
        })
        return {"ok": True}
    except Exception as e:
        logger.error("approve_ingredient_report failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reports/{id}/reject")
async def reject_ingredient_report(id: str, request: Request):
    user = await require_admin(request)
    try:
        now = datetime.datetime.utcnow().isoformat()
        supabase_admin.table("ingredient_reports").update({"status": "rejected", "reviewed_at": now}).eq("id", id).execute()
        _audit(user.email, "reject", "ingredient_report", id)
        return {"ok": True}
    except Exception as e:
        logger.error("reject_ingredient_report failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Blogs ──────────────────────────────────────────────────────────────────────

class BlogStatusBody(BaseModel):
    status: str


@router.patch("/blogs/{id}/status")
async def update_blog_status(id: str, body: BlogStatusBody, request: Request):
    if body.status not in ("approved", "rejected", "pending"):
        raise HTTPException(status_code=400, detail="Invalid status")
    user = await require_admin(request)
    try:
        supabase_admin.table("blogs").update({"status": body.status}).eq("id", id).execute()
        _audit(user.email, f"blog_set_{body.status}", "blog", id)
        return {"ok": True}
    except Exception as e:
        logger.error("update_blog_status failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/blogs/{id}")
async def delete_blog(id: str, request: Request):
    user = await require_admin(request)
    try:
        row = supabase_admin.table("blogs").select("title, author_email").eq("id", id).limit(1).execute()
        meta = row.data[0] if row.data else {}
        supabase_admin.table("blogs").delete().eq("id", id).execute()
        _audit(user.email, "delete", "blog", id, {"title": meta.get("title"), "author": meta.get("author_email")})
        return {"ok": True}
    except Exception as e:
        logger.error("delete_blog failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Direct Product Insert (Admin Form) ────────────────────────────────────────

class InsertProductBody(BaseModel):
    name: str
    brand: Optional[str] = None
    category: str
    ingredients_raw: str
    ingredients: list
    grade: str
    static_key: str
    summary: str
    fssai_note: str
    verdict: str
    recommendation: str
    image_url: Optional[str] = None


@router.post("/products")
async def insert_product(body: InsertProductBody, request: Request):
    user = await require_admin(request)
    if body.grade not in ("A", "B", "C", "D"):
        raise HTTPException(status_code=400, detail="grade must be A/B/C/D")
    try:
        res = supabase_admin.table("ai_extracted_products").insert({
            "name":            body.name.strip(),
            "brand":           (body.brand or "").strip() or None,
            "category":        body.category,
            "ingredients_raw": body.ingredients_raw.strip(),
            "ingredients":     body.ingredients,
            "grade":           body.grade,
            "static_key":      body.static_key,
            "summary":         body.summary,
            "fssai_note":      body.fssai_note,
            "verdict":         body.verdict,
            "recommendation":  body.recommendation,
            "image_url":       body.image_url or None,
        }).select("id").execute()

        product_id = res.data[0]["id"] if res.data else None
        _audit(user.email, "insert", "product", product_id or "unknown", {
            "name": body.name, "grade": body.grade, "category": body.category
        })
        return {"id": product_id}
    except Exception as e:
        logger.error("insert_product failed name=%s: %s", body.name, e)
        raise HTTPException(status_code=500, detail=str(e))


# ── Barcode Submissions ────────────────────────────────────────────────────────

@router.get("/barcodes/pending")
async def get_pending_barcodes(request: Request):
    user = await require_admin(request)
    res = supabase_admin.table("barcode_submissions").select("*").eq("status", "pending").order("created_at", desc=True).execute()
    return res.data or []


@router.post("/barcodes/{id}/approve")
async def approve_barcode(id: str, request: Request):
    user = await require_admin(request)
    try:
        row = supabase_admin.table("barcode_submissions").select("*").eq("id", id).limit(1).execute()
        if not row.data:
            raise HTTPException(status_code=404, detail="Barcode submission not found")
        sub = row.data[0]

        now = datetime.datetime.utcnow().isoformat()
        supabase_admin.table("barcode_submissions").update({"status": "approved", "reviewed_at": now}).eq("id", id).execute()

        if sub.get("submitted_by"):
            try:
                supabase_admin.rpc("increment_earnings", {"uid": sub["submitted_by"], "amount": 1}).execute()
            except Exception as e:
                logger.warning("Failed to credit barcode reward: %s", e)

        _audit(user.email, "approve", "barcode_submission", id, {"barcode": sub["barcode"], "product_name": sub.get("product_name")})
        return {"ok": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("approve_barcode failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/barcodes/{id}/reject")
async def reject_barcode(id: str, request: Request):
    user = await require_admin(request)
    try:
        now = datetime.datetime.utcnow().isoformat()
        supabase_admin.table("barcode_submissions").update({"status": "rejected", "reviewed_at": now}).eq("id", id).execute()
        _audit(user.email, "reject", "barcode_submission", id)
        return {"ok": True}
    except Exception as e:
        logger.error("reject_barcode failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/products/{id}/image")
async def update_product_image(id: str, request: Request):
    user = await require_admin(request)
    data = await request.json()
    image_url = data.get("image_url", "").strip()
    if not image_url:
        raise HTTPException(status_code=400, detail="image_url required")
    try:
        supabase_admin.table("ai_extracted_products").update({"image_url": image_url}).eq("id", id).execute()
        _audit(user.email, "update_image", "product", id, {"image_url": image_url})
        return {"ok": True}
    except Exception as e:
        logger.error("update_product_image failed id=%s: %s", id, e)
        raise HTTPException(status_code=500, detail=str(e))
