# CheckKaro System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│                    http://localhost:5173                         │
├─────────────────────────────────────────────────────────────────┤
│  Pages:                                                          │
│  • Home.jsx          - Landing page with search                 │
│  • Result.jsx        - Product analysis results                 │
│  • CheckIngredient   - Individual ingredient lookup             │
│  • Products          - Browse products                          │
│  • About             - About page                               │
│                                                                  │
│  Components:                                                     │
│  • SearchBar         - Product search input                     │
│  • ScoreCircle       - Awareness score display                  │
│  • ProductCard       - Product display card                     │
│  • DisclaimerBox     - Legal disclaimer                         │
│  • Navbar, Footer    - Navigation                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP Requests
                         │ (axios)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                           │
│                    http://localhost:8000                         │
├─────────────────────────────────────────────────────────────────┤
│  Routes:                                                         │
│  • GET  /api/product/search    - Search product                 │
│  • GET  /api/product/browse    - Browse products                │
│  • GET  /api/product/popular   - Popular products               │
│  • POST /api/product/verify    - Verify ingredients ✨ NEW      │
│  • POST /api/product/correct   - Submit correction ✨ NEW       │
│  • GET  /api/ingredient/check  - Check ingredient               │
│  • GET  /api/history           - Search history                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Calls
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE ✨ NEW                         │
│              (services/data_pipeline.py)                         │
├─────────────────────────────────────────────────────────────────┤
│  Master orchestrator that tries sources in order:               │
│                                                                  │
│  1. Open Food Facts  → High reliability, no API key             │
│  2. Edamam API       → High reliability, free API key           │
│  3. BigBasket        → Medium reliability, web scraping         │
│  4. AI Estimation    → Low reliability, fallback only           │
│                                                                  │
│  Returns: ingredients_list + data_source + confidence           │
└────┬────────────┬────────────┬────────────┬─────────────────────┘
     │            │            │            │
     ▼            ▼            ▼            ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐
│  Open   │ │ Edamam  │ │BigBasket│ │   Groq AI       │
│  Food   │ │   API   │ │ Scraper │ │   Service       │
│  Facts  │ │         │ │         │ │                 │
├─────────┤ ├─────────┤ ├─────────┤ ├─────────────────┤
│ • Free  │ │ • Free  │ │ • Free  │ │ • Analyzes      │
│ • Global│ │ • API   │ │ • Web   │ │   ingredients   │
│ • High  │ │   key   │ │   scrape│ │ • Classifies    │
│   data  │ │ • Nutri │ │ • Indian│ │ • Scores        │
│   quality│ │   focus │ │   focus │ │ • Details       │
└─────────┘ └─────────┘ └─────────┘ └────────┬────────┘
                                              │
                                              │ Analyzes
                                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GROQ AI ANALYSIS                              │
│                  (llama-3.3-70b-versatile)                       │
├─────────────────────────────────────────────────────────────────┤
│  Functions:                                                      │
│  • analyze_product()           - Estimate ingredients            │
│  • analyze_ingredients_list()  - Analyze known list ✨ NEW      │
│  • analyze_ingredient()        - Single ingredient               │
│                                                                  │
│  Output:                                                         │
│  • Classification (generally_recognised, worth_knowing, etc.)    │
│  • Awareness score (0-100)                                       │
│  • Detailed effects (for flagged ingredients) ✨ NEW            │
│  • Verdict and recommendation ✨ NEW                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Stores corrections
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATABASE (Supabase)                           │
│              https://ecyuhdegovjhhqvasiez.supabase.co           │
├─────────────────────────────────────────────────────────────────┤
│  Tables:                                                         │
│  • products              - Product catalog                       │
│  • ingredients           - Ingredient rules (50 seed items)      │
│  • search_history        - User search history                   │
│  • pending_corrections   - User submissions ✨ NEW              │
│                                                                  │
│  RLS Policies:                                                   │
│  • Anyone can read                                               │
│  • Anyone can submit corrections ✨ NEW                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Product Search

### Flow Diagram

```
USER TYPES "MAGGI NOODLES"
         │
         ▼
┌────────────────────┐
│   SearchBar.jsx    │  User input
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│   Result.jsx       │  Navigate to /result/Maggi+Noodles
└────────┬───────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   GET /api/product/search?name=Maggi+Noodles           │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   product.py (route)                                    │
│   • Calls data_pipeline.get_product_data()              │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   data_pipeline.py                                      │
│   • Try Open Food Facts → ✅ FOUND (15 ingredients)    │
│   • Skip Edamam (already found)                         │
│   • Skip BigBasket (already found)                      │
│   • Skip AI (already found)                             │
│   • Return: {                                           │
│       source: "open_food_facts",                        │
│       confidence: "high",                               │
│       ingredients_list: [...]                           │
│     }                                                    │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   groq_service.py                                       │
│   • analyze_ingredients_list()                          │
│   • Classify each ingredient                            │
│   • Calculate awareness score                           │
│   • Generate verdict & recommendation                   │
│   • Return: {                                           │
│       brand: "Nestle",                                  │
│       awareness_score: 65,                              │
│       ingredients: [...classified...],                  │
│       verdict: "Worth knowing about some ingredients",  │
│       recommendation: "Use with awareness..."           │
│     }                                                    │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   product.py (route)                                    │
│   • Combine pipeline data + AI analysis                 │
│   • Return ProductResponse with:                        │
│     - data_source: "open_food_facts"                    │
│     - confidence: "high"                                │
│     - is_complete: true                                 │
│     - All ingredient details                            │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   Result.jsx                                            │
│   • Display product info                                │
│   • Show awareness score                                │
│   • List all ingredients (color-coded)                  │
│   • Show detailed effects for flagged ingredients       │
│   • Show verdict & recommendation                       │
│   • ✅ NO yellow warning (confidence is high)          │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow: User Correction

### Flow Diagram

```
USER SEARCHES "UNKNOWN PRODUCT"
         │
         ▼
AI ESTIMATION USED (no external data)
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   Result.jsx                                            │
│   • Shows yellow warning box                            │
│   • "These ingredients are AI estimated..."             │
│   • [Submit correct ingredients] button                 │
└────────┬───────────────────────────────────────────────┘
         │
         ▼ USER CLICKS BUTTON
┌────────────────────────────────────────────────────────┐
│   Result.jsx                                            │
│   • setShowCorrectionForm(true)                         │
│   • Display textarea                                    │
└────────┬───────────────────────────────────────────────┘
         │
         ▼ USER PASTES INGREDIENTS
┌────────────────────────────────────────────────────────┐
│   Result.jsx                                            │
│   • setCorrectionText("Water, Sugar, ...")              │
└────────┬───────────────────────────────────────────────┘
         │
         ▼ USER CLICKS "SUBMIT CORRECTION"
┌────────────────────────────────────────────────────────┐
│   handleSubmitCorrection()                              │
│   • POST /api/product/correct                           │
│     params: {                                           │
│       product_name: "Unknown Product",                  │
│       ingredients: "Water, Sugar, ...",                 │
│       product_id: null                                  │
│     }                                                    │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   product.py (route)                                    │
│   • Receive correction data                             │
│   • Insert into Supabase:                               │
│     supabase.table("pending_corrections").insert({      │
│       product_name: "Unknown Product",                  │
│       submitted_ingredients: "Water, Sugar, ...",       │
│       status: "pending"                                 │
│     })                                                   │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   Supabase Database                                     │
│   • pending_corrections table                           │
│   • New row inserted                                    │
│   • Can be reviewed in dashboard                        │
└────────┬───────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   Result.jsx                                            │
│   • Show success message                                │
│   • "Thank you! Your correction has been submitted..."  │
│   • Hide form                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend
```
React 18.2.0
├── Vite (build tool)
├── React Router (routing)
├── Tailwind CSS (styling)
├── Framer Motion (animations)
├── Axios (HTTP client)
└── Environment: Node.js
```

### Backend
```
Python 3.9+
├── FastAPI (web framework)
├── Uvicorn (ASGI server)
├── Pydantic (data validation)
├── HTTPX (async HTTP client)
├── BeautifulSoup4 (web scraping)
├── Python-dotenv (environment variables)
└── Groq SDK (AI integration)
```

### Database
```
Supabase (PostgreSQL)
├── Products table
├── Ingredients table (50 seed items)
├── Search history table
└── Pending corrections table ✨ NEW
```

### External APIs
```
1. Open Food Facts API
   └── Free, no key required

2. Edamam Food Database API
   └── Free tier, API key required

3. Groq AI API
   └── llama-3.3-70b-versatile model

4. BigBasket (web scraping)
   └── No API, respectful scraping
```

---

## Environment Variables

### Backend (.env)
```env
# Required
SUPABASE_URL=https://ecyuhdegovjhhqvasiez.supabase.co
SUPABASE_ANON_KEY=eyJ...
GROQ_API_KEY=gsk_...
ALLOWED_ORIGINS=http://localhost:5173

# Optional (for better coverage)
EDAMAM_APP_ID=your_app_id
EDAMAM_APP_KEY=your_app_key
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## Port Configuration

```
Frontend:  http://localhost:5173  (Vite dev server)
Backend:   http://localhost:8000  (Uvicorn)
Database:  https://ecyuhdegovjhhqvasiez.supabase.co
```

---

## File Structure

```
checkkaro/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Result.jsx ✨ UPDATED
│   │   │   ├── CheckIngredient.jsx
│   │   │   ├── Products.jsx
│   │   │   └── About.jsx
│   │   ├── components/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── ScoreCircle.jsx
│   │   │   ├── ProductCard.jsx
│   │   │   ├── DisclaimerBox.jsx
│   │   │   ├── Navbar.jsx
│   │   │   └── Footer.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── .env
│
├── backend/
│   ├── routes/
│   │   ├── product.py ✨ UPDATED
│   │   ├── ingredient.py
│   │   └── history.py
│   ├── services/
│   │   ├── data_pipeline.py ✨ NEW
│   │   ├── openfoodfacts_service.py ✨ UPDATED
│   │   ├── edamam_service.py ✨ NEW
│   │   ├── bigbasket_service.py ✨ NEW
│   │   └── groq_service.py ✨ UPDATED
│   ├── models/
│   │   └── schemas.py ✨ UPDATED
│   ├── db/
│   │   └── supabase_client.py
│   ├── main.py
│   ├── requirements.txt ✨ UPDATED
│   ├── .env
│   └── kill_and_restart.ps1
│
├── database/
│   ├── schema.sql
│   ├── seed.sql
│   └── pending_corrections.sql ✨ NEW
│
└── Documentation/
    ├── README.md
    ├── QUICKSTART.md
    ├── USER_GUIDE.md
    ├── MULTI_SOURCE_PIPELINE_COMPLETE.md ✨ NEW
    ├── WHAT_CHANGED.md ✨ NEW
    ├── QUICK_START_PIPELINE.md ✨ NEW
    ├── TASK_7_COMPLETE.md ✨ NEW
    └── SYSTEM_ARCHITECTURE.md ✨ NEW (this file)
```

---

## Security & Privacy

### Data Protection
- ✅ No user authentication required
- ✅ No personal data collected
- ✅ Search history stored locally (optional)
- ✅ Supabase RLS policies enabled
- ✅ CORS configured for localhost only

### API Security
- ✅ API keys stored in .env (not committed)
- ✅ Rate limiting on external APIs
- ✅ Timeout handling (10-15 seconds)
- ✅ Error messages don't expose internals

### Web Scraping Ethics
- ✅ 1-second delay between requests
- ✅ Respectful user agent
- ✅ Only scrapes public product pages
- ✅ Graceful error handling

---

## Performance Optimization

### Frontend
- ✅ Code splitting with React Router
- ✅ Lazy loading of components
- ✅ Optimized images
- ✅ Tailwind CSS purging

### Backend
- ✅ Async/await throughout
- ✅ Connection pooling (httpx)
- ✅ Early exit in pipeline (stops when found)
- ✅ Timeout handling

### Database
- ✅ Indexed columns
- ✅ RLS policies optimized
- ✅ Connection pooling

---

## Monitoring & Logging

### Console Logs
```python
# Pipeline logs
[DATA PIPELINE] Starting search for: {product_name}
[DATA PIPELINE] Trying Open Food Facts...
[DATA PIPELINE] ✓ Found in Open Food Facts: {count} ingredients
[DATA PIPELINE] ✗ Open Food Facts: insufficient data

# Product search logs
[PRODUCT SEARCH] Starting search for: {name}
[PRODUCT SEARCH] Data source: {source}, Confidence: {confidence}
[PRODUCT SEARCH] Returning response with {count} ingredients

# Error logs
[EDAMAM] API returned status {status_code}
[BIGBASKET] Scraping error: {error}
```

---

## Deployment Considerations (Future)

### Frontend
- Build: `npm run build`
- Deploy to: Vercel, Netlify, or Cloudflare Pages
- Environment variables: Set in platform

### Backend
- Deploy to: Railway, Render, or AWS Lambda
- Environment variables: Set in platform
- Database: Already on Supabase (cloud)

### Domain
- Frontend: checkkaro.com
- Backend: api.checkkaro.com
- Update CORS settings

---

## Summary

This architecture provides:
- ✅ Multi-source data aggregation
- ✅ Intelligent fallback system
- ✅ User contribution mechanism
- ✅ Transparent data quality indicators
- ✅ Scalable and maintainable codebase
- ✅ Comprehensive error handling
- ✅ Clear separation of concerns

The system is production-ready for local development and can be deployed to cloud platforms with minimal configuration changes.
