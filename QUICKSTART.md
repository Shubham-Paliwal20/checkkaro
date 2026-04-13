# Quick Start Guide - Run CheckKaro Locally

## ⚠️ IMPORTANT: You need API keys first!

Before running, you MUST get these free API keys:

### 1. Get Supabase Keys (Database)
1. Go to https://supabase.com and sign up (free)
2. Create a new project
3. Go to Project Settings → API
4. Copy your:
   - Project URL
   - anon/public key

### 2. Get Groq API Key (AI)
1. Go to https://console.groq.com and sign up (free)
2. Go to API Keys section
3. Create a new API key
4. Copy the key

### 3. Set Up Database
1. In your Supabase project, go to SQL Editor
2. Copy and paste the contents of `database/schema.sql`
3. Click "Run"
4. Then copy and paste the contents of `database/seed.sql`
5. Click "Run"

---

## 🚀 Run the Application

### Step 1: Configure Backend
```bash
cd backend
# Edit .env file and add your keys:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_ANON_KEY=your-anon-key-here
# GROQ_API_KEY=your-groq-api-key-here
```

### Step 2: Start Backend Server
```bash
# In backend folder
python -m uvicorn main:app --reload --port 8000
```

Keep this terminal open! Backend will run at http://localhost:8000

### Step 3: Start Frontend (New Terminal)
```bash
cd frontend
npm run dev
```

Keep this terminal open! Frontend will run at http://localhost:5173

### Step 4: Open Browser
Go to: **http://localhost:5173**

---

## 🎯 Test the Application

1. **Home Page**: You should see the CheckKaro homepage
2. **Try a search**: Type "Maggi Noodles" or click a quick search chip
3. **View Results**: See the ingredient breakdown and awareness score
4. **Check Ingredient**: Go to "Check Ingredient" and search for "MSG" or "TBHQ"

---

## ❌ Troubleshooting

### Backend won't start?
- Make sure you added the API keys to `backend/.env`
- Make sure you ran the database SQL scripts in Supabase
- Check if port 8000 is already in use

### Frontend shows errors?
- Make sure backend is running first
- Check that `frontend/.env` has `VITE_API_BASE_URL=http://localhost:8000`
- Try refreshing the page

### "Failed to fetch" errors?
- Backend is not running or crashed
- Check backend terminal for errors
- Make sure your Supabase and Groq API keys are correct

---

## 📝 Quick Commands Reference

**Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**View API Docs:**
http://localhost:8000/docs
