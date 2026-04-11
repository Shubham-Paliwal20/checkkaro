import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import ProductCard from '../components/ProductCard'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function Products() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const limit = 12

  const categories = [
    'All', 'Food', 'Beverages', 'Snacks', 'Biscuits',
    'Cosmetics', 'Personal Care', 'Baby'
  ]

  useEffect(() => {
    fetchProducts()
  }, [category, page])

  const fetchProducts = async () => {
    try {
      setLoading(true)
      const params = { page, limit }
      if (category && category !== 'All') {
        params.category = category
      }
      
      const response = await axios.get(`${API_BASE_URL}/api/products/browse`, { params })
      setProducts(response.data.products)
      setTotal(response.data.total)
    } catch (err) {
      console.error('Failed to fetch products:', err)
    } finally {
      setLoading(false)
    }
  }

  const totalPages = Math.ceil(total / limit)

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft py-12"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="section-heading mb-2">Product Directory</h1>
          <p className="text-gray-600">Browse products already in our database</p>
        </div>

        {/* Category Filter */}
        <div className="mb-8 overflow-x-auto">
          <div className="flex gap-2 justify-center min-w-max px-4">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => {
                  setCategory(cat === 'All' ? '' : cat)
                  setPage(1)
                }}
                className={`px-6 py-2 rounded-full font-medium transition-colors whitespace-nowrap ${
                  (cat === 'All' && !category) || cat === category
                    ? 'bg-primary text-white'
                    : 'bg-white text-gray-700 hover:bg-primary-light'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          </div>
        )}

        {/* Products Grid */}
        {!loading && products.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && products.length === 0 && (
          <div className="text-center py-12">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <h3 className="font-poppins font-semibold text-xl text-navy mb-2">No products yet</h3>
            <p className="text-gray-600">Be the first to search!</p>
          </div>
        )}

        {/* Pagination */}
        {!loading && totalPages > 1 && (
          <div className="flex justify-center items-center gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="px-4 py-2 rounded-lg bg-white text-gray-700 hover:bg-primary-light disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <div className="flex gap-2">
              {[...Array(Math.min(5, totalPages))].map((_, idx) => {
                const pageNum = idx + 1
                return (
                  <button
                    key={pageNum}
                    onClick={() => setPage(pageNum)}
                    className={`w-10 h-10 rounded-lg font-medium ${
                      page === pageNum
                        ? 'bg-primary text-white'
                        : 'bg-white text-gray-700 hover:bg-primary-light'
                    }`}
                  >
                    {pageNum}
                  </button>
                )
              })}
            </div>
            
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="px-4 py-2 rounded-lg bg-white text-gray-700 hover:bg-primary-light disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default Products
