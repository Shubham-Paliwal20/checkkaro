import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'

// Session-level cache — survives re-renders, cleared only on tab close
const suggestionsCache = new Map()

// Silent pre-warm: fetch these prefixes on mount so first keystrokes are instant
const PREWARM_CHARS = ['m', 'p', 'a', 'd', 'k', 'h', 'b', 'n', 'c', 'l', 's', 't', 'r', 'f', 'g']

// Shown immediately when user focuses the empty search box
const POPULAR = [
  { name: 'Maggi 2-Minute Masala Noodles', brand: 'Maggi', category: 'Instant Noodles' },
  { name: 'Parle-G', brand: 'Parle', category: 'Biscuits' },
  { name: 'Amul Butter', brand: 'Amul', category: 'Dairy' },
  { name: 'Dove Soap', brand: 'Dove', category: 'Personal Care' },
  { name: 'Kurkure Masala Munch', brand: 'Kurkure', category: 'Snacks' },
  { name: 'Cadbury Dairy Milk', brand: 'Cadbury', category: 'Chocolate' },
  { name: 'Thums Up', brand: 'Coca-Cola', category: 'Soft Drink' },
  { name: 'Himalaya Neem Face Wash', brand: 'Himalaya', category: 'Skincare' },
]

function SearchBar({ placeholder = 'Search any product...', onSearch }) {
  const [query, setQuery]               = useState('')
  const [suggestions, setSuggestions]   = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [isPopular, setIsPopular]       = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const [loading, setLoading]           = useState(false)
  const navigate  = useNavigate()
  const searchRef = useRef(null)
  const timerRef  = useRef(null)

  // ── Pre-warm cache on mount (background, staggered so server isn't hit at once) ──
  useEffect(() => {
    const warm = async (char) => {
      if (suggestionsCache.has(char)) return
      try {
        const r = await axios.get(`${API_BASE_URL}/api/product/suggestions`, {
          params: { q: char },
          timeout: 8000,
        })
        suggestionsCache.set(char, r.data.suggestions || [])
      } catch {}
    }
    const ids = PREWARM_CHARS.map((c, i) => setTimeout(() => warm(c), i * 50))
    return () => ids.forEach(id => clearTimeout(id))
  }, [])

  // ── Fetch suggestions with 250ms debounce ──
  useEffect(() => {
    clearTimeout(timerRef.current)

    if (query.length < 1) {
      setSuggestions([])
      setShowSuggestions(false)
      setLoading(false)
      return
    }

    // Cache hit → instant, zero loading state
    if (suggestionsCache.has(query)) {
      setSuggestions(suggestionsCache.get(query))
      setIsPopular(false)
      setShowSuggestions(true)
      setLoading(false)
      return
    }

    // Cache miss → show spinner, wait 80ms before hitting the server
    setLoading(true)
    const abortController = new AbortController()
    timerRef.current = setTimeout(async () => {
      try {
        const [backendRes] = await Promise.allSettled([
          axios.get(`${API_BASE_URL}/api/product/suggestions`, { params: { q: query }, timeout: 5000, signal: abortController.signal }),
        ])

        const backendResults = backendRes.status === 'fulfilled' ? (backendRes.value.data.suggestions || []) : []

        const seen = new Set()
        const final = backendResults.filter(s => {
          const k = s.name.toLowerCase()
          if (seen.has(k)) return false
          seen.add(k)
          return true
        }).slice(0, 30)

        // Cap cache at 100 entries (each entry now holds up to 30 results)
        if (suggestionsCache.size >= 100) {
          suggestionsCache.delete(suggestionsCache.keys().next().value)
        }
        suggestionsCache.set(query, final)
        setSuggestions(final)
        setIsPopular(false)
        setShowSuggestions(true)
      } catch {
        setSuggestions([])
      } finally {
        setLoading(false)
      }
    }, 250)

    return () => { clearTimeout(timerRef.current); abortController.abort() }
  }, [query])

  // ── Close on outside click ──
  useEffect(() => {
    const handler = (e) => {
      if (searchRef.current && !searchRef.current.contains(e.target)) {
        setShowSuggestions(false)
        setSelectedIndex(-1)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  // ── Show popular on focus (empty box) ──
  const handleFocus = () => {
    if (query.length === 0) {
      setSuggestions(POPULAR)
      setIsPopular(true)
      setShowSuggestions(true)
    } else if (suggestions.length > 0) {
      setShowSuggestions(true)
    }
  }

  // ── Keyboard navigation ──
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setSelectedIndex(i => (i < suggestions.length - 1 ? i + 1 : 0))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setSelectedIndex(i => (i > 0 ? i - 1 : suggestions.length - 1))
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (selectedIndex >= 0) selectSuggestion(suggestions[selectedIndex])
      else handleSubmit(e)
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
      setSelectedIndex(-1)
    }
  }

  const selectSuggestion = (s) => {
    setQuery(s.name)
    setShowSuggestions(false)
    setSelectedIndex(-1)
    if (onSearch) onSearch(s.name)
    else navigate(`/result/${encodeURIComponent(s.name)}`)
  }

  const handleSubmit = (e) => {
    e?.preventDefault()
    if (query.trim()) {
      setShowSuggestions(false)
      if (onSearch) onSearch(query.trim())
      else navigate(`/result/${encodeURIComponent(query.trim())}`)
    }
  }

  return (
    <div ref={searchRef} className="w-full relative">
      <form onSubmit={handleSubmit} className="w-full">
        <div className="flex items-center bg-white rounded-full border-2 border-gray-200 focus-within:border-primary shadow-lg overflow-hidden h-[60px] sm:h-[72px] transition-colors">
          {/* Search icon */}
          <svg className="w-5 h-5 sm:w-6 sm:h-6 text-gray-400 ml-4 sm:ml-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>

          <input
            type="text"
            value={query}
            onChange={e => { setQuery(e.target.value); setSelectedIndex(-1) }}
            onKeyDown={handleKeyDown}
            onFocus={handleFocus}
            placeholder={placeholder}
            className="flex-1 px-3 sm:px-4 text-base sm:text-lg outline-none font-inter bg-transparent"
            autoComplete="off"
            spellCheck={false}
          />

          {/* Loading spinner — only visible while fetching */}
          {loading && (
            <svg className="animate-spin w-5 h-5 text-gray-300 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          )}

          {/* Clear button when there's text */}
          {query && !loading && (
            <button
              type="button"
              onClick={() => { setQuery(''); setSuggestions(POPULAR); setIsPopular(true); setShowSuggestions(true) }}
              className="mr-2 text-gray-400 hover:text-gray-600 flex-shrink-0 text-xl leading-none"
              tabIndex={-1}
            >
              ×
            </button>
          )}

          <button
            type="submit"
            className="bg-orange text-white rounded-full mr-2 px-4 sm:px-8 py-2 sm:py-3 hover:bg-orange-dark transition-colors font-semibold text-sm sm:text-base flex-shrink-0"
          >
            <span className="hidden sm:inline">Search</span>
            <svg className="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </form>

      {/* ── Suggestions dropdown ── */}
      {showSuggestions && suggestions.length > 0 && (
        <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-2xl shadow-xl z-50 mt-2 overflow-hidden">

          {/* Header row */}
          <div className="px-4 py-2 border-b border-gray-100 flex items-center gap-2">
            {isPopular ? (
              <>
                <svg className="w-3.5 h-3.5 text-orange" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Popular searches</span>
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
                  {suggestions.length} result{suggestions.length !== 1 ? 's' : ''}
                </span>
              </>
            )}
          </div>

          {/* Suggestion rows */}
          <div className="max-h-72 overflow-y-auto">
            {suggestions.map((s, i) => (
              <div
                key={i}
                onMouseDown={() => selectSuggestion(s)}
                className={`px-4 py-3 cursor-pointer border-b border-gray-50 last:border-b-0 transition-colors ${
                  i === selectedIndex ? 'bg-blue-50' : 'hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0 text-xs font-bold text-gray-400">
                    {s.name.charAt(0).toUpperCase()}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-gray-900 text-sm truncate">{s.name}</div>
                    <div className="flex items-center gap-1 text-xs text-gray-400 min-w-0">
                      {!isPopular && query && s.brand && s.brand.toLowerCase().includes(query.toLowerCase()) && (
                        <span className="bg-orange/10 text-orange px-1.5 py-0.5 rounded-full text-[10px] font-semibold flex-shrink-0">brand</span>
                      )}
                      <span className="truncate">{s.brand} · {s.category}</span>
                    </div>
                  </div>
                  <svg className="w-4 h-4 text-gray-300 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            ))}
          </div>

          {/* "Search for..." footer (only when typing, not on popular) */}
          {!isPopular && query && (
            <div
              onMouseDown={handleSubmit}
              className="px-4 py-3 cursor-pointer hover:bg-gray-50 border-t border-gray-100 transition-colors"
            >
              <div className="flex items-center gap-3">
                <div className="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0" style={{ background: '#EFF4FF' }}>
                  <svg className="w-3.5 h-3.5" style={{ color: '#1B3F8A' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <span className="font-medium text-sm" style={{ color: '#1B3F8A' }}>
                  Search for "<span className="font-bold">{query}</span>"
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SearchBar
