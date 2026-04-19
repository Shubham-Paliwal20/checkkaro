import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import axios from 'axios'
import ScoreCircle from '../components/ScoreCircle'
import DisclaimerBox from '../components/DisclaimerBox'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function Result() {
  const { productName } = useParams()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [product, setProduct] = useState(null)
  const [showCorrectionForm, setShowCorrectionForm] = useState(false)
  const [correctionText, setCorrectionText] = useState('')
  const [submitting, setSubmitting] = useState(false)

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

  const handleVerifyCorrect = async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/product/verify`, null, {
        params: { product_name: productName, is_correct: true }
      })
      alert('Thank you for verifying!')
    } catch (err) {
      console.error('Error verifying:', err)
    }
  }

  const handleSubmitCorrection = async () => {
    if (!correctionText.trim()) {
      alert('Please enter the ingredients')
      return
    }

    try {
      setSubmitting(true)
      await axios.post(`${API_BASE_URL}/api/product/correct`, null, {
        params: {
          product_name: productName,
          ingredients: correctionText,
          product_id: product?.id
        }
      })
      alert('Thank you! Your correction has been submitted for review.')
      setShowCorrectionForm(false)
      setCorrectionText('')
    } catch (err) {
      alert('Error submitting correction. Please try again.')
      console.error('Error submitting correction:', err)
    } finally {
      setSubmitting(false)
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
  const allIngredients = product.ingredients || []
  const generally_recognised = allIngredients.filter(i => i.classification === 'generally_recognised')
  const worth_knowing = allIngredients.filter(i => i.classification === 'worth_knowing')
  const commonly_questioned = allIngredients.filter(i => i.classification === 'commonly_questioned')

  // Get score color
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    if (score >= 40) return 'text-orange-600'
    return 'text-red-600'
  }

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-50 border-green-200'
    if (score >= 60) return 'bg-yellow-50 border-yellow-200'
    if (score >= 40) return 'bg-orange-50 border-orange-200'
    return 'bg-red-50 border-red-200'
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft py-8"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Product Header Card */}
        <div className="card p-4 sm:p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4 sm:gap-6">
            {/* Product Image */}
            <div className="w-full md:w-48 h-48 bg-gray-100 rounded-xl overflow-hidden flex-shrink-0 mx-auto md:mx-0">
              {product.image_url ? (
                <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  <svg className="w-16 sm:w-20 h-16 sm:h-20" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>

            {/* Product Info */}
            <div className="flex-1 text-center md:text-left">
              {product.brand && (
                <p className="text-sm text-primary uppercase font-semibold mb-1">{product.brand}</p>
              )}
              <h1 className="font-poppins font-bold text-xl sm:text-2xl md:text-3xl text-navy mb-3">{product.name}</h1>
              
              <div className="flex flex-wrap gap-2 mb-4 justify-center md:justify-start">
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
        </div>

        {/* Final Verdict Section */}
        {(product.verdict || product.recommendation) && (
          <div className={`card p-4 sm:p-6 mb-6 border-2 ${getScoreBg(product.awareness_score)}`}>
            <div className="flex flex-col sm:flex-row items-start gap-4">
              <div className="flex-shrink-0 mx-auto sm:mx-0">
                <div className={`w-12 h-12 rounded-full ${getScoreBg(product.awareness_score)} flex items-center justify-center`}>
                  <span className={`text-xl sm:text-2xl font-bold ${getScoreColor(product.awareness_score)}`}>
                    {product.awareness_score}
                  </span>
                </div>
              </div>
              <div className="flex-1 text-center sm:text-left">
                <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-2">Final Verdict</h2>
                {product.verdict && (
                  <p className="text-gray-700 mb-3 font-medium text-sm sm:text-base">{product.verdict}</p>
                )}
                {product.recommendation && (
                  <div className="bg-white rounded-lg p-3 sm:p-4 border border-gray-200">
                    <p className="text-sm font-semibold text-navy mb-1">Recommendation:</p>
                    <p className="text-sm text-gray-700">{product.recommendation}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Complete Ingredients List */}
        <div className="card p-4 sm:p-6 mb-6">
          <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-4">
            Complete Ingredients List ({allIngredients.length} ingredients)
          </h2>
          <div className="bg-gray-50 rounded-lg p-3 sm:p-4">
            <p className="text-sm text-gray-600 leading-relaxed">
              {allIngredients.map((ing, idx) => (
                <span key={idx}>
                  <span className={
                    ing.classification === 'commonly_questioned' ? 'text-red-700 font-semibold' :
                    ing.classification === 'worth_knowing' ? 'text-red-500 font-semibold' :
                    'text-gray-700'
                  }>
                    {ing.name}
                  </span>
                  {ing.aliases && <span className="text-gray-500"> ({ing.aliases})</span>}
                  {idx < allIngredients.length - 1 && ', '}
                </span>
              ))}
            </p>
          </div>
        </div>

        {/* Worth Knowing Ingredients */}
        {worth_knowing.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6 border-l-4 border-red-400">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-red-600 mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-red-400 rounded-full"></span>
              Worth Knowing ({worth_knowing.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Ingredients with some concerns or restrictions. May cause issues in sensitive individuals or at high doses. Mixed scientific findings — fine for most people in small amounts.
            </p>
            <div className="space-y-4">
              {worth_knowing.map((ing, idx) => (
                <div key={idx} className="bg-red-50 rounded-lg p-3 sm:p-4 border border-red-200">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-navy text-sm sm:text-base">
                      {ing.name}
                      {ing.aliases && <span className="text-xs sm:text-sm text-gray-500 font-normal ml-2">({ing.aliases})</span>}
                    </h3>
                  </div>
                  {ing.one_line_note && (
                    <p className="text-sm text-gray-600 mb-2">{ing.one_line_note}</p>
                  )}
                  {ing.detailed_effects && (
                    <div className="mt-3 pt-3 border-t border-red-200">
                      <p className="text-sm font-semibold text-navy mb-1">Detailed Information:</p>
                      <p className="text-sm text-gray-700 leading-relaxed">{ing.detailed_effects}</p>
                    </div>
                  )}
                  {ing.regulatory_note && (
                    <div className="mt-2 text-xs text-gray-600 italic">
                      Regulatory: {ing.regulatory_note}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Commonly Questioned Ingredients */}
        {commonly_questioned.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6 border-l-4 border-red-600">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-red-700 mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-red-600 rounded-full"></span>
              Commonly Questioned ({commonly_questioned.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Ingredients flagged, restricted, or banned in one or more countries. Associated with potential health concerns — worth avoiding or limiting where possible.
            </p>
            <div className="space-y-4">
              {commonly_questioned.map((ing, idx) => (
                <div key={idx} className="bg-red-100 rounded-lg p-3 sm:p-4 border border-red-300">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-navy text-sm sm:text-base">
                      {ing.name}
                      {ing.aliases && <span className="text-xs sm:text-sm text-gray-500 font-normal ml-2">({ing.aliases})</span>}
                    </h3>
                  </div>
                  {ing.one_line_note && (
                    <p className="text-sm text-gray-600 mb-2">{ing.one_line_note}</p>
                  )}
                  {ing.detailed_effects && (
                    <div className="mt-3 pt-3 border-t border-red-300">
                      <p className="text-sm font-semibold text-navy mb-1">Detailed Information:</p>
                      <p className="text-sm text-gray-700 leading-relaxed">{ing.detailed_effects}</p>
                    </div>
                  )}
                  {ing.regulatory_note && (
                    <div className="mt-2 text-xs text-gray-600 italic">
                      Regulatory: {ing.regulatory_note}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Generally Recognised Ingredients */}
        {generally_recognised.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              Generally Recognised ({generally_recognised.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Safe ingredients with no known adverse effects at normal consumption levels. Approved by major regulatory bodies worldwide without restrictions.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {generally_recognised.map((ing, idx) => (
                <div key={idx} className="bg-green-50 rounded-lg p-3 border border-green-200">
                  <h3 className="font-semibold text-navy text-sm">
                    {ing.name}
                    {ing.aliases && <span className="text-xs text-gray-500 font-normal ml-2">({ing.aliases})</span>}
                  </h3>
                  {ing.one_line_note && (
                    <p className="text-xs text-gray-600 mt-1">{ing.one_line_note}</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary */}
        {product.summary && (
          <div className="card p-6 mb-6">
            <h3 className="font-poppins font-semibold text-navy mb-3">Summary</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{product.summary}</p>
          </div>
        )}

        {/* FSSAI Note */}
        {product.fssai_note && (
          <div className="card p-6 mb-6 bg-amber-50 border border-amber-200">
            <h3 className="font-poppins font-semibold text-navy mb-2">FSSAI Position</h3>
            <p className="text-sm text-gray-700">{product.fssai_note}</p>
          </div>
        )}

        {/* Help Improve This Section - Show when data is AI estimated or low confidence */}
        {(product.data_source === 'ai_estimated' || product.confidence === 'low') && (
          <div className="card p-4 sm:p-6 mb-6 bg-yellow-50 border-2 border-yellow-400">
            <div className="flex flex-col sm:flex-row items-start gap-4">
              <div className="flex-shrink-0 mx-auto sm:mx-0">
                <svg className="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="flex-1 text-center sm:text-left">
                <h3 className="font-poppins font-bold text-base sm:text-lg text-yellow-900 mb-2">
                  Help Improve This Data
                </h3>
                <p className="text-sm text-yellow-800 mb-4">
                  These ingredients are AI estimated and may be incomplete. Do you have this product with you?
                </p>
                
                {!showCorrectionForm ? (
                  <div className="flex flex-col sm:flex-row flex-wrap gap-3 justify-center sm:justify-start">
                    <button
                      onClick={handleVerifyCorrect}
                      className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium text-sm transition-colors"
                    >
                      ✓ Ingredients look correct
                    </button>
                    <button
                      onClick={() => setShowCorrectionForm(true)}
                      className="px-4 py-2 bg-primary hover:bg-primary-dark text-white rounded-lg font-medium text-sm transition-colors"
                    >
                      Submit correct ingredients
                    </button>
                  </div>
                ) : (
                  <div className="bg-white rounded-lg p-3 sm:p-4 border border-yellow-300">
                    <label className="block text-sm font-semibold text-navy mb-2">
                      Paste the complete ingredients list from the product label:
                    </label>
                    <textarea
                      value={correctionText}
                      onChange={(e) => setCorrectionText(e.target.value)}
                      placeholder="Example: Water, Sugar, Wheat Flour, Palm Oil, Salt, Citric Acid (E330), Preservative (E211)..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
                      rows="4"
                    />
                    <div className="flex flex-col sm:flex-row gap-3 mt-3">
                      <button
                        onClick={handleSubmitCorrection}
                        disabled={submitting}
                        className="px-4 py-2 bg-primary hover:bg-primary-dark text-white rounded-lg font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {submitting ? 'Submitting...' : 'Submit Correction'}
                      </button>
                      <button
                        onClick={() => {
                          setShowCorrectionForm(false)
                          setCorrectionText('')
                        }}
                        className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium text-sm transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="mb-6">
          <DisclaimerBox variant="info">
            This Awareness Score reflects how commonly ingredients in this product are discussed by health researchers and flagged by international regulatory bodies. It is not a safety rating, health claim, or medical assessment. CheckKaro does not certify any product as safe or unsafe. Always read the actual product label and consult a qualified professional for personal health decisions.
          </DisclaimerBox>
        </div>
      </div>
    </motion.div>
  )
}

export default Result
