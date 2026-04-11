import { useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import DisclaimerBox from '../components/DisclaimerBox'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function CheckIngredient() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [ingredient, setIngredient] = useState(null)
  const [error, setError] = useState(null)

  const popularIngredients = [
    'TBHQ', 'Tartrazine', 'MSG', 'Sodium Benzoate',
    'Aspartame', 'BHA', 'Carrageenan', 'Sunset Yellow'
  ]

  const handleSearch = async (searchQuery) => {
    const queryToSearch = searchQuery || query
    if (!queryToSearch.trim()) return

    try {
      setLoading(true)
      setError(null)
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

  const getClassificationBadge = (classification) => {
    const badges = {
      generally_recognised: { bg: 'bg-green-100', text: 'text-green-700', label: 'Widely Accepted' },
      worth_knowing: { bg: 'bg-amber-100', text: 'text-amber-700', label: 'Discussed by Researchers' },
      commonly_questioned: { bg: 'bg-red-100', text: 'text-red-700', label: 'Restricted in Some Countries' }
    }
    const badge = badges[classification] || badges.worth_knowing
    return (
      <span className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${badge.bg} ${badge.text}`}>
        {badge.label}
      </span>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {/* Hero Section */}
      <section className="bg-navy text-white py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <div className="inline-block mb-4">
            <span className="inline-block px-4 py-2 rounded-full border border-primary text-primary text-sm font-medium">
              Ingredient Checker
            </span>
          </div>
          
          <h1 className="font-poppins font-bold text-4xl md:text-5xl mb-4">
            What does this ingredient do?
          </h1>
          
          <p className="text-gray-300 text-lg mb-8">
            Type any ingredient name or E-number from a product label
          </p>

          {/* Search Bar */}
          <form onSubmit={handleSubmit} className="max-w-xl mx-auto">
            <div className="flex items-center bg-white rounded-full overflow-hidden h-[60px]">
              <svg className="w-6 h-6 text-gray-400 ml-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g. TBHQ, E102, Tartrazine, Sodium Benzoate..."
                className="flex-1 px-4 text-gray-900 outline-none"
              />
              <button
                type="submit"
                disabled={loading}
                className="bg-primary text-white rounded-full mr-2 px-6 py-2 hover:bg-primary-dark transition-colors font-semibold disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </form>
        </div>
      </section>

      {/* Results Section */}
      {ingredient && (
        <section className="py-12 bg-gray-soft">
          <div className="max-w-2xl mx-auto px-4">
            <div className="card p-8">
              {/* Header */}
              <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
                <div>
                  <h2 className="font-poppins font-bold text-2xl text-navy mb-2">{ingredient.name}</h2>
                  {ingredient.aliases && ingredient.aliases.length > 0 && (
                    <p className="text-sm text-gray-500">
                      Also known as: {ingredient.aliases.join(', ')}
                    </p>
                  )}
                </div>
                {getClassificationBadge(ingredient.classification)}
              </div>

              {/* What it is */}
              {ingredient.what_it_is && (
                <div className="mb-6">
                  <h3 className="font-poppins font-semibold text-navy mb-2">What is it?</h3>
                  <p className="text-gray-700 leading-relaxed">{ingredient.what_it_is}</p>
                </div>
              )}

              {/* One line note */}
              {ingredient.one_line_note && (
                <div className="mb-6 p-4 bg-primary-light rounded-lg">
                  <p className="text-sm text-gray-700 font-medium">{ingredient.one_line_note}</p>
                </div>
              )}

              {/* Commonly found in */}
              {ingredient.commonly_found_in && (
                <div className="mb-6">
                  <h3 className="font-poppins font-semibold text-navy mb-2">Commonly found in</h3>
                  <div className="flex flex-wrap gap-2">
                    {ingredient.commonly_found_in.split(',').map((item, idx) => (
                      <span key={idx} className="inline-block px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                        {item.trim()}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* FSSAI Position */}
              {ingredient.fssai_position && (
                <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h3 className="font-poppins font-semibold text-navy mb-2">FSSAI Position</h3>
                  <p className="text-sm text-gray-700">{ingredient.fssai_position}</p>
                </div>
              )}

              {/* Countries Restricted */}
              {ingredient.countries_restricted && ingredient.countries_restricted.length > 0 && (
                <div className="mb-6">
                  <h3 className="font-poppins font-semibold text-navy mb-2">Restricted in</h3>
                  <div className="flex flex-wrap gap-2">
                    {ingredient.countries_restricted.map((country, idx) => (
                      <span key={idx} className="inline-block px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm">
                        {country}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Disclaimer */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  This information is for general awareness based on public regulatory data. Not medical advice.
                </p>
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

      {/* Popular Ingredients */}
      <section className="py-12 bg-white">
        <div className="max-w-4xl mx-auto px-4">
          <h2 className="section-heading text-center mb-8">Popular Ingredients to Check</h2>
          <div className="flex flex-wrap gap-3 justify-center">
            {popularIngredients.map((item, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setQuery(item)
                  handleSearch(item)
                }}
                className="px-6 py-3 bg-primary-light text-primary rounded-full hover:bg-primary hover:text-white transition-colors font-medium"
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      </section>
    </motion.div>
  )
}

export default CheckIngredient
