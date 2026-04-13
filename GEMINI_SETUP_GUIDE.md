# Google Gemini AI Setup Guide

## Why Switch to Gemini?

**Google Gemini is BETTER than Groq for CheckKaro:**

✅ **Completely FREE** - 1,500 requests per day (vs Groq's 100,000 tokens/day limit)
✅ **More Effective** - Better at understanding Indian products and ingredients
✅ **Faster** - Gemini 1.5 Flash is optimized for speed
✅ **No Rate Limits** - 1 million tokens per minute (vs Groq's strict limits)
✅ **Better JSON Output** - More reliable structured responses

## Setup Steps (5 Minutes)

### Step 1: Get Your Free Gemini API Key

1. Go to: **https://aistudio.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (starts with `AIza...`)

### Step 2: Add API Key to Your Project

1. Open `checkkaro/backend/.env` file
2. Find the line: `GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`
3. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key
4. Save the file

Example:
```
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 3: Install Required Library

Open terminal in `checkkaro/backend` folder and run:

```bash
pip install google-generativeai
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### Step 4: Restart Backend Server

1. Stop the current backend server (Ctrl+C)
2. Start it again:

```bash
cd backend
python main.py
```

### Step 5: Test Product Search

1. Open your frontend: http://localhost:5173
2. Search for any product (e.g., "Dove Soap", "Maggi Noodles")
3. You should now see ingredients displayed correctly!

## What Changed?

✅ **Backend now uses Gemini AI** instead of Groq
✅ **All routes updated** - product search, ingredient search
✅ **Same strict scoring system** - harmful products still score 30-50
✅ **Same color coding** - Green (safe), Yellow (moderate), Red (questioned)

## Troubleshooting

### Error: "GEMINI_API_KEY not found"
- Make sure you added the API key to `.env` file
- Restart the backend server after adding the key

### Error: "Invalid API key"
- Check that you copied the full API key from Google AI Studio
- Make sure there are no extra spaces in the `.env` file

### Still showing 0 ingredients?
- Check backend terminal for error messages
- Make sure you restarted the backend after adding the API key
- Try searching for a common product like "Coca Cola" or "Dove Soap"

## API Limits

**Gemini Free Tier:**
- 1,500 requests per day
- 1 million tokens per minute
- 32,000 tokens per request

This is MORE than enough for CheckKaro! Even with 100 users searching products all day, you won't hit the limit.

## Need Help?

If you still see issues:
1. Check backend terminal for error messages
2. Make sure `.env` file has the correct API key
3. Restart both frontend and backend servers
4. Clear browser cache and try again

---

**Your product search should now work perfectly with Google Gemini AI!** 🎉
