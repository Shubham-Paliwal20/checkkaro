import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function SearchBar({ placeholder = "Search any product...", onSearch }) {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      if (onSearch) {
        onSearch(query.trim())
      } else {
        navigate(`/result/${encodeURIComponent(query.trim())}`)
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-center bg-white rounded-full border-2 border-gray-200 focus-within:border-primary shadow-lg overflow-hidden h-[72px] transition-colors">
        <svg className="w-6 h-6 text-gray-400 ml-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={placeholder}
          className="flex-1 px-4 text-lg outline-none font-inter"
        />
        <button
          type="submit"
          className="bg-primary text-white rounded-full mr-2 px-8 py-3 hover:bg-primary-dark transition-colors font-semibold"
        >
          Search
        </button>
      </div>
    </form>
  )
}

export default SearchBar
