import os
from fastapi import HTTPException, Request
from db.supabase_client import supabase_admin

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "shubhampaliwal5@gmail.com")


async def get_current_user(request: Request):
    """Verify Supabase JWT from Authorization header. Returns user object or raises 401."""
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth[7:].strip()
    try:
        resp = supabase_admin.auth.get_user(token)
        if not resp or not resp.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return resp.user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token verification failed")


async def require_admin(request: Request):
    """Verify JWT and confirm the caller is the admin account."""
    user = await get_current_user(request)
    if user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
