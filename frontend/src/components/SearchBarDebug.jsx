import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function SearchBarDebug() {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [debugInfo, setDebugInfo] = useState('')

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.length >= 2) {
        try {
          setDebugInfo(`Fetching suggestions for: ${query}`)
          const response = await axios.get(`${API_BASE_URL}/api/product/suggestions`, {
            params: { q: query }
          })
          setDebugInfo(`Got ${response.data.suggestions?.length || 0} suggestions`)
          setSuggestions(response.data.suggestions || [])
          setShowSuggestions(true)
        } catch (error) {
          setDebugInfo(`Error: ${error.message}`)
          setSuggestions([])
        }
      } else {
        setDebugInfo(`Query too short: ${query}`)
        setSuggestions([])
        setShowSuggestions(false)
      }
    }

    const debounceTimer = setTimeout(fetchSuggestions, 200)
    return () => clearTimeout(debounceTimer)
  }, [query])

  return (
    <div className="p-4 border border-red-500 bg-red-50 m-4">
      <h3 className="text-lg font-bold mb-2">DEBUG SEARCH BAR</h3>
      
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Type here to test..."
        className="w-full p-2 border border-gray-300 rounded mb-2"
      />
      
      <div className="mb-2">
        <strong>Debug Info:</strong> {debugInfo}
      </div>
      
      <div className="mb-2">
        <strong>Query:</strong> "{query}" (length: {query.length})
      </div>
      
      <div className="mb-2">
        <strong>Show Suggestions:</strong> {showSuggestions ? 'YES' : 'NO'}
      </div>
      
      <div className="mb-2">
        <strong>Suggestions Count:</strong> {suggestions.length}
      </div>
      
      {suggestions.length > 0 && (
        <div className="bg-white border border-gray-300 rounded p-2">
          <strong>Suggestions:</strong>
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index} className="py-1 border-b">
                {suggestion.name} ({suggestion.brand})
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {/* Test dropdown visibility */}
      <div className="mt-4 relative">
        <div className="bg-blue-100 p-2 rounded">Input area</div>
        {showSuggestions && suggestions.length > 0 && (
          <div className="absolute top-full left-0 right-0 bg-white border border-gray-200 rounded shadow-xl z-50 mt-1">
            <div className="p-2 bg-green-100">
              ✅ DROPDOWN IS VISIBLE! Suggestions: {suggestions.length}
            </div>
            {suggestions.map((suggestion, index) => (
              <div key={index} className="px-4 py-2 border-b hover:bg-gray-50">
                {suggestion.name}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchBarDebug