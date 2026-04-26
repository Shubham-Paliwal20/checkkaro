import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Score badge colour
function ScoreBadge({ score }) {
  const color =
    score >= 75 ? 'bg-green-100 text-green-700' :
    score >= 50 ? 'bg-yellow-100 text-yellow-700' :
                  'bg-red-100 text-red-700'
  return (
    <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${color}`}>
      {score}
    </span>
  )
}

// Minimal product card
function BrowseCard({ product }) {
  const navigate = useNavigate()
  return (
    <motion.div
      whileHover={{ y: -4, boxShadow: '0 8px 24px rgba(0,0,0,0.10)' }}
      transition={{ duration: 0.18 }}
      onClick={() => navigate(`/result/${encodeURIComponent(product.name)}`)}
      className="bg-white rounded-2xl overflow-hidden cursor-pointer border border-gray-100 flex flex-col"
    >
      {/* Image */}
      <div className="aspect-square bg-gray-50 flex items-center justify-center overflow-hidden">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-full object-contain p-2"
            onError={e => { e.target.style.display = 'none' }}
          />
        ) : (
          <div className="flex flex-col items-center text-gray-300">
            <svg className="w-12 h-12 mb-1" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="p-3 flex flex-col flex-1">
        <p className="text-[11px] font-semibold text-blue-500 uppercase tracking-wide truncate mb-0.5">
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

      {/* Check button */}
      <div className="px-3 pb-3">
        <button className="w-full py-1.5 text-xs font-semibold rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white transition-colors">
          Check Ingredients
        </button>
      </div>
    </motion.div>
  )
}

export default function Products() {
  const [products, setProducts]   = useState([])
  const [loading, setLoading]     = useState(true)
  const [categories, setCategories] = useState([])
  const [brands, setBrands]       = useState([])
  const [category, setCategory]   = useState('')
  const [brand, setBrand]         = useState('')
  const [q, setQ]                 = useState('')
  const [page, setPage]           = useState(1)
  const [total, setTotal]         = useState(0)
  const [pages, setPages]         = useState(1)
  const [sort, setSort]           = useState('score')
  const limit = 24
  const brandRef = useRef(null)

  useEffect(() => { fetch() }, [category, brand, q, page, sort])

  // reset page when filters change
  useEffect(() => { setPage(1); setBrand('') }, [category])
  useEffect(() => { setPage(1) }, [brand, q, sort])

  async function fetch() {
    setLoading(true)
    try {
      const params = { page, limit, sort }
      if (category) params.category = category
      if (brand)    params.brand = brand
      if (q)        params.q = q
      const res = await axios.get(`${API_BASE_URL}/api/product/browse`, { params })
      setProducts(res.data.products)
      setTotal(res.data.total)
      setPages(res.data.pages)
      if (res.data.categories.length) setCategories(res.data.categories)
      if (res.data.brands.length)     setBrands(res.data.brands)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  // Category emoji map
  const catIcon = {
    'Skincare': '✨', 'Hair Care': '💆', 'Personal Care': '🧴',
    'Cosmetics': '💄', 'Food': '🍱', 'Snacks': '🍿',
    'Beverages': '🥤', 'Soft Drink': '🫧', 'Health Drink': '🥛',
    'Biscuits': '🍪', 'Chocolate': '🍫', 'Nutrition': '🥗',
    'Protein Supplement': '💪', 'Baby Care': '👶', 'Oral Care': '🦷',
    'Household': '🏠', 'Dairy': '🥛', 'Instant Noodles': '🍜',
    'Spices': '🌶️', 'Condiments': '🫙', 'Cooking Oil': '🫙',
    'Breakfast Cereal': '🥣', 'Energy Drink': '⚡', 'Sports Drink': '🏃',
  }

  const sortOptions = [
    { value: 'score', label: 'Best Score' },
    { value: 'name',  label: 'Name A–Z' },
    { value: 'brand', label: 'Brand A–Z' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* ── Hero strip ── */}
      <div className="bg-white border-b border-gray-100 py-8 px-4">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mb-1">
            Product Directory
          </h1>
          <p className="text-gray-500 text-sm mb-5">
            {total > 0 ? `${total} products` : '570+ products'} · click any to see full ingredient breakdown
          </p>

          {/* Search */}
          <div className="relative max-w-md">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              type="text"
              placeholder="Search products or brands…"
              value={q}
              onChange={e => setQ(e.target.value)}
              className="w-full pl-9 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
            />
            {q && (
              <button onClick={() => setQ('')} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">✕</button>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* ── Category pills ── */}
        <div className="mb-4 overflow-x-auto pb-2 scrollbar-hide">
          <div className="flex gap-2 min-w-max">
            <button
              onClick={() => { setCategory(''); setBrand('') }}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium border transition-all whitespace-nowrap ${
                !category ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'
              }`}
            >
              🔍 All
            </button>
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium border transition-all whitespace-nowrap ${
                  category === cat ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'
                }`}
              >
                {catIcon[cat] || '📦'} {cat}
              </button>
            ))}
          </div>
        </div>

        {/* ── Brand pills (contextual) ── */}
        <AnimatePresence>
          {(category || brands.length < 40) && brands.length > 0 && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="mb-5 overflow-x-auto pb-2 scrollbar-hide"
              ref={brandRef}
            >
              <div className="flex gap-2 min-w-max">
                <button
                  onClick={() => setBrand('')}
                  className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all ${
                    !brand ? 'bg-gray-800 text-white border-gray-800' : 'bg-white text-gray-500 border-gray-200 hover:border-gray-400'
                  }`}
                >
                  All Brands
                </button>
                {brands.map(b => (
                  <button
                    key={b}
                    onClick={() => setBrand(b)}
                    className={`px-3 py-1.5 rounded-full text-xs font-medium border transition-all whitespace-nowrap ${
                      brand === b ? 'bg-gray-800 text-white border-gray-800' : 'bg-white text-gray-500 border-gray-200 hover:border-gray-400'
                    }`}
                  >
                    {b}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Toolbar: count + sort ── */}
        <div className="flex items-center justify-between mb-5">
          <p className="text-sm text-gray-500">
            {loading ? 'Loading…' : (
              <>
                <span className="font-semibold text-gray-800">{total}</span> products
                {category ? ` in ${category}` : ''}
                {brand ? ` · ${brand}` : ''}
              </>
            )}
          </p>
          <div className="flex items-center gap-2">
            <span className="text-xs text-gray-400 hidden sm:inline">Sort:</span>
            <div className="flex border border-gray-200 rounded-lg overflow-hidden text-xs">
              {sortOptions.map(o => (
                <button
                  key={o.value}
                  onClick={() => setSort(o.value)}
                  className={`px-3 py-1.5 transition-colors ${sort === o.value ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 hover:bg-gray-50'}`}
                >
                  {o.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ── Product Grid ── */}
        {loading ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="bg-white rounded-2xl overflow-hidden border border-gray-100 animate-pulse">
                <div className="aspect-square bg-gray-100" />
                <div className="p-3">
                  <div className="h-2 bg-gray-100 rounded mb-2 w-1/2" />
                  <div className="h-3 bg-gray-100 rounded mb-1" />
                  <div className="h-3 bg-gray-100 rounded w-3/4" />
                </div>
              </div>
            ))}
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-5xl mb-4">🔍</p>
            <h3 className="text-lg font-semibold text-gray-700 mb-1">No products found</h3>
            <p className="text-gray-400 text-sm">Try a different filter or search term</p>
            <button onClick={() => { setCategory(''); setBrand(''); setQ('') }} className="mt-4 text-blue-600 text-sm hover:underline">
              Clear all filters
            </button>
          </div>
        ) : (
          <motion.div
            layout
            className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4"
          >
            {products.map(p => (
              <BrowseCard key={p.id} product={p} />
            ))}
          </motion.div>
        )}

        {/* ── Pagination ── */}
        {!loading && pages > 1 && (
          <div className="flex justify-center items-center gap-2 mt-10">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              ← Prev
            </button>
            <div className="flex gap-1">
              {Array.from({ length: Math.min(7, pages) }, (_, i) => {
                let num
                if (pages <= 7) {
                  num = i + 1
                } else if (page <= 4) {
                  num = i + 1
                } else if (page >= pages - 3) {
                  num = pages - 6 + i
                } else {
                  num = page - 3 + i
                }
                return (
                  <button
                    key={num}
                    onClick={() => setPage(num)}
                    className={`w-9 h-9 text-sm rounded-lg font-medium transition-colors ${
                      page === num ? 'bg-blue-600 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    {num}
                  </button>
                )
              })}
            </div>
            <button
              onClick={() => setPage(p => Math.min(pages, p + 1))}
              disabled={page === pages}
              className="px-4 py-2 text-sm rounded-lg border border-gray-200 bg-white hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
