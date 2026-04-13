# 🚀 Run CheckKaro RIGHT NOW (Without API Keys)

## Option 1: Just See the Frontend UI (No Backend Needed)

This will show you the UI design, but search won't work yet.

### Open 2 Terminals:

**Terminal 1 - Start Frontend:**
```bash
cd checkkaro/frontend
npm run dev
```

Then open: **http://localhost:5173**

You'll see:
- ✅ Beautiful homepage
- ✅ Navigation working
- ✅ All pages visible
- ❌ Search won't work (needs backend + API keys)

---

## Option 2: Full Working App (Needs API Keys)

### Step 1: Get FREE API Keys (5 minutes)

**A. Supabase (Database):**
1. Go to https://supabase.com
2. Sign up (free, no credit card)
3. Click "New Project"
4. Wait 2 minutes for setup
5. Go to Settings → API
6. Copy: Project URL and anon key

**B. Groq (AI):**
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Go to API Keys
4. Create new key
5. Copy the key

### Step 2: Setup Database (2 minutes)
1. In Supabase, go to SQL Editor
2. Open `checkkaro/database/schema.sql` in notepad
3. Copy all text, paste in SQL Editor, click RUN
4. Open `checkkaro/database/seed.sql` in notepad
5. Copy all text, paste in SQL Editor, click RUN

### Step 3: Add Keys to Backend
Open `checkkaro/backend/.env` in notepad and replace:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Step 4: Run Both Servers

**Terminal 1 - Backend:**
```bash
cd checkkaro/backend
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd checkkaro/frontend
npm run dev
```

### Step 5: Open Browser
Go to: **http://localhost:5173**

Now search for "Maggi Noodles" or "Kurkure" and see the magic! ✨

---

## 🎯 What You'll See Working:

1. **Search any product** → AI analyzes ingredients
2. **Awareness Score** → Color-coded 0-100 score
3. **3 Columns** → Ingredients categorized
4. **Check Ingredient** → Look up individual ingredients
5. **Product Directory** → Browse analyzed products

---

## ⚡ Quick Test (No Setup)

Want to see the UI immediately?

```bash
cd checkkaro/frontend
npm run dev
```

Open http://localhost:5173 - You'll see the beautiful interface!

(Search won't work without backend + API keys, but you can see the design)
