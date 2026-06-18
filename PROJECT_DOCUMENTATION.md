# Parkho (CheckKaro) — Project Documentation

> **For new developers joining the project.**
> This document covers architecture, codebase structure, data flow, and how to run the project locally.

---

## Table of Contents

1. [What Is This App?](#1-what-is-this-app)
2. [Tech Stack](#2-tech-stack)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Repository Structure](#4-repository-structure)
5. [Backend — FastAPI](#5-backend--fastapi)
6. [Frontend — React](#6-frontend--react)
7. [Database — Supabase](#7-database--supabase)
8. [Ingredient Classification Engine](#8-ingredient-classification-engine)
9. [Grading System](#9-grading-system)
10. [Authentication](#10-authentication)
11. [Admin Panel](#11-admin-panel)
12. [Deployment](#12-deployment)
13. [Local Setup Guide](#13-local-setup-guide)
14. [Key Concepts for New Developers](#14-key-concepts-for-new-developers)
15. [What NOT to Touch](#15-what-not-to-touch)

---

## 1. What Is This App?

**Parkho** (formerly CheckKaro) is an ingredient awareness platform for Indian consumers. Users can:

- Search any food or cosmetic product by name
- See a **Grade (A / B / C / D)** based on the ingredient list
- Understand what each ingredient is — in plain English with scientific detail
- Check any ingredient individually (Check Ingredient page)
- Submit new products for review
- Upload product photos
- Read blogs about ingredient safety

The app is live at **parkho.in** and is targeted at Indian consumers using FSSAI-aligned ingredient data.

---

## 2. Tech Stack

| Layer | Technology | Hosted On |
|---|---|---|
| Frontend | React 18 + Vite + Tailwind CSS | Vercel |
| Backend | FastAPI (Python 3.11) | Render |
| Database | PostgreSQL via Supabase | Supabase |
| Auth | Supabase Auth (email OTP) | Supabase |
| File Storage | Supabase Storage | Supabase |
| AI Extraction | Google Gemini (image → ingredients) | Google Cloud |

---

## 3. High-Level Architecture

```
User's Browser
      │
      ├─── React Frontend (Vercel)
      │         │
      │         ├── axios → FastAPI Backend (Render)
      │         │               │
      │         │               ├── ingredient_database.py  ← Classification engine
      │         │               ├── grading.py              ← A/B/C/D logic
      │         │               └── Supabase PostgreSQL     ← Product data
      │         │
      │         └── Supabase JS client (anon key)
      │                   │
      │                   ├── Auth (login / signup)
      │                   ├── product_photos (read)
      │                   └── product_reviews (read/write)
      │
Admin Browser
      │
      └── Admin page → FastAPI /api/admin (JWT required)
                              │
                              └── Google Gemini (image extraction)
```

**Key design decision:** The backend is the primary source of product data. The frontend has a direct Supabase fallback (only for reading product data) if the backend is slow or unavailable (Render free tier cold starts).

---

## 4. Repository Structure

```
checkkaro/
├── backend/                    ← FastAPI Python app
│   ├── main.py                 ← App entry point, middleware, routers
│   ├── grading.py              ← Grade calculation (A/B/C/D)
│   ├── requirements.txt
│   ├── db/
│   │   └── supabase_client.py  ← Two Supabase connections
│   ├── models/
│   │   └── schemas.py          ← Pydantic request/response models
│   ├── routes/
│   │   ├── product_new.py      ← ACTIVE: all product endpoints
│   │   ├── ingredient.py       ← Ingredient search endpoints
│   │   ├── ingredient_database.py  ← 5500-line classification engine
│   │   ├── admin_extract.py    ← Admin: Gemini extraction + product CRUD
│   │   ├── reports.py          ← Admin: ingredient report review
│   │   └── history.py          ← Search history (stub)
│   └── services/               ← External API clients (Gemini, etc.)
│
├── frontend/                   ← React Vite app
│   ├── src/
│   │   ├── App.jsx             ← Router setup
│   │   ├── context/
│   │   │   └── AuthContext.jsx ← Global auth state
│   │   ├── lib/
│   │   │   └── supabaseClient.js ← Frontend Supabase client
│   │   ├── pages/              ← 9 full pages
│   │   └── components/         ← 17 reusable components
│   ├── package.json
│   └── vite.config.js
│
└── _saved_recommendations_feature.md  ← Saved feature code for later
```

---

## 5. Backend — FastAPI

### Entry Point: `main.py`

Handles:
- **Rate limiting** — 60 requests/minute per IP (in-memory sliding window)
- **Security headers** — X-Frame-Options, X-Content-Type-Options, HSTS, etc.
- **CORS** — allows parkho.in and Vercel preview URLs
- **GZip compression** on all responses
- **Sitemap generation** — `/sitemap-products.xml`, `/sitemap-blogs.xml`
- **Health check** — `GET /health` (used by uptime monitor to keep Render awake)

### Active Routes

| Mount Path | File | Purpose |
|---|---|---|
| `/api/product` | `product_new.py` | Product search, browse, suggestions |
| `/api/ingredient` | `ingredient.py` | Ingredient lookup and list |
| `/api/admin` | `admin_extract.py` + `reports.py` | Admin-only operations |
| `/api/history` | `history.py` | Stub — returns empty list |

### Product Endpoints (`/api/product`)

**`GET /api/product/search?name=`**
The most important endpoint. Called every time a user views a product page.

Flow:
1. Check in-memory search cache (5 min TTL, 500 entries)
2. Query `ai_extracted_products` using multi-strategy fuzzy matching:
   - Exact `static_key` match
   - Hyphenated `static_key` match
   - Exact name (case-insensitive)
   - Prefix match (`name%`)
   - Word pattern (`%word1%word2%`)
   - Substring match (`%name%`)
3. If stored ingredients exist → use them directly (fast path)
4. If not → classify all ingredients from scratch and store for next time
5. Compute grade, build response, cache it, return

**`GET /api/product/browse`**
Paginated product listing. Filters: `category`, `brand`, `q` (search), `sort`. Results cached per filter combo for 2 minutes.

**`GET /api/product/suggest?q=`**
Typeahead suggestions — returns product names matching the query. Cached 5 minutes.

**`GET /api/product/brands`** / **`GET /api/product/categories`**
Returns distinct brand/category lists for filter dropdowns.

### Ingredient Endpoints (`/api/ingredient`)

**`GET /api/ingredient/check?name=`**
Looks up an ingredient in the in-code `INGREDIENT_DESCRIPTIONS` dictionary, returns its classification, description, health effects, related ingredients, and recommendation (if applicable).

**`GET /api/ingredient/list`**
Returns paginated list of all known ingredients.

### Caching Architecture

Three in-memory caches in the backend (reset on each deploy):

| Cache | TTL | Max Size | Purpose |
|---|---|---|---|
| `_search_cache` | 5 min | 500 products | Full product search results |
| `_browse_cache` | 2 min | 80 filter combos | Paginated browse results |
| `_suggest_cache` | 5 min | 200 queries | Autocomplete suggestions |

---

## 6. Frontend — React

### Pages

| Route | File | Description |
|---|---|---|
| `/` | `Home.jsx` | Landing page with search bar and reviews |
| `/products` | `Products.jsx` | Browse/filter all products |
| `/result/:name` | `Result.jsx` | Product detail page (core page) |
| `/check-ingredient` | `CheckIngredient.jsx` | Standalone ingredient lookup |
| `/admin` | `Admin.jsx` | Admin dashboard (restricted) |
| `/blog` | `Blog.jsx` | Blog listing |
| `/blog/:slug` | `BlogPost.jsx` | Single blog post |
| `/write-blog` | `WriteBlog.jsx` | User blog submission form |
| `/about` | `About.jsx` | About/mission page |

### Key Components

| Component | What It Does |
|---|---|
| `SearchBar.jsx` | Main search input with autocomplete; navigates to `/result/:name` |
| `GradeBadge.jsx` | Shows A/B/C/D grade as a colored pill |
| `IngredientColumns.jsx` | Three-column ingredient layout (GR / WK / CQ) |
| `ProductReviews.jsx` | Star rating + comment widget per product |
| `AuthModal.jsx` | Login / signup modal (Supabase email OTP) |
| `AddProductModal.jsx` | Form to submit a new product for review |
| `PhotoUploadModal.jsx` | Upload a product photo |
| `ProductNotFound.jsx` | Shown when search finds nothing; lets user submit the product |
| `SEO.jsx` | Sets page title and meta tags |

### Data Flow in `Result.jsx` (Product Detail Page)

```
User navigates to /result/maggi-masala-noodles
        │
        ├─ 1. Try axios GET /api/product/search?name=maggi...
        │         └─ Success → render product
        │
        └─ 2. Fallback: Supabase JS direct query on ai_extracted_products
                  (multi-strategy: exact → prefix → word → substring)
                  └─ Success → render product with stored classification
```

The fallback exists because Render free tier can have cold starts (backend sleeping after 15 min idle).

---

## 7. Database — Supabase

### Primary Table: `ai_extracted_products`

This is the table the live app reads from. Every product query hits this table.

| Column | Type | Description |
|---|---|---|
| `id` | uuid | Primary key |
| `name` | text | Product name |
| `brand` | text | Brand name |
| `category` | text | Product category |
| `grade` | text | A / B / C / D |
| `ingredients_raw` | text | Raw ingredient string from label |
| `ingredients` | jsonb | Pre-classified ingredient array |
| `image_url` | text | Primary product image URL |
| `static_key` | text | URL-friendly slug (e.g. `maggi-masala-noodles`) |
| `summary` | text | Auto-generated product summary |
| `fssai_note` | text | FSSAI regulatory note |

### Other Tables

| Table | Purpose |
|---|---|
| `product_photos` | Multiple photos per product (user-uploaded) |
| `product_submissions` | User-submitted new products (pending admin review) |
| `product_photo_submissions` | User-submitted photos (pending review) |
| `ingredient_reports` | User-reported ingredient corrections |
| `user_profiles` | One row per user — email, quiz answers |
| `product_reviews` | Star ratings + comments (one per user per product) |
| `reviews` | General site testimonials shown on Home page |
| `blogs` | Blog posts (pending/approved status) |

### Two Database Connections

The backend uses two Supabase clients with different permission levels:

- **`supabase`** — uses the `anon` key. Used for all read queries. Safe to use for user-facing data.
- **`supabase_admin`** — uses the `service_role` key. Bypasses Row Level Security. Used only for admin writes (inserting products, approving reports). Lives only on the server, never in frontend code.

### Row Level Security

All tables have RLS enabled. Key policies:
- `ai_extracted_products` — anyone can read, only admin can update
- `product_photos` — anyone can read, admin only for all writes
- `product_reviews` — authenticated users can read/write their own reviews
- `user_profiles` — users can only see their own profile

---

## 8. Ingredient Classification Engine

The heart of the app. Lives in `backend/routes/ingredient_database.py` (~5500 lines).

### Three Classification Tiers

| Tier | Color | Meaning |
|---|---|---|
| `generally_recognised` | Green | Safe, no known concerns at normal use levels |
| `worth_knowing` | Amber | Permitted but has some research concerns or restrictions |
| `commonly_questioned` | Red | Flagged, restricted, or banned in one or more countries |

### How Classification Works

`classify_ingredient(ingredient_name)` is called for every ingredient in every product:

1. **Pre-checks** — safe food enzymes (amylase, protease, lipase), safe cosmetic bases
2. **E-number lookup** — `e621` → MSG → `worth_knowing`
3. **Pattern matching** — checks ingredient name against 300+ curated patterns in priority order
4. **`INGREDIENT_DESCRIPTIONS` lookup** — 1000+ ingredients with 500-900 char scientific descriptions
5. **Generic category handling** — `emulsifiers`, `stabilizers` etc. → `worth_knowing` with undisclosed warning
6. **Default** → `generally_recognised`

### Undisclosed Ingredient Warning

When a brand writes "Emulsifiers" or "Flavourings" without naming specific compounds, the engine returns a `recommendation` field:

> "Brand has not fully disclosed this ingredient. Specific compounds cannot be independently assessed — use with caution, especially if you have allergies or sensitivities."

This is shown as an amber warning banner on the product page.

### `get_ingredient_details(ingredient_name)`

Extended version used by the Check Ingredient page. Returns everything above plus:
- `commonly_found_in` — product types where it appears
- `health_effects` — dict of effects
- `countries_restricted` — list of countries with restrictions
- `fssai_position` — India-specific regulatory note
- `related_ingredients` — 6 similar ingredients to explore
- `recommendation` — caution advice if applicable

---

## 9. Grading System

Defined in `backend/grading.py`. Pure Python, no AI, completely deterministic.

```
Input: list of ingredient objects, each with a "classification" field

Rules (evaluated in order):
  1. ANY "commonly_questioned" ingredient → Grade D
  2. ZERO "worth_knowing" ingredients   → Grade A
  3. "worth_knowing" ≤ 30% of total     → Grade B
  4. "worth_knowing" > 30% of total     → Grade C
```

| Grade | Label | Meaning |
|---|---|---|
| A | Excellent | All ingredients generally recognised as safe |
| B | Good | Mostly clean — a few worth-knowing additives (≤30%) |
| C | Average | Many worth-knowing additives (>30%) |
| D | Poor | Contains commonly questioned or restricted ingredients |

---

## 10. Authentication

Handled entirely by **Supabase Auth** (email OTP / magic link).

- `AuthContext.jsx` — wraps the entire app, provides `user`, `profile`, `openAuthModal()` to all components
- `AuthModal.jsx` — the login/signup UI
- On login: creates/updates a `user_profiles` row with the user's ID and email
- Admin check: `user.email === ADMIN_EMAIL` (hardcoded in the frontend)
- Admin API: backend verifies the JWT from Supabase and checks email claim

---

## 11. Admin Panel

Located at `/admin`. Only accessible to the admin email account.

Capabilities:
- **Review product submissions** — approve, reject, or "extract" (run Gemini AI on product image to get ingredients)
- **Review photo submissions** — approve or reject user-uploaded product photos
- **Review ingredient reports** — approve corrections (updates the live product) or reject
- **Edit any product** — name, brand, category, image, ingredients
- **Blog management** — approve, reject, or delete blog posts

### How Product Extraction Works (Admin Flow)

```
Admin uploads product image URL
        │
        └─ POST /api/admin/extract
                  │
                  └─ Google Gemini Vision API
                            │
                            └─ Returns ingredient list as text
                                      │
                                      └─ Saved to ai_extracted_products
                                                │
                                                └─ Classification + grade computed
                                                   on next search request
```

---

## 12. Deployment

### Backend (Render)

- Platform: Render Web Service (free tier)
- Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Auto-deploys on push to `main` branch of GitHub
- Environment variables set in Render dashboard (never committed to git)
- Free tier limitation: server sleeps after 15 min idle, takes ~5-10s to wake up
- Health endpoint `/health` is pinged every 5 minutes by UptimeRobot to prevent sleeping

### Frontend (Vercel)

- Platform: Vercel (free tier)
- Auto-deploys on push to `main` branch
- Environment variables set in Vercel dashboard
- Build command: `npm run build` (Vite)
- Output directory: `dist/`

### Git Workflow

- `main` branch = production (auto-deploys to both Render and Vercel)
- `testing` branch = staging (test before merging to main)
- Always push to `testing` first, verify, then merge to `main`

---

## 13. Local Setup Guide

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Backend

```bash
cd checkkaro/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example, fill in values)
cp .env.example .env

# Run
uvicorn main:app --reload --port 8000
```

Backend runs at `http://localhost:8000`
API docs at `http://localhost:8000/docs` (only in non-production mode)

### Frontend

```bash
cd checkkaro/frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Set VITE_API_BASE_URL=http://localhost:8000
# Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY

# Run
npm run dev
```

Frontend runs at `http://localhost:5173`

### Required Environment Variables

**Backend `.env`:**
```
SUPABASE_URL=           # Your Supabase project URL
SUPABASE_KEY=           # Supabase anon key (public)
SUPABASE_SERVICE_KEY=   # Supabase service role key (keep secret)
GEMINI_API_KEY=         # Google Gemini API key
ADMIN_EMAIL=            # Admin email address
ENV=development
```

**Frontend `.env`:**
```
VITE_API_BASE_URL=      # Backend URL
VITE_SUPABASE_URL=      # Supabase project URL
VITE_SUPABASE_ANON_KEY= # Supabase anon key (public, safe to expose)
```

---

## 14. Key Concepts for New Developers

### "Static Key" vs Product Name
`static_key` is a normalized slug (e.g. `maggi2minutenoodles`) used for fast exact-match lookups. Not all products have one. Products with a `static_key` are considered "verified" — the `data_source` field shows `"database_verified"`.

### Why Two Supabase Clients?
- `supabase` (anon key) — same permissions as a logged-out browser user. Safe for reads.
- `supabase_admin` (service_role key) — bypasses all RLS. Used only for admin writes. Never sent to the browser.

### Why Is `ingredient_database.py` in the `routes/` folder?
Historical accident. It's not a router — it's a pure data module (classification engine + description dictionary). It just ended up there during development. Don't move it without updating all imports.

### Why Are There Two Product Tables?
`ai_extracted_products` is the **active** table. `products_catalog` and `products` are **legacy** tables from earlier iterations of the app. All live traffic reads from `ai_extracted_products`. The legacy tables are kept for reference only.

### What Is `reparse_all_products.py`?
A local script (not on the server) that reads all products from `ai_extracted_products`, re-classifies every ingredient using the current `ingredient_database.py`, and writes updated grades and classified ingredients back to Supabase. Run this after making significant changes to the classification engine to ensure all stored products reflect the latest rules.

### The Frontend Fallback
`Result.jsx` has a built-in fallback: if the backend API call fails, it queries Supabase directly using the JS client. This means users still see product data even when Render is cold-starting. The fallback uses stored `ingredients` JSON (pre-classified) so it doesn't need the backend classification engine.

---

## 15. What NOT to Touch

| Thing | Why |
|---|---|
| `ingredient_database.py` classification order | Patterns are checked in priority order. Changing the order can mis-classify hundreds of ingredients. |
| `grading.py` grade thresholds | Changing 30% threshold re-grades all 1600+ products. Run `reparse_all_products.py` after. |
| Supabase `service_role` key | Must only live in backend `.env` and Render environment variables. Never in frontend code. |
| `main` branch | Direct pushes to main deploy to production. Always use `testing` branch first. |
| `_BANNED` and `_QUESTIONED` lists in `product_new.py` | These drive Grade D assignments. Adding a common ingredient here will downgrade many products. |

---

*Last updated: June 2026*
*Project by: Shubham Paliwal*
