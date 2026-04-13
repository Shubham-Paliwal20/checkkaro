# Quick Start - Multi-Source Pipeline

## 🚀 Get Started in 3 Steps

### Step 1: Run Database Migration (2 minutes)

1. Open Supabase Dashboard: https://supabase.com/dashboard
2. Select your project: `ecyuhdegovjhhqvasiez`
3. Click "SQL Editor" in left sidebar
4. Click "New Query"
5. Copy entire contents of `database/pending_corrections.sql`
6. Paste into SQL editor
7. Click "Run" button
8. ✅ You should see: "Success. No rows returned"

### Step 2: Restart Backend (1 minute)

**Option A - Using PowerShell Script:**
```bash
cd checkkaro/backend
./kill_and_restart.ps1
```

**Option B - Manual:**
```bash
# Kill existing Python processes
Get-Process | Where-Object {$_.Path -like "*python*"} | Stop-Process -Force

# Start backend
cd checkkaro/backend
python -m uvicorn main:app --reload --port 8000
```

### Step 3: Test It! (2 minutes)

1. Make sure frontend is running: http://localhost:5173
2. Search for: **"Coca Cola"**
3. Check console logs - should see: `[DATA PIPELINE] ✓ Found in Open Food Facts`
4. Search for: **"Unknown Product XYZ"**
5. Should see yellow warning box: "Help Improve This Data"
6. Click "Submit correct ingredients" - form should appear
7. ✅ Done!

---

## 🎯 What to Expect

### High Confidence Products (No Warning)
- Coca Cola
- Nutella
- Kelloggs Corn Flakes
- Maggi Noodles
- Parle G Biscuits

### Low Confidence Products (Yellow Warning)
- Unknown brands
- Local products
- New products not in databases

---

## 🔧 Optional: Add Edamam API (5 minutes)

For better coverage of nutritional products:

1. Go to: https://developer.edamam.com/food-database-api
2. Click "Sign Up" (free tier available)
3. Create account and get credentials
4. Copy APP_ID and APP_KEY
5. Add to `backend/.env`:

```env
EDAMAM_APP_ID=your_app_id_here
EDAMAM_APP_KEY=your_app_key_here
```

6. Restart backend

**Note**: Pipeline works fine without Edamam, it just adds one more data source.

---

## 📊 How to View User Corrections

### In Supabase Dashboard:

1. Go to "Table Editor"
2. Select `pending_corrections` table
3. See all user submissions

### Using SQL:

```sql
-- View all pending corrections
SELECT 
    product_name,
    submitted_ingredients,
    submitted_at
FROM pending_corrections
WHERE status = 'pending'
ORDER BY submitted_at DESC;
```

---

## 🐛 Troubleshooting

### "Table pending_corrections does not exist"
→ Run `database/pending_corrections.sql` in Supabase SQL Editor

### "All products show AI-estimated"
→ Check backend console for errors
→ Verify internet connection
→ Try a well-known product like "Coca Cola"

### "Yellow warning not appearing"
→ Check browser console for errors
→ Verify frontend is using latest code
→ Hard refresh: Ctrl+Shift+R

### "Correction not saving"
→ Check backend console for errors
→ Verify `pending_corrections` table exists
→ Check Supabase RLS policies are enabled

---

## 📝 Quick Reference

### Data Sources (in order)
1. Open Food Facts - No API key needed
2. Edamam - Optional API key
3. BigBasket - No API key needed
4. AI Estimation - Fallback

### Confidence Levels
- **High**: External source with 4+ ingredients
- **Medium**: BigBasket scraper with 4+ ingredients
- **Low**: AI estimation only

### New API Endpoints
- `POST /api/product/verify` - User confirms ingredients
- `POST /api/product/correct` - User submits correction

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Backend starts without errors
2. ✅ Console shows: `[DATA PIPELINE] Starting search for...`
3. ✅ Products show data source in response
4. ✅ Yellow warning appears for unknown products
5. ✅ Corrections save to Supabase table

---

## 📚 Full Documentation

- `MULTI_SOURCE_PIPELINE_COMPLETE.md` - Complete implementation details
- `WHAT_CHANGED.md` - Visual guide of changes
- `QUICK_START_PIPELINE.md` - This file

---

## 🎉 That's It!

Your multi-source data pipeline is ready. The system will now automatically try multiple sources to get accurate ingredient data, and users can help improve the database by submitting corrections.

**Required**: Run SQL file + Restart backend
**Optional**: Add Edamam API credentials
**Test**: Search for products and see the magic happen!
