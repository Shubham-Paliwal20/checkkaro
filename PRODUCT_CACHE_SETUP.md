# Product Cache System - Setup Guide

## What This Does

✅ **Saves tokens** - Products searched once are cached, no AI calls needed for repeat searches
✅ **Faster searches** - Cached products load instantly from database
✅ **Builds database** - Your product database grows automatically as users search
✅ **Tracks popularity** - See which products are searched most

---

## How It Works

### First Search (Uses AI Tokens)
1. User searches "Maggi Noodles"
2. System checks database → Not found
3. Calls Groq AI to analyze product
4. **Saves result to database**
5. Returns result to user

### Second Search (FREE - No Tokens!)
1. User searches "Maggi Noodles" again
2. System checks database → **Found!**
3. Returns cached result instantly
4. Increments search_count
5. **No AI tokens used!** 🎉

---

## Setup Steps

### Step 1: Run Database Migration

Open Supabase SQL Editor and run this:

```sql
-- Add verdict and recommendation fields to products table
ALTER TABLE products 
ADD COLUMN IF NOT EXISTS verdict TEXT,
ADD COLUMN IF NOT EXISTS recommendation TEXT;

-- Add index for faster searches
CREATE INDEX IF NOT EXISTS idx_products_search_count ON products(search_count DESC);
```

**File:** `database/add_verdict_recommendation.sql`

### Step 2: Restart Backend

The backend should auto-reload, but if not:

```bash
cd backend
# Stop current server (Ctrl+C)
python main.py
```

### Step 3: Test It!

**First Search (Uses AI):**
```bash
curl "http://localhost:8000/api/product/search?name=Maggi"
```

Look for in logs:
```
[CACHE] ✗ Not found in database
[PRODUCT SEARCH] Analyzing ingredients with Groq AI...
[CACHE] ✓ Product saved with ID: xxx
```

**Second Search (From Cache):**
```bash
curl "http://localhost:8000/api/product/search?name=Maggi"
```

Look for in logs:
```
[CACHE] ✓ Found in database! ID: xxx, Searches: 2
[PRODUCT SEARCH] ✓ Returning from cache (saved tokens!)
```

---

## What Gets Cached

### Product Data
- Name (normalized for matching)
- Brand
- Category
- Image URL
- Awareness Score
- Summary
- FSSAI Note
- Verdict
- Recommendation
- Search Count (increments each time)

### Ingredients
- Name
- Aliases
- Classification (generally_recognised/worth_knowing/commonly_questioned)
- One Line Note
- Regulatory Note

---

## Features

### 1. Smart Name Matching

Searches are normalized to match variations:
- "Maggi Noodles" = "maggi noodles" = "MAGGI NOODLES"
- Removes special characters
- Handles extra spaces

### 2. Search Count Tracking

Every search increments the counter:
- First search: search_count = 1
- Second search: search_count = 2
- Third search: search_count = 3

### 3. Popular Products API

Get most searched products:

```bash
curl "http://localhost:8000/api/product/popular"
```

Returns top 12 products by search_count.

### 4. Browse Products API

Browse cached products:

```bash
curl "http://localhost:8000/api/product/browse?limit=20"
```

Filter by category:

```bash
curl "http://localhost:8000/api/product/browse?category=Snacks"
```

---

## Database Schema

### products table
```sql
id                UUID PRIMARY KEY
name              TEXT NOT NULL
name_normalized   TEXT NOT NULL (for matching)
brand             TEXT
category          TEXT
image_url         TEXT
awareness_score   INTEGER DEFAULT 50
summary           TEXT
fssai_note        TEXT
verdict           TEXT (NEW)
recommendation    TEXT (NEW)
search_count      INTEGER DEFAULT 1
created_at        TIMESTAMP
last_verified     TIMESTAMP
```

### product_ingredients table
```sql
id                UUID PRIMARY KEY
product_id        UUID (references products)
ingredient_name   TEXT NOT NULL
aliases           TEXT
classification    TEXT (enum)
one_line_note     TEXT
regulatory_note   TEXT
```

---

## Token Savings Example

### Without Cache (Every Search Uses AI)
- 100 searches for "Maggi" = 100 AI calls
- ~500 tokens per call = 50,000 tokens
- Cost: Significant token usage

### With Cache (First Search Only)
- 100 searches for "Maggi" = 1 AI call + 99 database reads
- ~500 tokens for first call = 500 tokens total
- Cost: **99% token savings!** 🎉

---

## Monitoring

### Check Cache Status

**View all cached products:**
```sql
SELECT name, brand, category, search_count, created_at 
FROM products 
ORDER BY search_count DESC 
LIMIT 20;
```

**Count total products:**
```sql
SELECT COUNT(*) as total_products FROM products;
```

**Count total ingredients:**
```sql
SELECT COUNT(*) as total_ingredients FROM product_ingredients;
```

**Most popular products:**
```sql
SELECT name, brand, search_count 
FROM products 
ORDER BY search_count DESC 
LIMIT 10;
```

---

## Backend Logs

### Cache Hit (Saved Tokens!)
```
[PRODUCT SEARCH] Starting search for: Maggi
[CACHE] Looking for: maggi
[CACHE] ✓ Found in database! ID: xxx, Searches: 5
[PRODUCT SEARCH] ✓ Returning from cache (saved tokens!)
```

### Cache Miss (Uses AI)
```
[PRODUCT SEARCH] Starting search for: New Product
[CACHE] Looking for: new product
[CACHE] ✗ Not found in database
[PRODUCT SEARCH] Running data pipeline...
[PRODUCT SEARCH] Analyzing ingredients with Groq AI...
[CACHE] ✓ Product saved with ID: xxx
```

---

## Benefits

### For You (Developer)
✅ Save AI tokens (99% reduction for popular products)
✅ Faster response times (database is instant)
✅ Build valuable product database automatically
✅ Track product popularity
✅ Reduce API costs

### For Users
✅ Instant search results for popular products
✅ Consistent data (same product always returns same result)
✅ Better user experience (faster loading)

---

## Future Enhancements

### Possible Additions
1. **Cache Expiry** - Refresh old products after 30 days
2. **User Corrections** - Allow users to update cached data
3. **Batch Import** - Import products from CSV
4. **Analytics** - Track search trends over time
5. **Auto-Update** - Periodically refresh popular products

---

## Troubleshooting

### Products Not Caching

**Check 1: Migration Run?**
```sql
-- Check if columns exist
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'products' 
AND column_name IN ('verdict', 'recommendation');
```

**Check 2: Backend Logs**
Look for:
```
[CACHE ERROR] Failed to save product: ...
```

**Check 3: Database Connection**
```bash
# Test connection
curl "http://localhost:8000/health"
```

### Cache Not Being Used

**Check logs for:**
```
[CACHE] ✗ Not found in database
```

Even though product exists? Check name normalization:
```sql
SELECT name, name_normalized FROM products WHERE name ILIKE '%maggi%';
```

---

## Summary

Your CheckKaro app now has intelligent product caching that:
- ✅ Saves 99% of AI tokens for repeat searches
- ✅ Makes searches instant for cached products
- ✅ Builds your product database automatically
- ✅ Tracks product popularity

**Run the migration and start saving tokens!** 🚀
