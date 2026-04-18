import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const PLACEHOLDER = [
  { id: 'p1', reviewer_name: 'Priya Sharma', review_text: 'Finally I know what\'s actually in my face cream! CheckKaro changed the way I shop. I check every product now before buying.', rating: 5 },
  { id: 'p2', reviewer_name: 'Rahul Mehta', review_text: 'Checked Maggi ingredients and was genuinely shocked. A must-have tool for every Indian household. Highly recommend!', rating: 5 },
  { id: 'p3', reviewer_name: 'Anjali Kapoor', review_text: 'So easy to use and very informative. The ingredient breakdown is clear and jargon-free. Love this app!', rating: 5 },
  { id: 'p4', reviewer_name: 'Vikash Tiwari', review_text: 'Great tool for health-conscious people. Helped me make smarter choices at the supermarket every week.', rating: 5 },
  { id: 'p5', reviewer_name: 'Sneha Reddy', review_text: 'The cosmetic checker is brilliant! Finally understood what\'s inside my shampoo. Everyone should use this.', rating: 5 },
  { id: 'p6', reviewer_name: 'Amit Dubey', review_text: 'Simple, clean, and very useful. I recommend CheckKaro to all my friends. It\'s a real eye-opener.', rating: 5 },
]

const ACCENTS = ['#FF9933', '#138808', '#FF9933']
const LIGHT_BG = ['#fff8f0', '#f0faf0', '#fff8f0']

function Stars({ rating }) {
  return (
    <div style={{ display: 'flex', gap: 3 }}>
      {[1, 2, 3, 4, 5].map(s => (
        <span key={s} style={{ fontSize: 15, color: s <= rating ? '#FF9933' : '#e5e7eb' }}>★</span>
      ))}
    </div>
  )
}

function InteractiveStars({ rating, onRate }) {
  const [hovered, setHovered] = useState(0)
  return (
    <div style={{ display: 'flex', gap: 4 }}>
      {[1, 2, 3, 4, 5].map(s => (
        <span
          key={s}
          onClick={() => onRate(s)}
          onMouseEnter={() => setHovered(s)}
          onMouseLeave={() => setHovered(0)}
          style={{ fontSize: 32, color: s <= (hovered || rating) ? '#FF9933' : '#e5e7eb', cursor: 'pointer', transition: 'color 0.15s' }}
        >★</span>
      ))}
    </div>
  )
}

function ReviewCard({ review, colorIndex }) {
  const accent = ACCENTS[colorIndex % ACCENTS.length]
  const lightBg = LIGHT_BG[colorIndex % LIGHT_BG.length]
  return (
    <div style={{
      flex: '1 1 0', minWidth: 0,
      backgroundColor: '#fff',
      borderRadius: 16,
      overflow: 'hidden',
      boxShadow: '0 2px 20px rgba(0,0,0,0.07)',
      display: 'flex', flexDirection: 'column',
    }}>
      {/* Top accent bar */}
      <div style={{ height: 5, backgroundColor: accent }} />

      <div style={{ padding: '22px 24px 24px', display: 'flex', flexDirection: 'column', gap: 14, flex: 1 }}>
        {/* Quote mark */}
        <span style={{ fontSize: 52, lineHeight: 0.8, color: lightBg, textShadow: `0 0 0 ${accent}`, fontFamily: 'Georgia, serif', display: 'block' }}>
          <span style={{ color: accent, opacity: 0.25 }}>"</span>
        </span>

        {/* Review text */}
        <p style={{ fontSize: 14, color: '#374151', lineHeight: 1.7, margin: 0, flex: 1 }}>
          {review.review_text}
        </p>

        {/* Stars */}
        <Stars rating={review.rating || 5} />

        {/* Reviewer */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, paddingTop: 8, borderTop: '1px solid #f3f4f6' }}>
          <div style={{
            width: 40, height: 40, borderRadius: '50%',
            backgroundColor: lightBg, border: `2px solid ${accent}`,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontWeight: 800, fontSize: 16, color: accent, flexShrink: 0
          }}>
            {review.reviewer_name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 14, color: '#111827' }}>{review.reviewer_name}</div>
            <div style={{ fontSize: 12, color: '#9ca3af' }}>Verified user</div>
          </div>
        </div>
      </div>
    </div>
  )
}

function ReviewFormModal({ onClose, onSubmitted }) {
  const [name, setName] = useState('')
  const [text, setText] = useState('')
  const [rating, setRating] = useState(5)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const submit = async () => {
    if (!name.trim()) { setError('Please enter your name.'); return }
    if (!text.trim() || text.trim().length < 10) { setError('Please write at least 10 characters.'); return }
    setLoading(true); setError('')
    try {
      const { data: { user } } = await supabase.auth.getUser()
      const { error: e } = await supabase.from('reviews').insert({ user_id: user?.id, reviewer_name: name.trim(), review_text: text.trim(), rating })
      if (e) throw e
      onSubmitted(); onClose()
    } catch (e) { setError(e.message || 'Failed to submit.') }
    setLoading(false)
  }

  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 9999, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
      <div style={{ position: 'absolute', inset: 0 }} onClick={onClose} />
      <div style={{ position: 'relative', backgroundColor: '#fff', borderRadius: 18, boxShadow: '0 20px 60px rgba(0,0,0,0.2)', width: '100%', maxWidth: 460, overflow: 'hidden' }}>
        <div style={{ height: 5, background: 'linear-gradient(90deg, #FF9933, #138808)' }} />
        <div style={{ padding: '24px 28px 28px' }}>
          <button onClick={onClose} style={{ position: 'absolute', top: 18, right: 18, background: 'none', border: 'none', fontSize: 20, color: '#9ca3af', cursor: 'pointer' }}>✕</button>
          <h3 style={{ fontSize: 20, fontWeight: 800, color: '#111827', margin: '0 0 4px', fontFamily: 'Poppins, sans-serif' }}>Share your experience</h3>
          <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 22px' }}>Help others make smarter choices.</p>

          <label style={{ fontSize: 12, fontWeight: 700, color: '#374151', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Your Name</label>
          <input type="text" placeholder="e.g. Priya Sharma" value={name} onChange={e => { setName(e.target.value); setError('') }}
            style={{ width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '11px 14px', fontSize: 14, outline: 'none', boxSizing: 'border-box', marginBottom: 16, fontFamily: 'inherit' }} />

          <label style={{ fontSize: 12, fontWeight: 700, color: '#374151', display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Rating</label>
          <div style={{ marginBottom: 16 }}>
            <InteractiveStars rating={rating} onRate={setRating} />
          </div>

          <label style={{ fontSize: 12, fontWeight: 700, color: '#374151', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Your Review</label>
          <textarea placeholder="What do you love about CheckKaro?" value={text} onChange={e => { setText(e.target.value); setError('') }} rows={4}
            style={{ width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '11px 14px', fontSize: 14, outline: 'none', resize: 'vertical', boxSizing: 'border-box', fontFamily: 'inherit' }} />

          {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '6px 0 0' }}>{error}</p>}

          <button onClick={submit} disabled={loading}
            style={{ width: '100%', background: 'linear-gradient(135deg, #FF9933, #e8880a)', color: '#fff', border: 'none', borderRadius: 10, padding: 14, fontSize: 15, fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', marginTop: 18, opacity: loading ? 0.7 : 1, fontFamily: 'inherit' }}>
            {loading ? 'Submitting…' : 'Submit Review'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function ReviewsSection() {
  const { user, openAuthModal } = useAuth()
  const [reviews, setReviews] = useState(PLACEHOLDER)
  const [currentPage, setCurrentPage] = useState(0)
  const [showForm, setShowForm] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const timerRef = useRef(null)

  const fetchReviews = async () => {
    const { data } = await supabase.from('reviews').select('*').eq('is_approved', true).order('created_at', { ascending: false })
    if (data && data.length > 0) setReviews(data)
  }

  useEffect(() => { fetchReviews() }, [])

  const PER_PAGE = 3
  const pages = []
  for (let i = 0; i < reviews.length; i += PER_PAGE) pages.push(reviews.slice(i, i + PER_PAGE))
  const totalPages = pages.length

  const startTimer = () => {
    timerRef.current = setInterval(() => setCurrentPage(p => (p + 1) % totalPages), 4500)
  }
  const stopTimer = () => clearInterval(timerRef.current)

  useEffect(() => { startTimer(); return stopTimer }, [totalPages])

  const goTo = (idx) => { stopTimer(); setCurrentPage(idx); startTimer() }

  return (
    <section style={{ padding: '72px 0', backgroundColor: '#f9fafb', overflow: 'hidden' }}>
      <div style={{ maxWidth: 1140, margin: '0 auto', padding: '0 24px' }}>

        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: 52 }}>
          <p style={{ fontSize: 12, fontWeight: 700, color: '#FF9933', textTransform: 'uppercase', letterSpacing: '0.1em', margin: '0 0 10px' }}>Testimonials</p>
          <h2 style={{ fontSize: 32, fontWeight: 800, color: '#0D1B2A', margin: '0 0 12px', fontFamily: 'Poppins, sans-serif' }}>
            Loved by users <span style={{ color: '#138808' }}>across India</span>
          </h2>
          <p style={{ fontSize: 15, color: '#6b7280', margin: 0 }}>Real reviews from real people making smarter choices every day.</p>
        </div>

        {/* Sliding carousel track */}
        <div
          style={{ overflow: 'hidden', borderRadius: 4 }}
          onMouseEnter={stopTimer}
          onMouseLeave={startTimer}
        >
          <div style={{
            display: 'flex',
            transform: `translateX(-${currentPage * 100}%)`,
            transition: 'transform 0.55s cubic-bezier(0.4, 0, 0.2, 1)',
            willChange: 'transform',
          }}>
            {pages.map((pageReviews, pageIdx) => (
              <div key={pageIdx} style={{ minWidth: '100%', display: 'flex', gap: 20, alignItems: 'stretch' }}>
                {pageReviews.map((review, cardIdx) => (
                  <ReviewCard key={review.id} review={review} colorIndex={cardIdx} />
                ))}
                {/* Fill empty slots so flex layout stays consistent */}
                {pageReviews.length < PER_PAGE && Array.from({ length: PER_PAGE - pageReviews.length }).map((_, i) => (
                  <div key={`empty-${i}`} style={{ flex: '1 1 0' }} />
                ))}
              </div>
            ))}
          </div>
        </div>

        {/* Dots */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginTop: 32 }}>
          {pages.map((_, i) => (
            <button key={i} onClick={() => goTo(i)} style={{
              width: currentPage === i ? 28 : 9,
              height: 9, borderRadius: 999, border: 'none', cursor: 'pointer',
              backgroundColor: currentPage === i ? '#FF9933' : '#d1d5db',
              transition: 'all 0.3s ease', padding: 0,
            }} />
          ))}
        </div>

        {/* CTA */}
        <div style={{ textAlign: 'center', marginTop: 44 }}>
          {submitted ? (
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, backgroundColor: '#f0fdf4', border: '1px solid #86efac', borderRadius: 999, padding: '10px 22px' }}>
              <span style={{ color: '#16a34a', fontSize: 18 }}>✓</span>
              <span style={{ color: '#15803d', fontWeight: 600, fontSize: 14 }}>Thank you! Your review has been submitted.</span>
            </div>
          ) : (
            <>
              <p style={{ fontSize: 14, color: '#6b7280', margin: '0 0 16px' }}>
                {user ? 'Enjoying CheckKaro? Let others know!' : 'Login to share your experience.'}
              </p>
              <button
                onClick={() => { if (!user) { openAuthModal(); return } setShowForm(true) }}
                style={{
                  background: 'linear-gradient(135deg, #FF9933 0%, #e8880a 100%)',
                  color: '#fff', border: 'none', borderRadius: 999,
                  padding: '14px 36px', fontSize: 15, fontWeight: 700,
                  cursor: 'pointer', boxShadow: '0 4px 18px rgba(255,153,51,0.4)',
                  fontFamily: 'inherit', transition: 'transform 0.15s',
                }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.04)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
              >
                ✍&nbsp; Write a Review
              </button>
              {!user && <p style={{ fontSize: 12, color: '#9ca3af', marginTop: 10 }}>Login required to submit a review.</p>}
            </>
          )}
        </div>
      </div>

      {showForm && (
        <ReviewFormModal
          onClose={() => setShowForm(false)}
          onSubmitted={() => { setSubmitted(true); fetchReviews() }}
        />
      )}
    </section>
  )
}
