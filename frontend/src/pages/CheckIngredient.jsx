import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import DisclaimerBox from '../components/DisclaimerBox'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'

function CheckIngredient() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [ingredient, setIngredient] = useState(null)
  const [error, setError] = useState(null)
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  const [popularIngredients, setPopularIngredients] = useState([])
  
  const searchRef = useRef(null)

  // Fetch popular ingredients on mount
  useEffect(() => {
    fetchPopularIngredients()
  }, [])

  // Fetch suggestions when user types
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.length >= 1) {
        try {
          const response = await axios.get(`${API_BASE_URL}/api/ingredient/suggestions`, {
            params: { q: query, limit: 8 }
          })
          setSuggestions(response.data || [])
          setShowSuggestions(true)
        } catch (error) {
          console.error('Error fetching suggestions:', error)
          setSuggestions([])
        }
      } else {
        setSuggestions([])
        setShowSuggestions(false)
      }
    }

    const debounceTimer = setTimeout(fetchSuggestions, 200)
    return () => clearTimeout(debounceTimer)
  }, [query])

  const fetchPopularIngredients = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/ingredient/popular`, {
        params: { limit: 16 }
      })
      setPopularIngredients(response.data || [])
    } catch (error) {
      console.error('Error fetching popular ingredients:', error)
      // Fallback to hardcoded list
      setPopularIngredients([
        { name: 'TBHQ', classification: 'commonly_questioned' },
        { name: 'Tartrazine', classification: 'commonly_questioned' },
        { name: 'MSG', classification: 'commonly_questioned' },
        { name: 'Sodium Benzoate', classification: 'commonly_questioned' },
        { name: 'Sunset Yellow', classification: 'commonly_questioned' },
        { name: 'Carrageenan', classification: 'worth_knowing' },
        { name: 'Palm Oil', classification: 'worth_knowing' },
        { name: 'Aspartame', classification: 'commonly_questioned' }
      ])
    }
  }

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
    handleSearch(suggestion.name)
  }

  const handleSearch = async (searchQuery) => {
    const queryToSearch = searchQuery || query
    if (!queryToSearch.trim()) return

    try {
      setLoading(true)
      setError(null)
      setShowSuggestions(false)
      const response = await axios.get(`${API_BASE_URL}/api/ingredient/search`, {
        params: { name: queryToSearch }
      })
      setIngredient(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch ingredient information')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    handleSearch()
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

  const getClassificationBadge = (classification) => {
    const badges = {
      generally_recognised: { 
        bg: 'bg-green-100', 
        text: 'text-green-700', 
        label: 'Generally Recognised',
        borderColor: 'border-green-300'
      },
      worth_knowing: { 
        bg: 'bg-red-100', 
        text: 'text-red-700', 
        label: 'Worth Knowing',
        borderColor: 'border-red-300'
      },
      commonly_questioned: { 
        bg: 'bg-red-200', 
        text: 'text-red-800', 
        label: 'Commonly Questioned',
        borderColor: 'border-red-400'
      }
    }
    const badge = badges[classification] || badges.worth_knowing
    return (
      <span className={`inline-block px-3 sm:px-4 py-1.5 sm:py-2 rounded-full text-xs sm:text-sm font-semibold ${badge.bg} ${badge.text}`}>
        {badge.label}
      </span>
    )
  }

  const getCardStyle = (classification) => {
    if (classification === 'generally_recognised') {
      return 'border-l-4 border-green-500 bg-green-50'
    } else if (classification === 'commonly_questioned') {
      return 'border-l-4 border-red-600 bg-red-50'
    } else {
      return 'border-l-4 border-red-400 bg-red-50'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {/* Hero Section - Mobile Optimized */}
      <section className="bg-navy text-white py-12 sm:py-16 md:py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="inline-block mb-3 sm:mb-4">
            <span className="inline-block px-3 sm:px-4 py-1.5 sm:py-2 rounded-full border border-primary text-primary text-xs sm:text-sm font-medium">
              Ingredient Checker
            </span>
          </div>
          
          <h1 className="font-poppins font-bold text-2xl sm:text-3xl md:text-4xl lg:text-5xl mb-3 sm:mb-4 px-2">
            What does this ingredient do?
          </h1>
          
          <p className="text-gray-300 text-sm sm:text-base md:text-lg mb-6 sm:mb-8 px-2">
            Type any ingredient name or E-number from a product label
          </p>

          {/* Enhanced Search Bar with Suggestions - Mobile Optimized */}
          <div ref={searchRef} className="max-w-xl mx-auto relative">
            <form onSubmit={handleSubmit}>
              <div className="flex items-center bg-white rounded-full overflow-hidden h-[48px] sm:h-[56px] md:h-[60px] shadow-lg">
                <svg className="w-4 h-4 sm:w-5 sm:h-5 md:w-6 md:h-6 text-gray-400 ml-3 sm:ml-4 md:ml-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  type="text"
                  value={query}
                  onChange={handleInputChange}
                  onKeyDown={handleKeyDown}
                  placeholder="e.g. Tartrazine, MSG..."
                  className="flex-1 px-2 sm:px-3 md:px-4 text-sm sm:text-base text-gray-900 outline-none min-w-0"
                  autoComplete="off"
                />
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-primary text-white rounded-full mr-1.5 sm:mr-2 px-3 sm:px-4 md:px-6 py-1.5 sm:py-2 hover:bg-primary-dark transition-colors font-semibold disabled:opacity-50 text-xs sm:text-sm md:text-base flex-shrink-0"
                >
                  {loading ? 'Searching...' : 'Search'}
                </button>
              </div>
            </form>

            {/* Suggestions Dropdown - Mobile Optimized */}
            {showSuggestions && suggestions.length > 0 && (
              <div 
                className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded-lg shadow-xl z-50 mt-2 max-h-72 sm:max-h-80 overflow-y-auto"
              >
                {suggestions.map((suggestion, index) => (
                  <div
                    key={suggestion.id}
                    onClick={() => selectSuggestion(suggestion)}
                    className={`px-3 sm:px-4 py-2.5 sm:py-3 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors ${
                      index === selectedIndex 
                        ? 'bg-primary-light text-primary' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-2 sm:gap-3">
                      <div className={`w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full flex-shrink-0 ${
                        suggestion.classification === 'commonly_questioned' ? 'bg-red-600' :
                        suggestion.classification === 'worth_knowing' ? 'bg-red-400' :
                        'bg-green-500'
                      }`}></div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 text-sm sm:text-base truncate">
                          {suggestion.name}
                        </div>
                        <div className="text-xs sm:text-sm text-gray-600 line-clamp-1">
                          {suggestion.what_it_is}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Results Section */}
      {ingredient && (
        <section className="py-12 bg-gray-soft">
          <div className="max-w-7xl mx-auto px-4">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Main Content - Left Side (2/3 width) */}
              <div className="lg:col-span-2">
                <div className={`card p-8 ${getCardStyle(ingredient.classification)}`}>
                  
                  {/* Header */}
                  <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
                    <div>
                      <h2 className="font-poppins font-bold text-2xl text-navy mb-2">{ingredient.name}</h2>
                      {ingredient.aliases && ingredient.aliases.length > 0 && (
                        <p className="text-sm text-gray-600">
                          Also known as: {ingredient.aliases.join(', ')}
                        </p>
                      )}
                    </div>
                    {getClassificationBadge(ingredient.classification)}
                  </div>

                  {/* What it is */}
                  {ingredient.what_it_is && (
                    <div className="mb-6">
                      <h3 className="font-poppins font-semibold text-navy mb-3">What is it?</h3>
                      <div className={`p-4 rounded-lg border-2 ${
                        ingredient.classification === 'generally_recognised' 
                          ? 'bg-green-50 border-green-300' 
                          : ingredient.classification === 'worth_knowing'
                          ? 'bg-yellow-50 border-yellow-400'
                          : 'bg-red-50 border-red-400'
                      }`}>
                        <p className={`leading-relaxed font-medium text-base ${
                          ingredient.classification === 'generally_recognised' ? 'text-green-900' : 
                          ingredient.classification === 'worth_knowing' ? 'text-yellow-900' :
                          'text-red-900'
                        }`}>
                          {ingredient.what_it_is}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Health Effects Section */}
                  <div className="mb-6">
                    <h3 className="font-poppins font-semibold text-navy mb-3 flex items-center gap-2">
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
                      </svg>
                      Health & Safety Information
                    </h3>
                    
                    {ingredient.classification === 'generally_recognised' ? (
                      <div className="p-5 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
                        <div className="flex items-start gap-3">
                          <svg className="w-6 h-6 text-green-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                          </svg>
                          <div>
                            <h4 className="font-semibold text-green-900 mb-2">Generally Recognised as Safe</h4>
                            <p className="text-green-800 text-sm leading-relaxed">
                              This ingredient has no known adverse health effects at levels found in foods. It is approved by major regulatory bodies (FSSAI, FDA, EU, WHO) without restrictions.
                            </p>
                          </div>
                        </div>
                      </div>
                    ) : ingredient.classification === 'worth_knowing' ? (
                      <div className="p-5 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
                        <div className="flex items-start gap-3">
                          <svg className="w-6 h-6 text-yellow-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                          </svg>
                          <div>
                            <h4 className="font-semibold text-yellow-900 mb-2">Worth Knowing About</h4>
                            <p className="text-yellow-900 text-sm leading-relaxed mb-3">
                              This ingredient has some concerns or restrictions. While permitted, it may cause issues in sensitive individuals or at high doses.
                            </p>
                            <div className="bg-yellow-100 p-3 rounded border border-yellow-300">
                              <p className="text-yellow-900 text-sm font-medium">
                                <strong>Potential Effects:</strong> {ingredient.one_line_note || 'May cause reactions in sensitive individuals.'}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <div className="p-5 bg-red-50 border-l-4 border-red-600 rounded-r-lg">
                        <div className="flex items-start gap-3">
                          <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                          </svg>
                          <div>
                            <h4 className="font-semibold text-red-900 mb-2">Commonly Questioned</h4>
                            <p className="text-red-900 text-sm leading-relaxed mb-3">
                              This ingredient has significant concerns backed by scientific research. It may be restricted or banned in some countries.
                            </p>
                            <div className="bg-red-100 p-3 rounded border border-red-400">
                              <p className="text-red-900 text-sm font-semibold">
                                <strong>Health Concerns:</strong> {ingredient.one_line_note || 'Linked to adverse health effects in scientific studies.'}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Commonly found in */}
                  {ingredient.commonly_found_in && (
                    <div className="mb-6">
                      <h3 className="font-poppins font-semibold text-navy mb-2">Commonly found in</h3>
                      <div className="flex flex-wrap gap-2">
                        {ingredient.commonly_found_in.split(',').map((item, idx) => (
                          <span key={idx} className="inline-block px-3 py-1 bg-white text-gray-700 rounded-full text-sm border border-gray-300">
                            {item.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Countries Restricted */}
                  {ingredient.countries_restricted && ingredient.countries_restricted.length > 0 && (
                    <div className="mb-6 p-4 bg-red-100 border-2 border-red-400 rounded-lg">
                      <h3 className="font-poppins font-semibold text-red-900 mb-3 flex items-center gap-2">
                        <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        Restricted/Banned in These Countries
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {ingredient.countries_restricted.map((country, idx) => (
                          <span key={idx} className="inline-block px-3 py-2 bg-red-200 text-red-900 rounded-lg text-sm font-semibold">
                            {country}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* FSSAI Position */}
                  {ingredient.fssai_position && (
                    <div className="mb-6 p-4 bg-white rounded-lg border-2 border-amber-300">
                      <h3 className="font-poppins font-semibold text-navy mb-2 flex items-center gap-2">
                        <svg className="w-5 h-5 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                        FSSAI Position (India)
                      </h3>
                      <p className="text-sm text-gray-800 font-medium">{ingredient.fssai_position}</p>
                    </div>
                  )}

                  {/* Disclaimer */}
                  <div className="mt-6 pt-6 border-t border-gray-300">
                    <p className="text-xs text-gray-600 italic">
                      This information is for general awareness based on publicly available regulatory data from FSSAI, WHO, EU, FDA, and peer-reviewed research.
                    </p>
                  </div>
                  
                </div>
              </div>

              {/* Category Information - Right Side (1/3 width) */}
              <div className="lg:col-span-1">
                <div className="sticky top-4">
                  <div className="card p-6 bg-white border-2 border-gray-200">
                    <h3 className="font-poppins font-bold text-lg text-navy mb-4 flex items-center gap-2">
                      <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                      </svg>
                      Our Classification System
                    </h3>
                    
                    <p className="text-sm text-gray-600 mb-4">
                      We classify ingredients into three categories based on scientific research:
                    </p>

                    {/* Generally Recognised */}
                    <div className="mb-4 p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
                      <div className="flex items-start gap-2 mb-2">
                        <svg className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                        </svg>
                        <h4 className="font-semibold text-green-900 text-sm">Generally Recognised</h4>
                      </div>
                      <p className="text-xs text-green-800 leading-relaxed">
                        Safe ingredients with no known adverse effects. Approved by major regulatory bodies.
                      </p>
                    </div>

                    {/* Worth Knowing */}
                    <div className="mb-4 p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
                      <div className="flex items-start gap-2 mb-2">
                        <svg className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                        </svg>
                        <h4 className="font-semibold text-yellow-900 text-sm">Worth Knowing</h4>
                      </div>
                      <p className="text-xs text-yellow-900 leading-relaxed">
                        Ingredients with some concerns. May cause issues in sensitive individuals.
                      </p>
                    </div>

                    {/* Commonly Questioned */}
                    <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-600 rounded-r-lg">
                      <div className="flex items-start gap-2 mb-2">
                        <svg className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                        </svg>
                        <h4 className="font-semibold text-red-900 text-sm">Commonly Questioned</h4>
                      </div>
                      <p className="text-xs text-red-900 leading-relaxed">
                        Ingredients with significant health concerns. May be restricted or banned.
                      </p>
                    </div>

                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <p className="text-xs text-gray-600 italic">
                        Based on data from FSSAI, WHO, EU, FDA, and peer-reviewed research.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
            </div>
          </div>
        </section>
      )}

      {/* Error State */}
      {error && (
        <section className="py-12 bg-gray-soft">
          <div className="max-w-2xl mx-auto px-4">
            <DisclaimerBox variant="warning">
              {error}
            </DisclaimerBox>
          </div>
        </section>
      )}

      {/* Category Information - Always Visible when no search */}
      {!ingredient && !error && (
        <section className="py-12 bg-gray-soft">
          <div className="max-w-4xl mx-auto px-4">
            <div className="card p-8 bg-white border-2 border-gray-200">
              <h3 className="font-poppins font-bold text-2xl text-navy mb-4 text-center flex items-center justify-center gap-2">
                <svg className="w-6 h-6 text-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                Understanding Our Classification System
              </h3>
              
              <p className="text-center text-gray-600 mb-8 max-w-2xl mx-auto">
                We classify ingredients into three categories based on scientific research from FSSAI, WHO, EU, FDA, and peer-reviewed studies:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                {/* Generally Recognised */}
                <div className="p-6 bg-green-50 border-2 border-green-500 rounded-lg">
                  <div className="flex items-center justify-center mb-4">
                    <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
                      <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                  <h4 className="font-poppins font-bold text-lg text-green-900 text-center mb-3">
                    Generally Recognised
                  </h4>
                  <p className="text-sm text-green-800 leading-relaxed text-center">
                    Safe ingredients with no known adverse effects at normal consumption levels. Approved by major regulatory bodies without restrictions.
                  </p>
                  <div className="mt-4 pt-4 border-t border-green-300">
                    <p className="text-xs text-green-700 text-center font-medium">
                      ✓ Extensive safety data<br/>
                      ✓ No significant concerns<br/>
                      ✓ Widely approved globally
                    </p>
                  </div>
                </div>

                {/* Worth Knowing */}
                <div className="p-6 bg-yellow-50 border-2 border-yellow-500 rounded-lg">
                  <div className="flex items-center justify-center mb-4">
                    <div className="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center">
                      <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                  <h4 className="font-poppins font-bold text-lg text-yellow-900 text-center mb-3">
                    Worth Knowing
                  </h4>
                  <p className="text-sm text-yellow-900 leading-relaxed text-center">
                    Ingredients with some concerns or restrictions. May cause issues in sensitive individuals or at high doses. Mixed scientific findings.
                  </p>
                  <div className="mt-4 pt-4 border-t border-yellow-300">
                    <p className="text-xs text-yellow-800 text-center font-medium">
                      ⚠ Some restrictions apply<br/>
                      ⚠ Sensitivity possible<br/>
                      ⚠ Emerging research
                    </p>
                  </div>
                </div>

                {/* Commonly Questioned */}
                <div className="p-6 bg-red-50 border-2 border-red-600 rounded-lg">
                  <div className="flex items-center justify-center mb-4">
                    <div className="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center">
                      <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"/>
                      </svg>
                    </div>
                  </div>
                  <h4 className="font-poppins font-bold text-lg text-red-900 text-center mb-3">
                    Commonly Questioned
                  </h4>
                  <p className="text-sm text-red-900 leading-relaxed text-center">
                    Ingredients with significant health concerns backed by scientific research. May be restricted or banned in some countries.
                  </p>
                  <div className="mt-4 pt-4 border-t border-red-400">
                    <p className="text-xs text-red-800 text-center font-medium">
                      ✗ Significant concerns<br/>
                      ✗ Restricted/banned<br/>
                      ✗ Health risks identified
                    </p>
                  </div>
                </div>
                
              </div>

              <div className="mt-8 p-4 bg-gray-100 rounded-lg">
                <p className="text-sm text-gray-700 text-center">
                  <strong>Our Mission:</strong> To provide transparent, science-based information about food and cosmetic ingredients so you can make informed choices for your health and well-being.
                </p>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Popular Ingredients */}
      <section className="py-12 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="section-heading text-center mb-8">Popular Ingredients to Check</h2>
          <div className="flex flex-wrap gap-3 justify-center">
            {popularIngredients.map((item, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setQuery(item.name)
                  handleSearch(item.name)
                }}
                className="px-6 py-3 bg-primary-light text-primary rounded-full hover:bg-primary hover:text-white transition-colors font-medium"
              >
                {item.name}
              </button>
            ))}
          </div>
        </div>
      </section>
      
    </motion.div>
  )
}

export default CheckIngredient
