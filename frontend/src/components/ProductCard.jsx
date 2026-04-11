import { useNavigate } from 'react-router-dom'
import ScoreCircle from './ScoreCircle'

function ProductCard({ product }) {
  const navigate = useNavigate()

  return (
    <div className="card p-4 hover:shadow-md transition-shadow cursor-pointer" onClick={() => navigate(`/result/${encodeURIComponent(product.name)}`)}>
      <div className="aspect-square bg-gray-100 rounded-xl mb-3 overflow-hidden">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>
      <h3 className="font-poppins font-semibold text-navy mb-1">{product.name}</h3>
      {product.brand && (
        <p className="text-xs text-primary uppercase mb-2">{product.brand}</p>
      )}
      {product.category && (
        <span className="inline-block text-xs bg-primary-light text-primary px-2 py-1 rounded-full mb-3">
          {product.category}
        </span>
      )}
      <div className="flex items-center justify-between mt-3">
        <ScoreCircle score={product.awareness_score} size="small" showLabel={false} />
        <button className="btn-outline text-sm px-4 py-1">
          Check
        </button>
      </div>
    </div>
  )
}

export default ProductCard
