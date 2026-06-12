# Saved: Product Recommendations Feature
# Add back to Result.jsx + product_new.py when ready

---

## 1. Result.jsx — state (add with other useState declarations)

```jsx
const [recommendations, setRecommendations] = useState([])
```

---

## 2. Result.jsx — reset on navigation (inside the productName useEffect)

```jsx
setRecommendations([])
```

---

## 3. Result.jsx — fetch useEffect (add after the productName useEffect)

```jsx
// Fetch better alternatives whenever a C/D grade product loads (any path)
useEffect(() => {
  if (!product) return
  if (!['C', 'D'].includes(product.grade)) return
  if (!product.category) return
  axios.get(`${API_BASE_URL}/api/product/recommendations`, {
    params: { category: product.category, exclude_id: product.id, limit: 6 }
  }).then(r => setRecommendations(r.data || [])).catch(() => {})
}, [product?.id, product?.grade])
```

---

## 4. Result.jsx — JSX section (place before the Summary section)

```jsx
{/* Better Alternatives — shown for C/D grade products */}
{recommendations.length > 0 && (
  <div className="card p-4 sm:p-6 mb-6 border-l-4 border-green-500 bg-green-50">
    <div className="flex items-center gap-2 mb-1">
      <svg className="w-5 h-5 text-green-600 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
      </svg>
      <h2 className="font-poppins font-bold text-base sm:text-lg text-green-900">
        Better Alternatives in {product.category}
      </h2>
    </div>
    <p className="text-xs text-green-700 mb-4">
      These {product.category.toLowerCase()} products are Grade A or B — cleaner ingredient lists in the same category.
    </p>
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {recommendations.map((rec, idx) => (
        <button
          key={idx}
          onClick={() => navigate(`/result/${encodeURIComponent(rec.name)}`)}
          className="bg-white rounded-xl border border-green-200 hover:border-green-400 hover:shadow-md transition-all text-left overflow-hidden group"
        >
          <div className="aspect-square bg-gray-50 flex items-center justify-center overflow-hidden">
            {rec.image_url ? (
              <img
                src={rec.image_url}
                alt={rec.name}
                loading="lazy"
                className="w-full h-full object-contain p-2"
                onError={e => { e.currentTarget.style.display='none' }}
              />
            ) : (
              <svg className="w-10 h-10 text-gray-200" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd"/>
              </svg>
            )}
          </div>
          <div className="p-2">
            <span className={`inline-block text-xs font-bold px-2 py-0.5 rounded-full mb-1 ${rec.grade === 'A' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
              Grade {rec.grade}
            </span>
            {rec.brand && (
              <p className="text-[10px] font-semibold text-blue-900 uppercase tracking-wide truncate">{rec.brand}</p>
            )}
            <p className="text-xs font-semibold text-gray-800 line-clamp-2 leading-snug group-hover:text-green-700 transition-colors">
              {rec.name}
            </p>
          </div>
        </button>
      ))}
    </div>
  </div>
)}
```

---

## 5. backend/routes/product_new.py — full endpoint (add before the Browse section)

```python
@router.get("/recommendations")
async def get_recommendations(
    category: str = Query(..., description="Product category to match"),
    exclude_id: str = Query(None, description="Product ID to exclude"),
    limit: int = Query(6, ge=1, le=12),
):
    """
    Return A/B grade products in the same category — shown as better alternatives
    when the current product has a C or D grade.
    """
    try:
        cat = category.strip()
        cat_lower = cat.lower()
        _CATEGORY_GROUPS = {
            'soap': ['soap', 'body wash', 'personal care'],
            'face wash': ['face wash', 'skincare', 'personal care'],
            'moisturizer': ['moisturizer', 'moisturiser', 'lotion', 'cream', 'skincare'],
            'shampoo': ['shampoo', 'hair care', 'hair wash'],
            'conditioner': ['conditioner', 'hair care'],
            'sunscreen': ['sunscreen', 'sunblock', 'spf', 'skincare'],
            'serum': ['serum', 'skincare'],
            'biscuits': ['biscuits', 'cookies', 'bakery', 'snacks'],
            'chocolate': ['chocolate', 'confectionery', 'snacks'],
            'snacks': ['snacks', 'chips', 'crisps'],
            'instant noodles': ['instant noodles', 'noodles', 'pasta'],
            'soft drink': ['soft drink', 'beverage', 'carbonated'],
            'juice': ['juice', 'fruit drink', 'beverage'],
            'health drink': ['health drink', 'nutrition', 'beverage'],
            'toothpaste': ['toothpaste', 'oral care'],
            'deodorant': ['deodorant', 'antiperspirant', 'personal care'],
            'hair oil': ['hair oil', 'hair care'],
            'body lotion': ['body lotion', 'lotion', 'moisturiser', 'skincare'],
        }

        search_terms = None
        for key, terms in _CATEGORY_GROUPS.items():
            if key in cat_lower or any(t in cat_lower for t in terms):
                search_terms = terms
                break
        if not search_terms:
            search_terms = [cat_lower]

        results = []
        seen_ids = set()
        if exclude_id:
            seen_ids.add(str(exclude_id))

        for term in search_terms:
            if len(results) >= limit:
                break
            try:
                rows = (
                    supabase.from_("ai_extracted_products")
                    .select("id, name, brand, category, grade, image_url, static_key")
                    .ilike("category", f"%{term}%")
                    .in_("grade", ["A", "B"])
                    .order("grade")
                    .limit(limit * 3)
                    .execute()
                ).data or []

                for row in rows:
                    rid = str(row.get("id", ""))
                    if rid not in seen_ids and row.get("grade") in ("A", "B"):
                        seen_ids.add(rid)
                        results.append({
                            "id": rid,
                            "name": row["name"],
                            "brand": row.get("brand") or "",
                            "category": row.get("category") or "",
                            "grade": row.get("grade") or "B",
                            "image_url": row.get("image_url"),
                            "static_key": row.get("static_key") or "",
                        })
                        if len(results) >= limit:
                            break
            except Exception as e:
                print(f"[RECS] query error for term={term!r}: {e}")
                continue

        return results[:limit]

    except Exception as e:
        print(f"[RECS] error: {e}")
        return []
```
