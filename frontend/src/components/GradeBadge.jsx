import { motion } from 'framer-motion'

const GRADE_META = {
  A: { label: 'Excellent', color: '#16a34a', bg: '#f0fdf4', border: '#86efac', desc: 'Minimal concern ingredients. Largely clean label.' },
  B: { label: 'Good',      color: '#2563eb', bg: '#eff6ff', border: '#93c5fd', desc: 'Mostly safe. Some commonly noted additives.' },
  C: { label: 'Average',   color: '#d97706', bg: '#fffbeb', border: '#fcd34d', desc: 'Mixed formulation. Several commonly questioned ingredients.' },
  D: { label: 'Poor',      color: '#dc2626', bg: '#fef2f2', border: '#fca5a5', desc: 'Proportion of questioned or banned ingredients.' },
}

const SIZES = {
  small:  { circle: 44, font: 20, ring: 3 },
  medium: { circle: 80, font: 36, ring: 4 },
  large:  { circle: 110, font: 50, ring: 5 },
}

function GradeBadge({ grade = 'C', size = 'large', showLabel = true }) {
  const meta = GRADE_META[grade] || GRADE_META['C']
  const { circle, font, ring } = SIZES[size] || SIZES['large']

  return (
    <div className="flex flex-col items-center">
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 260, damping: 20 }}
        style={{
          width: circle,
          height: circle,
          borderRadius: '50%',
          background: meta.bg,
          border: `${ring}px solid ${meta.color}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: `0 0 0 2px ${meta.border}`,
          flexShrink: 0,
        }}
      >
        <span style={{
          fontSize: font,
          fontWeight: 800,
          color: meta.color,
          fontFamily: 'Poppins, sans-serif',
          lineHeight: 1,
          letterSpacing: '-1px',
        }}>
          {grade}
        </span>
      </motion.div>

      {showLabel && (
        <div className="text-center mt-2 max-w-[140px]">
          <p className="text-sm font-bold" style={{ color: meta.color }}>{meta.label}</p>
          <p className="text-xs text-gray-400 mt-0.5 leading-snug">{meta.desc}</p>
        </div>
      )}
    </div>
  )
}

export default GradeBadge
