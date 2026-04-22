import { motion } from 'framer-motion'

function ScoreCircle({ score, size = 'large', showLabel = true }) {
  const sizes = {
    small: { width: 60, strokeWidth: 4, fontSize: 'text-lg' },
    medium: { width: 100, strokeWidth: 6, fontSize: 'text-2xl' },
    large: { width: 140, strokeWidth: 8, fontSize: 'text-4xl' }
  }

  const config = sizes[size]
  const radius = (config.width - config.strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const offset = circumference - (score / 100) * circumference

  // Color based on score
  const getColor = () => {
    if (score >= 70) return '#2ECC71' // green
    if (score >= 40) return '#F39C12' // amber
    return '#E74C3C' // red
  }

  return (
    <div className="flex flex-col items-center">
      <svg width={config.width} height={config.width} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={config.width / 2}
          cy={config.width / 2}
          r={radius}
          stroke="#E5E7EB"
          strokeWidth={config.strokeWidth}
          fill="none"
        />
        {/* Progress circle */}
        <motion.circle
          cx={config.width / 2}
          cy={config.width / 2}
          r={radius}
          stroke={getColor()}
          strokeWidth={config.strokeWidth}
          fill="none"
          strokeLinecap="round"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: 'easeOut' }}
        />
        {/* Score text */}
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dy=".3em"
          className={`font-poppins font-bold ${config.fontSize}`}
          fill={getColor()}
          transform={`rotate(90 ${config.width / 2} ${config.width / 2})`}
        >
          {score}
        </text>
      </svg>
      {showLabel && (
        <div className="text-center mt-2 max-w-[160px]">
          <p className="text-sm font-semibold text-gray-700">Composition Score</p>
          <p className="text-xs text-gray-400 mt-1 leading-snug">
            Based on ingredient composition and commonly known information to help you make informed choices.
          </p>
        </div>
      )}
    </div>
  )
}

export default ScoreCircle
