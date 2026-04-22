import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'

// Session-level cache so repeated keystrokes don't re-hit the server
const suggestionsCache = new Map()

function SearchBar({ placeholder = "Search any product...", onSearch }) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const navigate = useNavigate()
  const searchRef = useRef(null)
  const suggestionsRef = useRef(null)

  useEffect(() => {
    if (query.length < 1) {
      setSuggestions([])
      setShowSuggestions(false)
      return
    }

    // Return cached result immediately — no network round-trip
    if (suggestionsCache.has(query)) {
      setSuggestions(suggestionsCache.get(query))
      setShowSuggestions(true)
      return
    }

    const fetchSuggestions = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/product/suggestions`, {
          params: { q: query }
        })
        const results = response.data.suggestions || []
        suggestionsCache.set(query, results)
        setSuggestions(results)
        setShowSuggestions(true)
      } catch {
        setSuggestions([])
      }
    }

    const debounceTimer = setTimeout(fetchSuggestions, 150)
    return () => clearTimeout(debounceTimer)
  }, [query])

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) return

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : 0
        )
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex(prev => 
          prev > 0 ? prev - 1 : suggestions.length - 1
        )
        break
      case 'Enter':
        e.preventDefault()
        if (selectedIndex >= 0) {
          selectSuggestion(suggestions[selectedIndex])
        } else {
          handleSubmit(e)
        }
        break
      case 'Escape':
        setShowSuggestions(false)
        setSelectedIndex(-1)
        break
    }
  }

  const selectSuggestion = (suggestion) => {
    setQuery(suggestion.name)
    setShowSuggestions(false)
    setSelectedIndex(-1)
    
    // Navigate to result immediately
    if (onSearch) {
      onSearch(suggestion.name)
    } else {
      navigate(`/result/${encodeURIComponent(suggestion.name)}`)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      setShowSuggestions(false)
      if (onSearch) {
        onSearch(query.trim())
      } else {
        navigate(`/result/${encodeURIComponent(query.trim())}`)
      }
    }
  }

  const handleInputChange = (e) => {
    setQuery(e.target.value)
    setSelectedIndex(-1)
  }

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false)
        setSelectedIndex(-1)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div ref={searchRef} className="w-full relative">
      <form onSubmit={handleSubmit} className="w-full">
        <div className="flex items-center bg-white rounded-full border-2 border-gray-200 focus-within:border-primary shadow-lg overflow-hidden h-[60px] sm:h-[72px] transition-colors">
          <svg className="w-5 h-5 sm:w-6 sm:h-6 text-gray-400 ml-4 sm:ml-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className="flex-1 px-3 sm:px-4 text-base sm:text-lg outline-none font-inter"
            autoComplete="off"
          />
          <button
            type="submit"
            className="bg-orange text-white rounded-full mr-2 px-4 sm:px-8 py-2 sm:py-3 hover:bg-orange-dark transition-colors font-semibold text-sm sm:text-base"
          >
            <span className="hidden sm:inline">Search</span>
            <svg className="w-4 h-4 sm:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
        </div>
      </form>

      {/* Suggestions Dropdown */}
      {showSuggestions && suggestions.length > 0 && (
        <div 
          ref={suggestionsRef}
          className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-xl z-50 mt-2 max-h-80 overflow-y-auto"
        >
          {suggestions.map((suggestion, index) => (
            <div
              key={index}
              onClick={() => selectSuggestion(suggestion)}
              className={`px-3 sm:px-4 py-3 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors ${
                index === selectedIndex 
                  ? 'bg-primary-light text-primary' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <div className="flex items-center gap-2 sm:gap-3">
                <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900 text-sm sm:text-base truncate">
                    {suggestion.name}
                  </div>
                  <div className="text-xs sm:text-sm text-gray-500 truncate">
                    {suggestion.brand} • {suggestion.category}
                  </div>
                </div>
                <svg className="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          ))}
          
          {/* Show "Search for..." option */}
          <div
            onClick={handleSubmit}
            className={`px-3 sm:px-4 py-3 cursor-pointer transition-colors border-t border-gray-200 ${
              selectedIndex === suggestions.length 
                ? 'bg-primary-light text-primary' 
                : 'hover:bg-gray-50'
            }`}
          >
            <div className="flex items-center gap-2 sm:gap-3">
              <svg className="w-4 h-4 text-primary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <div className="font-medium text-primary text-sm sm:text-base truncate">
                Search for "{query}"
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SearchBar
