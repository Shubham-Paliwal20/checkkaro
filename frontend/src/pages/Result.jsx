import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import axios from 'axios'
import ScoreCircle from '../components/ScoreCircle'
import IngredientColumns from '../components/IngredientColumns'
import DisclaimerBox from '../components/DisclaimerBox'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function Result() {
  const { productName } = useParams()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [product, setProduct] = useState(null)

  useEffect(() => {
    fetchProduct()
  }, [productName])

  const fetchProduct = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get(`${API_BASE_URL}/api/product/search`, {
        params: { name: productName }
      })
      setProduct(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch product information')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing {productName}...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md text-center">
          <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          <h2 className="text-2xl font-poppins font-bold text-navy mb-2">Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={() => window.history.back()} className="btn-primary">
            Go Back
          </button>
        </div>
      </div>
    )
  }

  if (!product) return null

  // Categorize ingredients
  const generally_recognised = product.ingredients.filter(i => i.classification === 'generally_recognised')
  const worth_knowing = product.ingredients.filter(i => i.classification === 'worth_knowing')
  const commonly_questioned = product.ingredients.filter(i => i.classification === 'commonly_questioned')

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft py-8"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Product Header Card */}
        <div className="card p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-6">
            {/* Product Image */}
            <div className="w-full md:w-48 h-48 bg-gray-100 rounded-xl overflow-hidden flex-shrink-0">
              {product.image_url ? (
                <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  <svg className="w-20 h-20" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="flex-1">
              {product.brand && (
                <p className="text-sm text-primary uppercase font-semibold mb-1">{product.brand}</p>
              )}
              <h1 className="font-poppins font-bold text-2xl md:text-3xl text-navy mb-3">{product.name}</h1>
              
              <div className="flex flex-wrap gap-2 mb-4">
                {product.category && (
                  <span className="inline-block px-3 py-1 bg-primary-light text-primary rounded-full text-sm">
                    {product.category}
                  </span>
                )}
                <span className="inline-block px-3 py-1 bg-amber-50 text-amber-700 rounded-full text-sm">
                  FSSAI Regulated
                </span>
              </div>
            </div>

            {/* Awareness Score */}
            <div className="flex justify-center md:justify-end">
              <ScoreCircle score={product.awareness_score} size="large" showLabel={true} />
            </div>
          </div>

          {/* Summary */}
          {product.summary && (
            <div className="mt-6 pt-6 border-t border-gray-100">
              <p className="text-sm text-gray-600 leading-relaxed">{product.summary}</p>
            </div>
          )}
        </div>

        {/* Awareness Disclaimer */}
        <div className="mb-6">
          <DisclaimerBox variant="info">
            This Awareness Score reflects how commonly ingredients in this product are discussed by health researchers and flagged by international regulatory bodies. It is not a safety rating, health claim, or medical assessment. CheckKaro does not certify any product as safe or unsafe. Always read the actual product label and consult a qualified professional for personal health decisions.
          </DisclaimerBox>
        </div>

        {/* Ingredient Columns */}
        <div className="mb-6">
          <h2 className="section-heading mb-4">Ingredient Breakdown</h2>
          <IngredientColumns
            generally_recognised={generally_recognised}
            worth_knowing={worth_knowing}
            commonly_questioned={commonly_questioned}
          />
        </div>

        {/* Awareness Message */}
        <div className="mb-6">
          <div className="bg-primary-light border-2 border-primary rounded-xl p-5">
            <p className="text-sm text-gray-700 leading-relaxed">
              CheckKaro provides ingredient information for general awareness only. Our classifications are based on publicly available international regulatory data. We do not make health claims. Individual responses to ingredients vary. This is not medical advice.
            </p>
          </div>
        </div>

        {/* FSSAI Note */}
        {product.fssai_note && (
          <div className="mb-6">
            <div className="card p-4">
              <h3 className="font-poppins font-semibold text-navy mb-2">FSSAI Position</h3>
              <p className="text-sm text-gray-600">{product.fssai_note}</p>
            </div>
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default Result
