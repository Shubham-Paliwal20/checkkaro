# 🚀 Deployment Checklist - Multi-Source Pipeline

## Pre-Deployment Checklist

### ✅ Step 1: Database Setup (REQUIRED)

- [ ] Open Supabase Dashboard: https://supabase.com/dashboard
- [ ] Navigate to SQL Editor
- [ ] Create new query
- [ ] Copy contents of `database/pending_corrections.sql`
- [ ] Paste and run the SQL
- [ ] Verify table created: Check "Table Editor" → `pending_corrections`

**Expected Result**: Table `pending_corrections` appears in table list

---

### ✅ Step 2: Backend Restart (REQUIRED)

- [ ] Stop any running backend processes
- [ ] Navigate to `checkkaro/backend`
- [ ] Run: `./kill_and_restart.ps1` OR manually kill Python processes
- [ ] Start backend: `python -m uvicorn main:app --reload --port 8000`
- [ ] Verify backend running: http://localhost:8000/docs

**Expected Result**: Backend starts without errors, shows FastAPI docs

---

### ✅ Step 3: Frontend Check (REQUIRED)

- [ ] Verify frontend is running: http://localhost:5173
- [ ] If not running: `cd checkkaro/frontend` → `npm run dev`
- [ ] Open browser to http://localhost:5173
- [ ] Verify homepage loads

**Expected Result**: Homepage loads with search bar

---

### 🟡 Step 4: Edamam API (OPTIONAL)

- [ ] Sign up at: https://developer.edamam.com/food-database-api
- [ ] Get APP_ID and APP_KEY
- [ ] Add to `backend/.env`:
  ```env
  EDAMAM_APP_ID=your_app_id_here
  EDAMAM_APP_KEY=your_app_key_here
  ```
- [ ] Restart backend

**Expected Result**: Edamam source available in pipeline

---

## Testing Checklist

### Test 1: High Confidence Product

- [ ] Search for: "Coca Cola"
- [ ] Wait for results
- [ ] Check console logs: Should see `[DATA PIPELINE] ✓ Found in Open Food Facts`
- [ ] Verify NO yellow warning box appears
- [ ] Verify ingredients list is complete
- [ ] Check awareness score is displayed

**Expected Result**: Complete data, no warning, high confidence

---

### Test 2: Low Confidence Product

- [ ] Search for: "Unknown Product XYZ"
- [ ] Wait for results
- [ ] Check console logs: Should see `[DATA PIPELINE] ⚠ Using AI estimation as fallback`
- [ ] Verify yellow warning box appears
- [ ] Verify "Help Improve This Data" section visible
- [ ] Verify two buttons: "Ingredients look correct" and "Submit correct ingredients"

**Expected Result**: Yellow warning box appears, correction options available

---

### Test 3: User Verification

- [ ] Search for unknown product (to trigger AI estimation)
- [ ] Click "✓ Ingredients look correct" button
- [ ] Verify success message appears
- [ ] Check backend console: Should see `[PRODUCT VERIFY]` log

**Expected Result**: Success message, verification logged

---

### Test 4: User Correction Submission

- [ ] Search for unknown product
- [ ] Click "Submit correct ingredients" button
- [ ] Verify textarea appears
- [ ] Paste sample ingredients: "Water, Sugar, Salt, Citric Acid"
- [ ] Click "Submit Correction"
- [ ] Verify success message appears
- [ ] Open Supabase → Table Editor → `pending_corrections`
- [ ] Verify new row appears with your submission

**Expected Result**: Correction saved to database, visible in Supabase

---

### Test 5: Indian Product

- [ ] Search for: "Maggi Noodles"
- [ ] Wait for results
- [ ] Check console logs for data source
- [ ] Verify ingredients appear
- [ ] Check if data is from Open Food Facts or BigBasket

**Expected Result**: Product found, ingredients displayed

---

### Test 6: Multiple Searches

- [ ] Search for: "Nutella"
- [ ] Wait for results
- [ ] Search for: "Kelloggs Corn Flakes"
- [ ] Wait for results
- [ ] Search for: "Parle G Biscuits"
- [ ] Wait for results
- [ ] Verify all searches complete successfully

**Expected Result**: All products return results, no errors

---

## Verification Checklist

### Backend Verification

- [ ] Backend running on port 8000
- [ ] No errors in console
- [ ] API docs accessible: http://localhost:8000/docs
- [ ] All endpoints visible in docs
- [ ] Environment variables loaded (check with `print(os.getenv("GROQ_API_KEY"))`)

---

### Frontend Verification

- [ ] Frontend running on port 5173
- [ ] No errors in browser console
- [ ] Search bar functional
- [ ] Navigation working
- [ ] Styling correct (orange/green theme)
- [ ] Responsive design working

---

### Database Verification

- [ ] Supabase connection working
- [ ] `pending_corrections` table exists
- [ ] RLS policies enabled
- [ ] Can insert data
- [ ] Can read data

---

### Pipeline Verification

- [ ] Open Food Facts working (try "Coca Cola")
- [ ] Edamam working (if configured)
- [ ] BigBasket scraper working (try "Maggi Noodles")
- [ ] AI fallback working (try "Unknown Product")
- [ ] Console logs showing pipeline flow
- [ ] Data source returned in response

---

## Troubleshooting Checklist

### Issue: Backend won't start

- [ ] Check if port 8000 is already in use
- [ ] Kill existing Python processes
- [ ] Verify virtual environment activated
- [ ] Check all dependencies installed: `pip install -r requirements.txt`
- [ ] Verify .env file exists and has correct values

---

### Issue: Frontend won't start

- [ ] Check if port 5173 is already in use
- [ ] Verify node_modules installed: `npm install`
- [ ] Check .env file exists
- [ ] Clear cache: `npm run dev -- --force`

---

### Issue: Database connection fails

- [ ] Verify SUPABASE_URL in .env
- [ ] Verify SUPABASE_ANON_KEY in .env
- [ ] Check Supabase project is active
- [ ] Test connection: Run `backend/test_connection.py`

---

### Issue: Groq API fails

- [ ] Verify GROQ_API_KEY in .env
- [ ] Check API key is valid
- [ ] Test Groq: Run `backend/test_groq.py`
- [ ] Check Groq API status: https://console.groq.com

---

### Issue: All products show AI-estimated

- [ ] Check internet connection
- [ ] Verify Open Food Facts API accessible
- [ ] Check backend console for API errors
- [ ] Try a well-known product like "Coca Cola"
- [ ] Check if httpx is installed: `pip show httpx`

---

### Issue: Yellow warning not appearing

- [ ] Check browser console for errors
- [ ] Verify frontend using latest code
- [ ] Hard refresh: Ctrl+Shift+R
- [ ] Check if `data_source` field in API response
- [ ] Verify Result.jsx has warning box code

---

### Issue: Corrections not saving

- [ ] Verify `pending_corrections` table exists
- [ ] Check RLS policies enabled
- [ ] Check backend console for errors
- [ ] Verify Supabase connection working
- [ ] Test with SQL: `SELECT * FROM pending_corrections;`

---

## Performance Checklist

### Response Times

- [ ] Product search completes in < 10 seconds
- [ ] Open Food Facts responds in < 5 seconds
- [ ] Groq AI responds in < 8 seconds
- [ ] Frontend renders results smoothly
- [ ] No lag in UI interactions

---

### Resource Usage

- [ ] Backend memory usage reasonable (< 500MB)
- [ ] Frontend bundle size reasonable (< 5MB)
- [ ] No memory leaks in browser
- [ ] CPU usage normal during searches

---

## Security Checklist

### Environment Variables

- [ ] .env files not committed to git
- [ ] .env.example files updated
- [ ] API keys kept secret
- [ ] No hardcoded credentials

---

### API Security

- [ ] CORS configured correctly
- [ ] Only localhost allowed in development
- [ ] Timeout handling implemented
- [ ] Error messages don't expose internals

---

### Database Security

- [ ] RLS policies enabled
- [ ] Only necessary permissions granted
- [ ] No SQL injection vulnerabilities
- [ ] Connection string secure

---

## Documentation Checklist

### Files Created

- [x] MULTI_SOURCE_PIPELINE_COMPLETE.md
- [x] WHAT_CHANGED.md
- [x] QUICK_START_PIPELINE.md
- [x] TASK_7_COMPLETE.md
- [x] SYSTEM_ARCHITECTURE.md
- [x] DEPLOYMENT_CHECKLIST.md (this file)

---

### Files Updated

- [x] backend/services/data_pipeline.py
- [x] backend/services/openfoodfacts_service.py
- [x] backend/services/edamam_service.py
- [x] backend/services/bigbasket_service.py
- [x] backend/services/groq_service.py
- [x] backend/routes/product.py
- [x] backend/models/schemas.py
- [x] backend/requirements.txt
- [x] backend/.env.example
- [x] frontend/src/pages/Result.jsx
- [x] database/pending_corrections.sql

---

## Final Verification

### All Systems Go?

- [ ] ✅ Database migration complete
- [ ] ✅ Backend running without errors
- [ ] ✅ Frontend running without errors
- [ ] ✅ All tests passing
- [ ] ✅ Documentation complete
- [ ] ✅ No diagnostics errors
- [ ] ✅ Console logs clean
- [ ] ✅ User corrections working

---

## Next Steps

### Immediate (Required)

1. [ ] Run database migration
2. [ ] Restart backend
3. [ ] Test with 3-5 products
4. [ ] Verify corrections work

### Short Term (Optional)

1. [ ] Sign up for Edamam API
2. [ ] Test with more products
3. [ ] Review pending corrections in Supabase
4. [ ] Monitor console logs for issues

### Long Term (Future)

1. [ ] Build admin dashboard for corrections
2. [ ] Add more data sources
3. [ ] Implement caching
4. [ ] Deploy to production

---

## Success Criteria

You'll know everything is working when:

✅ Backend starts without errors
✅ Frontend loads correctly
✅ Products search successfully
✅ Data pipeline tries multiple sources
✅ Yellow warning appears for AI-estimated data
✅ User corrections save to database
✅ Console logs show pipeline flow
✅ No errors in browser console
✅ All tests pass

---

## Support

If you encounter issues:

1. Check `QUICK_START_PIPELINE.md` for troubleshooting
2. Review console logs (backend and frontend)
3. Verify database migration ran successfully
4. Check all environment variables are set
5. Ensure all dependencies are installed

---

## Completion

When all checkboxes are checked, your multi-source data pipeline is fully deployed and operational! 🎉

**Estimated Time**: 10-15 minutes for required steps
**Difficulty**: Easy (just follow the steps)
**Result**: Production-ready multi-source ingredient data pipeline

---

## Quick Reference

### Start Backend
```bash
cd checkkaro/backend
python -m uvicorn main:app --reload --port 8000
```

### Start Frontend
```bash
cd checkkaro/frontend
npm run dev
```

### View Corrections
```sql
SELECT * FROM pending_corrections ORDER BY submitted_at DESC;
```

### Check Logs
- Backend: Terminal where uvicorn is running
- Frontend: Browser console (F12)
- Database: Supabase Dashboard → Logs

---

**Ready to deploy? Start with Step 1! 🚀**
