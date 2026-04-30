import { useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { supabase } from '../lib/supabaseClient'
import SEO from '../components/SEO'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const BRAND_BLUE = '#1B3F8A'

function ScoreBadge({ score }) {
  const cls =
    score >= 75 ? 'bg-green-100 text-green-700' :
    score >= 50 ? 'bg-yellow-100 text-yellow-700' :
                  'bg-red-100 text-red-700'
  return (
    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${cls}`}>{score}</span>
  )
}

function BrowseCard({ product }) {
  const navigate = useNavigate()

  function handleClick() {
    navigate(`/result/${encodeURIComponent(product.name)}`)
  }

  return (
    <motion.div
      whileHover={{ y: -3, boxShadow: '0 8px 24px rgba(0,0,0,0.10)' }}
      transition={{ duration: 0.15 }}
      onClick={handleClick}
      className="bg-white rounded-2xl overflow-hidden cursor-pointer border border-gray-100 flex flex-col"
    >
      {/* Image */}
      <div className="aspect-square bg-gray-50 flex items-center justify-center overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-contain p-2"
            onError={e => { e.currentTarget.style.display = 'none' }}
          />
        ) : (
          <svg className="w-12 h-12 text-gray-200" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
          </svg>
        )}
      </div>

      {/* Info */}
      <div className="p-3 flex flex-col flex-1">
        <p className="text-[11px] font-semibold uppercase tracking-wide truncate mb-0.5" style={{ color: BRAND_BLUE }}>
          {product.brand}
        </p>
        <h3 className="text-sm font-semibold text-gray-800 line-clamp-2 flex-1 leading-snug">
          {product.name}
        </h3>
        <div className="flex items-center justify-between mt-2">
          <span className="text-[10px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded-full truncate max-w-[100px]">
            {product.category}
          </span>
          <ScoreBadge score={product.awareness_score} />
        </div>
      </div>

      <div className="px-3 pb-3">
        <button
          onClick={e => { e.stopPropagation(); handleClick() }}
          className="w-full py-1.5 text-xs font-semibold rounded-lg transition-colors"
          style={{ background: '#EFF4FF', color: BRAND_BLUE }}
          onMouseOver={e => { e.currentTarget.style.background = BRAND_BLUE; e.currentTarget.style.color = '#fff' }}
          onMouseOut={e => { e.currentTarget.style.background = '#EFF4FF'; e.currentTarget.style.color = BRAND_BLUE }}
        >
          Check Ingredients
        </button>
      </div>
    </motion.div>
  )
}

const CAT_ICON = {
  'Skincare': '✨', 'Hair Care': '💆', 'Personal Care': '🧴',
  'Cosmetics': '💄', 'Food': '🍱', 'Snacks': '🍿',
  'Beverages': '🥤', 'Soft Drink': '🫧', 'Health Drink': '🥛',
  'Biscuits': '🍪', 'Chocolate': '🍫', 'Nutrition': '🥗',
  'Protein Supplement': '💪', 'Baby Care': '👶', 'Oral Care': '🦷',
  'Household': '🏠', 'Dairy': '🫙', 'Instant Noodles': '🍜',
  'Spices': '🌶️', 'Condiments': '🫙', 'Cooking Oil': '🫙',
  'Breakfast Cereal': '🥣', 'Energy Drink': '⚡', 'Sports Drink': '🏃',
  'Health Supplement': '💊', 'Confectionery': '🍬', 'Bakery': '🥖',
  'Ready to Eat': '🍽️', 'Pickles': '🥒', 'Fruit Drink': '🍹',
  'Fruit Juice': '🍊', 'Dessert': '🍨',
}

const SORT_OPTIONS = [
  { value: 'score', label: 'Best Score' },
  { value: 'name',  label: 'Name A–Z' },
  { value: 'brand', label: 'Brand A–Z' },
]

export default function Products() {
  const [products, setProducts]     = useState([])
  const [loading, setLoading]       = useState(true)
  const [allCategories, setAllCats] = useState([])
  const [brands, setBrands]         = useState([])
  const [category, setCategory]     = useState('')
  const [brand, setBrand]           = useState('')
  const [searchInput, setSearchInput] = useState('')  // raw input
  const [q, setQ]                   = useState('')    // debounced
  const [page, setPage]             = useState(1)
  const [total, setTotal]           = useState(0)
  const [pages, setPages]           = useState(1)
  const [sort, setSort]             = useState('score')
  const limit = 24
  const debounceRef = useRef(null)

  // Debounce search input → q (300ms)
  useEffect(() => {
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      setQ(searchInput)
      setPage(1)
    }, 300)
    return () => clearTimeout(debounceRef.current)
  }, [searchInput])

  // Single fetch effect — runs when any filter/sort/page changes
  const fetchProducts = useCallback(async () => {
    setLoading(true)
    try {
      const params = { page, limit, sort }
      if (category) params.category = category
      if (brand)    params.brand    = brand
      if (q)        params.q        = q
      const res = await axios.get(`${API_BASE_URL}/api/product/browse`, { params })
      const data = res.data
      const pageProducts = data.products || []

      // Batch-fetch uploaded photos for this page's products
      if (pageProducts.length > 0) {
        const ids = pageProducts.map(p => p.id)
        const { data: photos } = await supabase
          .from('product_photos')
          .select('product_id, image_url')
          .in('product_id', ids)
          .order('created_at')
        if (photos?.length) {
          const photoMap = {}
          photos.forEach(ph => { if (!photoMap[ph.product_id]) photoMap[ph.product_id] = ph.image_url })
          pageProducts.forEach(p => { if (!p.image_url && photoMap[p.id]) p.image_url = photoMap[p.id] })
        }
      }

      setProducts(pageProducts)
      setTotal(data.total || 0)
      setPages(data.pages || 1)
      if (data.categories?.length) setAllCats(data.categories)
      if (data.brands?.length)     setBrands(data.brands)
    } catch (err) {
      console.error('Browse error:', err)
      setProducts([])
    } finally {
      setLoading(false)
    }
  }, [category, brand, q, page, sort])

  useEffect(() => { fetchProducts() }, [fetchProducts])

  // When category changes → reset brand + page
  function handleCategory(cat) {
    setCategory(cat)
    setBrand('')
    setPage(1)
  }

  // When brand changes → reset page
  function handleBrand(b) {
    setBrand(b)
    setPage(1)
  }

  function clearAll() {
    setCategory('')
    setBrand('')
    setSearchInput('')
    setQ('')
    setPage(1)
    setSort('score')
  }

  const anyFilter = category || brand || q

  return (
    <>
      <SEO
        title="Product Directory — Browse 600+ Indian Products"
        description="Browse and search 600+ Indian food and cosmetic products. Filter by category or brand, check ingredients, and see FSSAI awareness scores."
        keywords="Indian food products list, cosmetic products India, browse product ingredients, FSSAI product database, food product directory India"
        canonical="/products"
      />
    <div className="min-h-screen bg-gray-50">

      {/* ── Hero strip ── */}
      <div className="bg-white border-b border-gray-100 py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl md:text-3xl font-bold mb-1" style={{ color: BRAND_BLUE }}>
            Product Directory
          </h1>
          <p className="text-gray-500 text-sm mb-5">
            <span className="font-semibold text-gray-700">{total || '570+'}</span> products
            {category ? ` in ${category}` : ''} · click any to see full ingredient breakdown
          </p>

          {/* Search box */}
          <div className="relative max-w-md">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search products or brands…"
              value={searchInput}
              onChange={e => setSearchInput(e.target.value)}
              className="w-full pl-9 pr-9 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none bg-gray-50"
              style={{ '--tw-ring-color': BRAND_BLUE }}
              onFocus={e => { e.target.style.borderColor = BRAND_BLUE; e.target.style.boxShadow = `0 0 0 2px ${BRAND_BLUE}22` }}
              onBlur={e => { e.target.style.borderColor = ''; e.target.style.boxShadow = '' }}
            />
            {searchInput && (
              <button
                onClick={() => { setSearchInput(''); setQ('') }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-lg leading-none"
              >
                ×
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">

        {/* ── Category pills ── */}
        <div className="mb-3 overflow-x-auto pb-2" style={{ scrollbarWidth: 'none' }}>
          <div className="flex gap-2 min-w-max">
            <button
              onClick={() => handleCategory('')}
              className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium border transition-all whitespace-nowrap"
              style={!category ? { background: BRAND_BLUE, color: '#fff', borderColor: BRAND_BLUE } : { background: '#fff', color: '#374151', borderColor: '#E5E7EB' }}
            >
              🔍 All
            </button>
            {allCategories.map(cat => (
              <button
                key={cat}
                onClick={() => handleCategory(cat)}
                className="flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium border transition-all whitespace-nowrap"
                style={category === cat ? { background: BRAND_BLUE, color: '#fff', borderColor: BRAND_BLUE } : { background: '#fff', color: '#374151', borderColor: '#E5E7EB' }}
              >
                {CAT_ICON[cat] || '📦'} {cat}
              </button>
            ))}
          </div>
        </div>

        {/* ── Brand chips (shown when a category is selected or few brands) ── */}
        <AnimatePresence>
          {brands.length > 0 && brands.length <= 60 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-4 overflow-x-auto pb-2"
              style={{ scrollbarWidth: 'none' }}
            >
              <div className="flex gap-2 min-w-max">
                <button
                  onClick={() => handleBrand('')}
                  className="px-3 py-1.5 rounded-full text-xs font-medium border transition-all"
                  style={!brand ? { background: '#1f2937', color: '#fff', borderColor: '#1f2937' } : { background: '#fff', color: '#6b7280', borderColor: '#E5E7EB' }}
                >
                  All Brands
                </button>
                {brands.map(b => (
                  <button
                    key={b}
                    onClick={() => handleBrand(b)}
                    className="px-3 py-1.5 rounded-full text-xs font-medium border transition-all whitespace-nowrap"
                    style={brand === b ? { background: '#1f2937', color: '#fff', borderColor: '#1f2937' } : { background: '#fff', color: '#6b7280', borderColor: '#E5E7EB' }}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Toolbar: count + sort + clear ── */}
        <div className="flex items-center justify-between mb-5 flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <p className="text-sm text-gray-500">
              {loading ? 'Loading…' : (
                <><span className="font-semibold text-gray-800">{total}</span> products
                  {brand ? ` · ${brand}` : ''}
                </>
              )}
            </p>
            {anyFilter && (
              <button onClick={clearAll} className="text-xs px-2 py-1 rounded-md text-red-500 border border-red-200 hover:bg-red-50 transition-colors">
                Clear filters
              </button>
            )}
          </div>
          <div className="flex border border-gray-200 rounded-lg overflow-hidden text-xs">
            {SORT_OPTIONS.map(o => (
              <button
                key={o.value}
                onClick={() => { setSort(o.value); setPage(1) }}
                className="px-3 py-1.5 transition-colors"
                style={sort === o.value ? { background: BRAND_BLUE, color: '#fff' } : { background: '#fff', color: '#374151' }}
              >
                {o.label}
              </button>
            ))}
          </div>
        </div>

        {/* ── Grid ── */}
        {loading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl overflow-hidden border border-gray-100 animate-pulse">
                <div className="aspect-square bg-gray-100" />
                <div className="p-3 space-y-2">
                  <div className="h-2 bg-gray-100 rounded w-1/2" />
                  <div className="h-3 bg-gray-100 rounded" />
                  <div className="h-3 bg-gray-100 rounded w-3/4" />
                </div>
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-5xl mb-4">🔍</p>
            <h3 className="text-lg font-semibold text-gray-700 mb-1">No products found</h3>
            <p className="text-gray-400 text-sm mb-4">Try a different filter or search term</p>
            <button onClick={clearAll} className="text-sm font-medium px-4 py-2 rounded-lg border" style={{ color: BRAND_BLUE, borderColor: BRAND_BLUE }}>
              Clear all filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {products.map(p => (
              <BrowseCard key={p.id} product={p} />
            ))}
          </div>
        )}

        {/* ── Pagination ── */}
        {!loading && pages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-10 flex-wrap">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 text-sm rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              ← Prev
            </button>
            <div className="flex gap-1 flex-wrap justify-center">
              {(() => {
                const half = 3
                let start = Math.max(1, page - half)
                let end   = Math.min(pages, start + 2 * half)
                start = Math.max(1, end - 2 * half)
                return Array.from({ length: end - start + 1 }, (_, i) => start + i)
              })().map(num => (
                <button
                  key={num}
                  onClick={() => setPage(num)}
                  className="w-9 h-9 text-sm rounded-lg font-medium transition-colors"
                  style={page === num ? { background: BRAND_BLUE, color: '#fff' } : { background: '#fff', border: '1px solid #E5E7EB', color: '#374151' }}
                >
                  {num}
                </button>
              ))}
            </div>
            <button
              onClick={() => setPage(p => Math.min(pages, p + 1))}
              disabled={page === pages}
              className="px-4 py-2 text-sm rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </div>
    </>
  )
}
