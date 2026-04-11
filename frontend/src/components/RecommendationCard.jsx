import ScoreCircle from './ScoreCircle'

function RecommendationCard({ recommendation }) {
  return (
    <div className="card p-4 hover:shadow-md transition-shadow">
      {recommendation.is_sponsored && (
        <span className="inline-block text-xs bg-amber-100 text-amber-700 px-2 py-1 rounded-full mb-2">
          Sponsored
        </span>
      )}
      <div className="aspect-square bg-gray-100 rounded-xl mb-3 overflow-hidden">
        {recommendation.recommended_image ? (
          <img src={recommendation.recommended_image} alt={recommendation.recommended_name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400">
            <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>
      <h3 className="font-poppins font-semibold text-navy mb-1">{recommendation.recommended_name}</h3>
      {recommendation.recommended_brand && (
        <p className="text-xs text-primary uppercase mb-2">{recommendation.recommended_brand}</p>
      )}
      <div className="flex items-center justify-between mt-3">
        <ScoreCircle score={85} size="small" showLabel={false} />
        {recommendation.buy_link ? (
          <a 
            href={recommendation.buy_link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="btn-outline text-sm px-4 py-1"
          >
            View
          </a>
        ) : (
          <button className="btn-outline text-sm px-4 py-1">
            View
          </button>
        )}
      </div>
    </div>
  )
}

export default RecommendationCard
