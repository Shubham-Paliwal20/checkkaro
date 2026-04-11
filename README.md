# CheckKaro — Know Your Food & Cosmetic Products

## What is CheckKaro?

CheckKaro is an Indian consumer awareness platform that helps you understand the ingredients in food and cosmetic products. Search any product sold in India and get a clear, jargon-free breakdown of every ingredient with regulatory context from FSSAI, WHO, EFSA, and international research.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | React 18 + Vite + Tailwind CSS |
| Backend | Python FastAPI |
| Database | Supabase (PostgreSQL) |
| AI Analysis | Groq (Llama 3 70B) |
| Product Data | Open Food Facts API |

## Prerequisites

- Node.js 18+
- Python 3.11+
- Supabase account (free at supabase.com)
- Groq API key (free at console.groq.com)

## Setup Instructions

### 1. Database Setup

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to SQL Editor in your Supabase dashboard
3. Run `database/schema.sql` to create tables
4. Run `database/seed.sql` to populate ingredient rules

### 2. Backend Setup

```bash
cd backend
cp .env.example .env
# Edit .env and fill in:
# SUPABASE_URL=your_supabase_project_url_here
# SUPABASE_ANON_KEY=your_supabase_anon_key_here
# GROQ_API_KEY=your_groq_api_key_here

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
cp .env.example .env
# Edit .env:
# VITE_API_BASE_URL=http://localhost:8000

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Open in Browser

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

## API Documentation

### Product Endpoints

- `GET /api/product/search?name={query}` - Search for a product by name
- `GET /api/product/{product_id}` - Get product details by ID
- `GET /api/products/browse?category={cat}&page={n}&limit={l}` - Browse products with pagination
- `GET /api/products/popular` - Get top 12 most searched products

### Ingredient Endpoints

- `GET /api/ingredient/search?name={query}` - Search for ingredient information

### History Endpoints

- `GET /api/history?limit={n}` - Get recent search history

### Health Check

- `GET /health` - API health status

## Awareness Score

The Awareness Score (0-100) reflects how commonly ingredients are discussed by researchers and flagged by international regulatory bodies:

**Calculation:**
- Start at 100
- Subtract 3 for each "worth knowing" ingredient
- Subtract 12 for each "commonly questioned" ingredient
- Minimum score is 5

**Color Coding:**
- Green (70-100): Mostly generally recognised ingredients
- Amber (40-69): Contains ingredients worth knowing about
- Red (0-39): Contains commonly questioned ingredients

## Classification System

**Generally Recognised:** Ingredients with no notable regulatory flags in major jurisdictions

**Worth Knowing:** Permitted but discussed in research or has regulatory limits in some contexts

**Commonly Questioned:** Restricted or banned in one or more countries, or subject to significant scientific debate

## Legal Disclaimer

CheckKaro provides ingredient information for general awareness only. Our classifications are based on publicly available international regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research.

**This is not medical advice.** CheckKaro does not certify any product as safe or unsafe. We do not make health claims. Individual responses to ingredients vary. Always read the actual product label and consult a qualified healthcare professional for personal health decisions.

The Awareness Score is not a safety rating, health claim, or medical assessment. It reflects regulatory discussion frequency, not product quality or health impact.

## Git Workflow

### Branches

- `main`: Production-ready code only
- `develop`: Integration branch for features
- `feature/xxx`: New features
- `fix/xxx`: Bug fixes

### Adding a New Feature

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make changes
git add .
git commit -m "feat: description of what you built"
git push origin feature/your-feature-name

# Open Pull Request on GitHub: feature → develop
```

### Commit Message Format

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting
- `refactor:` code restructure
- `chore:` setup/config

## Contributing

See `.github/CONTRIBUTING.md` for detailed contribution guidelines.

## License

This project is for educational and informational purposes.
