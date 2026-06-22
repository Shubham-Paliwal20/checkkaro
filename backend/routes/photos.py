import logging
import re
import uuid
from fastapi import APIRouter, Request, HTTPException, UploadFile, File, Form
from typing import List, Optional
from pydantic import BaseModel
from db.supabase_client import supabase_admin
from utils.auth import get_current_user, require_admin

logger = logging.getLogger(__name__)
router = APIRouter()

BUCKET = "product-images"
MAX_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

# S3: map content-type → extension (never trust client filename)
_EXT_MAP = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}

_SAFE_ID  = re.compile(r'^[a-zA-Z0-9_\-]{1,128}$')
_UUID_RE  = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)

def _validate_product_id(pid: str) -> str:
    if not _SAFE_ID.match(pid):
        raise HTTPException(status_code=400, detail="Invalid product_id format")
    return pid

def _validate_uuid(val: str, label: str = "id") -> str:
    if not _UUID_RE.match(val):
        raise HTTPException(status_code=400, detail=f"Invalid {label} format")
    return val


# ── GET /api/photos/{product_id} ─────────────────────────────────────────────
@router.get("/{product_id}")
async def get_photos(product_id: str):
    """Return all approved photos for a product. Public."""
    product_id = _validate_product_id(product_id)  # S2 fix
    try:
        res = supabase_admin.table("product_photos") \
            .select("id, image_url, created_at") \
            .eq("product_id", product_id) \
            .order("created_at") \
            .execute()
        return {"photos": res.data or []}
    except Exception as e:
        logger.error("get_photos failed product_id=%s: %s", product_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch photos")  # S4 fix


# ── POST /api/photos/batch ────────────────────────────────────────────────────
class BatchRequest(BaseModel):
    ids: List[str]

@router.post("/batch")
async def get_photos_batch(body: BatchRequest):
    """Return first photo URL for each product_id in the list. Public."""
    if not body.ids:
        return {"photos": []}
    # Validate and cap IDs to prevent abuse (S10)
    safe_ids = [_validate_product_id(i) for i in body.ids[:50]]
    try:
        res = supabase_admin.table("product_photos") \
            .select("product_id, image_url") \
            .in_("product_id", safe_ids) \
            .order("created_at") \
            .execute()
        return {"photos": res.data or []}
    except Exception as e:
        logger.error("get_photos_batch failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to fetch photos")  # S4 fix


# ── POST /api/photos/upload  (admin only) ────────────────────────────────────
@router.post("/upload")
async def upload_photos(
    request: Request,
    product_id: str = Form(...),
    files: List[UploadFile] = File(...),
):
    """Admin: upload files to Supabase Storage and insert rows to product_photos."""
    user = await require_admin(request)
    product_id = _validate_product_id(product_id)

    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    uploaded = []
    for f in files:
        if f.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {f.content_type}")
        data = await f.read()
        if len(data) > MAX_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="File exceeds 8 MB limit")

        # S3: derive extension from validated content-type, never from filename
        ext = _EXT_MAP[f.content_type]
        path = f"{product_id}/{uuid.uuid4().hex}.{ext}"

        try:
            supabase_admin.storage.from_(BUCKET).upload(
                path=path,
                file=data,
                file_options={"content-type": f.content_type, "upsert": "false"},
            )
        except Exception as e:
            logger.error("Storage upload failed path=%s: %s", path, e)
            raise HTTPException(status_code=500, detail="Storage upload failed")  # S4 fix

        public_url = supabase_admin.storage.from_(BUCKET).get_public_url(path)
        uploaded.append({"url": public_url, "path": path})

    rows = [
        {
            "product_id": product_id,
            "image_url": u["url"],
            "storage_path": u["path"],
            "added_by": str(user.id),
            "is_admin_added": True,
        }
        for u in uploaded
    ]
    try:
        supabase_admin.table("product_photos").insert(rows).execute()
    except Exception as e:
        logger.error("product_photos insert failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to save photo records")  # S4 fix

    try:
        supabase_admin.table("ai_extracted_products") \
            .update({"image_url": uploaded[0]["url"]}) \
            .eq("id", product_id) \
            .execute()
    except Exception:
        pass  # non-fatal — primary image update is best-effort

    return {"uploaded": uploaded}


# ── POST /api/photos/submit  (logged-in users) ───────────────────────────────
@router.post("/submit")
async def submit_photos(
    request: Request,
    product_id: str = Form(...),
    product_name: str = Form(...),
    upi_or_mobile: str = Form(...),
    files: List[UploadFile] = File(...),
):
    """User: upload photos as a submission for admin review."""
    user = await get_current_user(request)
    product_id = _validate_product_id(product_id)

    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Please upload at least 2 photos (front and back)")
    if not upi_or_mobile.strip():
        raise HTTPException(status_code=400, detail="UPI ID or mobile number is required")

    uploaded_urls = []
    for f in files:
        if f.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {f.content_type}")
        data = await f.read()
        if len(data) > MAX_SIZE_BYTES:
            raise HTTPException(status_code=400, detail="File exceeds 8 MB limit")

        # S3: derive extension from content-type
        ext = _EXT_MAP[f.content_type]
        path = f"submissions/{product_id}/{uuid.uuid4().hex}.{ext}"

        try:
            supabase_admin.storage.from_(BUCKET).upload(
                path=path,
                file=data,
                file_options={"content-type": f.content_type, "upsert": "false"},
            )
        except Exception as e:
            logger.error("Submission storage upload failed path=%s: %s", path, e)
            raise HTTPException(status_code=500, detail="Storage upload failed")  # S4 fix

        uploaded_urls.append(supabase_admin.storage.from_(BUCKET).get_public_url(path))

    try:
        supabase_admin.table("product_photo_submissions").insert({
            "product_id": product_id,
            "product_name": product_name[:200],  # cap length
            "user_id": str(user.id),
            "image_urls": uploaded_urls,
            "upi_or_mobile": upi_or_mobile.strip()[:50],  # cap length
            "status": "pending",
        }).execute()
    except Exception as e:
        logger.error("product_photo_submissions insert failed user=%s: %s", user.id, e)
        raise HTTPException(status_code=500, detail="Submission failed")  # S4 fix

    return {"message": "Submitted! You will earn ₹1 after admin approves your photos."}


# ── DELETE /api/photos/{photo_id}  (admin only) ──────────────────────────────
@router.delete("/{photo_id}")
async def delete_photo(photo_id: str, request: Request):
    """Admin: delete a photo row and its object from Storage."""
    await require_admin(request)
    _validate_uuid(photo_id, "photo_id")  # S9 fix — reject non-UUID before hitting DB
    try:
        row = supabase_admin.table("product_photos").select("storage_path").eq("id", photo_id).execute()
        storage_path = (row.data or [{}])[0].get("storage_path") if row.data else None
        supabase_admin.table("product_photos").delete().eq("id", photo_id).execute()
        if storage_path:
            try:
                supabase_admin.storage.from_(BUCKET).remove([storage_path])
            except Exception:
                pass  # row is gone; storage cleanup is best-effort
        return {"deleted": photo_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("delete_photo failed photo_id=%s: %s", photo_id, e)
        raise HTTPException(status_code=500, detail="Failed to delete photo")  # S4 fix


# ── PATCH /api/photos/primary  (admin only) ──────────────────────────────────
class PrimaryImageBody(BaseModel):
    product_id: str
    image_url: Optional[str] = None
    images: Optional[List[str]] = None

@router.patch("/primary")
async def set_primary_image(body: PrimaryImageBody, request: Request):
    """Admin: update the primary image_url on ai_extracted_products."""
    await require_admin(request)
    _validate_product_id(body.product_id)
    update = {}
    if body.image_url is not None:
        update["image_url"] = body.image_url
    if body.images is not None:
        update["images"] = body.images if body.images else None
    if not update:
        raise HTTPException(status_code=400, detail="Nothing to update")
    try:
        supabase_admin.table("ai_extracted_products") \
            .update(update) \
            .eq("id", body.product_id) \
            .execute()
        return {"updated": body.product_id}
    except Exception as e:
        logger.error("set_primary_image failed product_id=%s: %s", body.product_id, e)
        raise HTTPException(status_code=500, detail="Failed to update primary image")  # S4 fix
