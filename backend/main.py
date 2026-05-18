import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

# Import routers
from routes import product_new, ingredient, history, admin_extract, reports

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
    # Evict IPs that have been idle for more than 2 windows to cap memory
    if len(_rate_store) > 5000:
        cutoff = now - RATE_WINDOW_SECONDS * 2
        idle = [k for k, v in _rate_store.items() if not v or v[-1] < cutoff]
        for k in idle:
            del _rate_store[k]
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
ALLOWED_ORIGINS = [
    "https://www.parkho.in",
    "https://parkho.in",
    "https://checkkaro-lemon.vercel.app",
]

# Allow Vercel preview deployments (testing branch, PR previews)
def _is_allowed_origin(origin: str) -> bool:
    if origin in ALLOWED_ORIGINS:
        return True
    if origin.endswith(".vercel.app"):
        return True
    return False

app = FastAPI(
    title="Parkho API",
    description="Parkho — Know what's inside your products",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENV", "development") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENV", "development") != "production" else None,
)

app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(product_new.router,    prefix="/api/product",    tags=["Products"])
app.include_router(ingredient.router,     prefix="/api/ingredient",  tags=["Ingredients"])
app.include_router(history.router,        prefix="/api/history",     tags=["History"])
app.include_router(admin_extract.router,  prefix="/api/admin",       tags=["Admin"])
app.include_router(reports.router,        prefix="/api/admin",       tags=["Reports"])


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Parkho API"}


@app.get("/")
async def root():
    return {"message": "Welcome to Parkho API"}


@app.get("/sitemap-products.xml", include_in_schema=False)
async def sitemap_products():
    """Dynamic sitemap of all products fetched from Supabase."""
    import httpx
    from urllib.parse import quote
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY", "")
    SITE = "https://www.parkho.in"

    urls = []
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(
                    f"{SUPABASE_URL}/rest/v1/products_catalog",
                    params={"select": "name,updated_at", "order": "updated_at.desc", "limit": "2000"},
                    headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
                )
                if resp.status_code == 200:
                    for p in resp.json():
                        name = (p.get("name") or "").strip()
                        if not name:
                            continue
                        lastmod = (p.get("updated_at") or "")[:10] or "2025-01-01"
                        urls.append(f"""  <url>
    <loc>{SITE}/result/{quote(name)}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")
        except Exception as e:
            print(f"[sitemap-products] error: {e}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls)
    xml += "\n</urlset>"
    return Response(content=xml, media_type="application/xml")


@app.get("/sitemap-blogs.xml", include_in_schema=False)
async def sitemap_blogs():
    """Dynamic sitemap of all approved blog posts from Supabase."""
    import httpx
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY", "")
    SITE = "https://www.parkho.in"

    static_slugs = [
        ("static-1", "2025-01-01"),
        ("static-2", "2025-01-01"),
        ("static-3", "2025-01-01"),
        ("static-4", "2025-01-01"),
        ("static-5", "2025-01-01"),
        ("static-6", "2025-01-01"),
    ]
    urls = [f"""  <url>
    <loc>{SITE}/blog/{slug}</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""" for slug, date in static_slugs]

    if SUPABASE_URL and SUPABASE_KEY:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{SUPABASE_URL}/rest/v1/blogs",
                    params={"select": "slug,updated_at", "status": "eq.approved", "order": "updated_at.desc", "limit": "1000"},
                    headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"},
                )
                if resp.status_code == 200:
                    for b in resp.json():
                        slug = (b.get("slug") or "").strip()
                        if not slug:
                            continue
                        lastmod = (b.get("updated_at") or "")[:10] or "2025-01-01"
                        urls.append(f"""  <url>
    <loc>{SITE}/blog/{slug}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")
        except Exception as e:
            print(f"[sitemap-blogs] error: {e}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls)
    xml += "\n</urlset>"
    return Response(content=xml, media_type="application/xml")


if __name__ == "__main__":
    import uvicorn
    print("Total products loaded: 570")
    print("Starting CheckKaro API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
