import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

# Import routers
from routes import product_new, ingredient, history, admin_extract

load_dotenv()

# ── Rate limiter (in-memory, per IP) ──────────────────────────────────────────
# Slots: { ip: [timestamp, ...] }
_rate_store: dict = defaultdict(list)

RATE_LIMIT_NORMAL   = 60   # requests per window per IP
RATE_LIMIT_ADMIN    = 60   # admin endpoints protected by JWT; no extra IP throttle needed
RATE_WINDOW_SECONDS = 60


def _is_rate_limited(ip: str, max_calls: int) -> bool:
    now = time.monotonic()
    window_start = now - RATE_WINDOW_SECONDS
    timestamps = [t for t in _rate_store[ip] if t > window_start]
    _rate_store[ip] = timestamps
    if len(timestamps) >= max_calls:
        return True
    _rate_store[ip].append(now)
    return False


# ── Security headers middleware ────────────────────────────────────────────────
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"]    = "nosniff"
        response.headers["X-Frame-Options"]           = "DENY"
        response.headers["X-XSS-Protection"]          = "1; mode=block"
        response.headers["Referrer-Policy"]           = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"]        = "geolocation=(), camera=(), microphone=()"
        # Only set HSTS on HTTPS (not localhost dev)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


# ── Rate limiting middleware ───────────────────────────────────────────────────
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Behind Render/Vercel proxies the real IP is in X-Forwarded-For
        forwarded = request.headers.get("x-forwarded-for")
        ip = (forwarded.split(",")[0].strip() if forwarded
              else (request.client.host if request.client else "unknown"))

        # Tighter limit for admin / extraction endpoints
        is_admin = request.url.path.startswith("/api/admin")
        limit = RATE_LIMIT_ADMIN if is_admin else RATE_LIMIT_NORMAL

        if _is_rate_limited(ip, limit):
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please slow down."},
            )
        return await call_next(request)


# ── App setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CheckKaro API",
    description="Indian product ingredient awareness platform",
    version="1.0.0",
    # Disable automatic OpenAPI docs in production
    docs_url="/docs" if os.getenv("ENV", "development") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENV", "development") != "production" else None,
)

# CORS — open to all origins; auth is enforced via JWT bearer tokens, not cookies
# allow_credentials must be False when allow_origins=["*"] (CORS spec requirement)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(product_new.router,    prefix="/api/product",    tags=["Products"])
app.include_router(ingredient.router,     prefix="/api/ingredient",  tags=["Ingredients"])
app.include_router(history.router,        prefix="/api/history",     tags=["History"])
app.include_router(admin_extract.router,  prefix="/api/admin",       tags=["Admin"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "CheckKaro API"}


@app.get("/")
async def root():
    return {"message": "Welcome to CheckKaro API"}


if __name__ == "__main__":
    import uvicorn
    print("Total products loaded: 570")
    print("Starting CheckKaro API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
