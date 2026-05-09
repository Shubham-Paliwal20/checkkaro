import os
import uuid
import threading
from fastapi import APIRouter, HTTPException, Header, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
from db.supabase_client import supabase, supabase_admin
from services.gemini_service import extract_ingredients_from_image, analyze_ingredients_list as analyze_ingredients
from routes.product_new import invalidate_browse_cache

router = APIRouter()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")

# In-memory task store — fine for single-instance Render free tier
# { task_id: { "status": "processing"|"done"|"error", "result": {...}, "error": "..." } }
_tasks: dict = {}
_TASK_LIMIT = 200  # keep at most this many completed tasks in memory

def _prune_tasks() -> None:
    if len(_tasks) <= _TASK_LIMIT:
        return
    # Drop the oldest half — keys are insertion-ordered in Python 3.7+
    keys = list(_tasks.keys())
    for k in keys[:len(keys) // 2]:
        del _tasks[k]


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


class ExtractRequest(BaseModel):
    submission_id: str
    ingredients_text: Optional[str] = None  # if set, skip Claude Vision


async def _do_extract(task_id: str, sub: dict, manual_text: Optional[str]) -> None:
    """Background coroutine — runs after response is returned to client."""
    try:
        images: list = sub.get("images") or []
        product_name: str = (sub.get("product_name_searched") or "Unknown Product")[:200]

        # ── Determine ingredients text ────────────────────────────────────────
        if manual_text and manual_text.strip():
            ingredients_text = manual_text.strip()
            print(f"[EXTRACT-MANUAL] {product_name} | {len(ingredients_text)} chars")
        else:
            if not images:
                _tasks[task_id] = {"status": "error", "error": "No images in submission. Use manual text entry."}
                return

            # Try back-label (index 1) first, then front, then rest
            ordered = ([images[1]] if len(images) > 1 else []) + [images[0]] + images[2:]
            ingredients_text = "NOT_VISIBLE"
            for url in ordered:
                text = await extract_ingredients_from_image(url, product_name)
                if text and text != "NOT_VISIBLE":
                    ingredients_text = text
                    break

            if ingredients_text == "NOT_VISIBLE":
                _tasks[task_id] = {
                    "status": "error",
                    "error": "Could not read ingredients from any image. Use 'Enter manually' and paste the label text.",
                }
                return

            print(f"[EXTRACT-VISION] {product_name} | {len(ingredients_text)} chars")

        # ── Classify with Claude ──────────────────────────────────────────────
        analysis = await analyze_ingredients(product_name, ingredients_text)

        product_data = {
            "name": product_name,
            "brand": (analysis.get("brand") or "Unknown")[:100],
            "category": (analysis.get("category") or "General")[:100],
            "image_url": images[0] if images else None,
            "images": images,
            "awareness_score": max(0, min(100, int(analysis.get("awareness_score") or 50))),
            "summary": (analysis.get("summary") or "")[:2000],
            "fssai_note": (analysis.get("fssai_note") or "")[:500],
            "verdict": (analysis.get("verdict") or "")[:200],
            "recommendation": (analysis.get("recommendation") or "")[:500],
            "ingredients": analysis.get("ingredients") or [],
            "ingredients_raw": ingredients_text[:5000],
            "submission_id": sub["id"],
            "status": "active",
        }

        insert_res = supabase.from_("ai_extracted_products").insert(product_data).execute()
        if not insert_res.data:
            _tasks[task_id] = {"status": "error", "error": "Failed to save to database."}
            return

        supabase.from_("product_submissions").update({"status": "extracted"}).eq("id", sub["id"]).execute()
        invalidate_browse_cache()  # new product — flush stale browse results

        _tasks[task_id] = {
            "status": "done",
            "result": {
                "product_name": product_name,
                "brand": analysis.get("brand"),
                "awareness_score": analysis.get("awareness_score"),
                "ingredients_count": len(analysis.get("ingredients") or []),
            },
        }
        _prune_tasks()

    except Exception as e:
        print(f"[EXTRACT ERROR] task={task_id} | {e}")
        _tasks[task_id] = {"status": "error", "error": str(e)}
        _prune_tasks()


@router.post("/extract-product")
async def extract_product(
    req: ExtractRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    result = supabase.from_("product_submissions").select("*").eq("id", req.submission_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Submission not found")

    task_id = str(uuid.uuid4())
    _tasks[task_id] = {"status": "processing"}

    background_tasks.add_task(_do_extract, task_id, result.data, req.ingredients_text)

    # Returns immediately — client polls /task/{task_id} for completion
    return {"task_id": task_id, "status": "processing"}


@router.get("/task/{task_id}")
async def get_task_status(
    task_id: str,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)
    task = _tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or expired")
    return task


@router.delete("/product/{product_id}")
async def delete_product(
    product_id: str,
    authorization: Optional[str] = Header(None),
):
    _verify_admin(authorization)

    import os
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not service_key:
        raise HTTPException(status_code=500, detail="SUPABASE_SERVICE_ROLE_KEY not configured on server — cannot bypass RLS")

    # Confirm the row exists first
    check = supabase_admin.from_("ai_extracted_products").select("id, name").eq("id", product_id).execute()
    if not check.data:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found in database")

    product_name = check.data[0].get("name", product_id)
    print(f"[DELETE] Deleting product: {product_name} ({product_id})")

    try:
        supabase_admin.from_("ai_extracted_products").delete().eq("id", product_id).execute()
    except Exception as e:
        print(f"[DELETE ERROR] {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

    # Verify the row is actually gone
    verify = supabase_admin.from_("ai_extracted_products").select("id").eq("id", product_id).execute()
    if verify.data:
        print(f"[DELETE FAIL] Row still exists after delete — RLS may be blocking even admin client")
        raise HTTPException(status_code=500, detail="Delete command ran but row still exists. Check Supabase RLS policies.")

    invalidate_browse_cache()  # deleted product — flush stale browse results
    print(f"[DELETE OK] {product_name} ({product_id})")
    return {"success": True, "deleted": product_id, "name": product_name}


# ── Regrade all products ───────────────────────────────────────────────────────
_regrade_status: dict = {"running": False, "processed": 0, "updated": 0, "done": False, "error": ""}

@router.post("/regrade-all")
async def regrade_all(authorization: Optional[str] = Header(None)):
    """Recompute grades for every product using current classification rules."""
    _verify_admin(authorization)

    if _regrade_status["running"]:
        return {"status": "already_running", **_regrade_status}

    def _run():
        from backfill_grades import run_backfill
        _regrade_status.update({"running": True, "processed": 0, "updated": 0, "done": False, "error": ""})
        try:
            result = run_backfill(log=lambda msg: print(f"[REGRADE] {msg}"))
            _regrade_status.update({"running": False, "done": True, **result})
            invalidate_browse_cache()
        except Exception as e:
            _regrade_status.update({"running": False, "done": True, "error": str(e)})

    threading.Thread(target=_run, daemon=True).start()
    return {"status": "started"}

@router.get("/regrade-status")
async def regrade_status(authorization: Optional[str] = Header(None)):
    _verify_admin(authorization)
    return _regrade_status
