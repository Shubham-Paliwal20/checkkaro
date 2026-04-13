# CheckKaro Data Collection Strategy

## Goal
Build a reliable database of Indian products with verified ingredients instead of relying on AI estimation.

---

## Phase 1: Immediate - Use Open Food Facts API ⭐

### Why Open Food Facts?
- ✅ Free and open source
- ✅ 50,000+ Indian products
- ✅ Real ingredient data from product labels
- ✅ Product images and barcodes
- ✅ JSON API available
- ✅ Crowdsourced and verified

### Implementation Steps

1. **Search Products by Name**
   ```
   GET https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&search_simple=1&action=process&json=1&page_size=10&fields=product_name,brands,ingredients_text,image_url,code
   ```

2. **Get Product by Barcode**
   ```
   GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json
   ```

3. **Filter for India**
   ```
   GET https://in.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&countries=India&json=1
   ```

### Data Available
- Product name
- Brand
- Ingredients list (text)
- Barcode
- Product image
- Category
- Nutrition facts
- Labels (organic, vegan, etc.)

---

## Phase 2: Web Scraping Indian E-commerce

### 1. BigBasket (Already Implemented!)
Your code already has `bigbasket_service.py` - just needs to be enhanced.

**Products Available**: 20,000+
**Categories**: Snacks, beverages, personal care, household

### 2. Amazon India
**Method**: Product Advertising API or Selenium scraping
**Coverage**: Largest catalog
**Data Quality**: Good (user-submitted)

### 3. Flipkart
**Method**: Web scraping
**Coverage**: Large Indian product catalog
**Data Quality**: Good

### 4. Blinkit/Zepto/Swiggy Instamart
**Method**: API or web scraping
**Coverage**: Popular FMCG products
**Data Quality**: Good

---

## Phase 3: User-Generated Content

### Your App Already Has This!
- ✅ Correction form on Result page
- ✅ `pending_corrections` table in database
- ✅ Users can submit real ingredients from product labels

### Enhancement Needed
1. **Admin Panel**: Review and approve user submissions
2. **Verification System**: Mark products as "verified by users"
3. **Gamification**: Reward users for contributing data
4. **Photo Upload**: Let users upload product label photos

---

## Phase 4: FSSAI Official Data

### FSSAI License Database
- **Website**: https://foscos.fssai.gov.in/
- **Data**: All licensed food products in India
- **Access**: Public search portal
- **Method**: Web scraping or manual collection

### FSSAI Product Approval List
- **Source**: FSSAI notifications and circulars
- **Data**: Approved additives, ingredients, limits
- **Use**: Validate ingredient safety

---

## Database Schema for Products

```sql
-- Products table (already exists)
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    brand TEXT,
    category TEXT,
    barcode TEXT UNIQUE,
    image_url TEXT,
    ingredients_text TEXT, -- Raw ingredients from label
    awareness_score INTEGER,
    data_source TEXT, -- 'openfoodfacts', 'bigbasket', 'user_submitted', 'verified'
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Product ingredients (parsed)
CREATE TABLE product_ingredients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    ingredient_name TEXT NOT NULL,
    classification TEXT, -- from ingredient_rules table
    position INTEGER, -- order in ingredient list
    created_at TIMESTAMP DEFAULT NOW()
);

-- User contributions
CREATE TABLE user_contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_name TEXT NOT NULL,
    brand TEXT,
    barcode TEXT,
    ingredients_text TEXT NOT NULL,
    image_url TEXT,
    submitted_by TEXT, -- user email or ID
    status TEXT DEFAULT 'pending', -- pending, approved, rejected
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## Implementation Priority

### Week 1: Open Food Facts Integration ⭐ START HERE
1. Create `openfoodfacts_service.py`
2. Add search function
3. Parse ingredients from API response
4. Store in database
5. Update product search to check database first

### Week 2: Enhance BigBasket Scraper
1. Improve existing `bigbasket_service.py`
2. Add more product categories
3. Schedule regular scraping
4. Store in database

### Week 3: User Contribution System
1. Create admin panel for reviewing submissions
2. Add photo upload for product labels
3. Implement verification workflow
4. Add "verified" badge on products

### Week 4: FSSAI Data Collection
1. Manual collection of popular products
2. Web scraping FOSCOS portal
3. Validate against FSSAI standards

---

## Data Collection Workflow

```
User searches "Maggi Noodles"
    ↓
1. Check database (products table)
    ↓ Not found
2. Search Open Food Facts API
    ↓ Found
3. Parse ingredients
    ↓
4. Classify using ingredient_rules table
    ↓
5. Calculate awareness score
    ↓
6. Store in database
    ↓
7. Return to user
    ↓
8. Next search = instant from database!
```

---

## Cost Analysis

| Source | Cost | Coverage | Quality | Effort |
|--------|------|----------|---------|--------|
| Open Food Facts | FREE | 50K+ | High | Low |
| BigBasket Scraping | FREE | 20K+ | High | Medium |
| User Submissions | FREE | Growing | Very High | Low |
| FSSAI Manual | FREE | 1K+ | Highest | High |
| Amazon API | $0-500/mo | 100K+ | Medium | Medium |

**Recommended**: Start with Open Food Facts (free, easy, high quality)

---

## Sample Code: Open Food Facts Integration

```python
# services/openfoodfacts_service.py
import aiohttp
import asyncio

async def search_product(product_name: str):
    """Search Open Food Facts for Indian products"""
    url = "https://in.openfoodfacts.org/cgi/search.pl"
    params = {
        "search_terms": product_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
        "fields": "product_name,brands,ingredients_text,image_url,code,categories"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data.get("products", [])

async def get_product_by_barcode(barcode: str):
    """Get product details by barcode"""
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if data.get("status") == 1:
                return data.get("product")
            return None
```

---

## Next Steps

1. **Implement Open Food Facts integration** (I can do this now!)
2. **Create database tables for products**
3. **Update search flow to check database first**
4. **Build admin panel for user submissions**
5. **Schedule regular data collection**

---

## Expected Results

- **Week 1**: 50,000+ products from Open Food Facts
- **Month 1**: 100,000+ products from multiple sources
- **Month 3**: 200,000+ products with user contributions
- **Year 1**: 500,000+ verified Indian products

**Success Rate**: 95%+ (vs current 70% with AI)
**Response Time**: <100ms (vs 2-5 seconds with AI)
**Cost**: FREE (vs Groq API limits)
**Accuracy**: Very High (real labels vs AI estimation)
