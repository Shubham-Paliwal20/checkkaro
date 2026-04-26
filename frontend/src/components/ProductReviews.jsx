import { useState, useEffect, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const BRAND_BLUE = '#1B3F8A'
const ORANGE     = '#FF9933'

// Strip "sample-" prefix so reviews match regardless of which backend path served the product
function normId(id) { return id ? String(id).replace(/^sample-/, '') : '' }
const AVATAR_COLORS = ['#1B3F8A', '#0d7c66', '#9333ea', '#c2410c', '#0369a1', '#b45309']

function getAvatarColor(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
  return AVATAR_COLORS[Math.abs(h) % AVATAR_COLORS.length]
}

function Avatar({ name, size = 42 }) {
  const parts = (name || 'U').trim().split(/\s+/)
  const init  = parts.length >= 2
    ? parts[0][0].toUpperCase() + parts[parts.length - 1][0].toUpperCase()
    : parts[0][0].toUpperCase()
  return (
    <div style={{
      width: size, height: size, borderRadius: '50%', flexShrink: 0,
      background: getAvatarColor(name), color: '#fff',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontWeight: 700, fontSize: size * 0.38, fontFamily: 'Poppins,sans-serif',
    }}>{init}</div>
  )
}

function StarBadge({ rating }) {
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 3,
      background: '#15803d', color: '#fff',
      borderRadius: 6, padding: '3px 9px', fontSize: 13, fontWeight: 700,
    }}>
      {rating} <span style={{ fontSize: 11 }}>★</span>
    </span>
  )
}

function StarsRow({ rating, size = 16 }) {
  return (
    <span style={{ display: 'inline-flex', gap: 2 }}>
      {[1,2,3,4,5].map(s => (
        <span key={s} style={{ fontSize: size, color: s <= Math.round(rating) ? ORANGE : '#d1d5db', lineHeight: 1 }}>★</span>
      ))}
    </span>
  )
}

function ClickStars({ value, onChange }) {
  const [hover, setHover] = useState(0)
  return (
    <span style={{ display: 'inline-flex', gap: 4 }}>
      {[1,2,3,4,5].map(s => (
        <span key={s}
          onClick={() => onChange(s)}
          onMouseEnter={() => setHover(s)}
          onMouseLeave={() => setHover(0)}
          style={{ fontSize: 36, lineHeight: 1, cursor: 'pointer',
            color: s <= (hover || value) ? ORANGE : '#d1d5db', transition: 'color 0.1s' }}
        >★</span>
      ))}
    </span>
  )
}

function RatingBar({ star, count, total }) {
  const pct = total > 0 ? Math.round(count / total * 100) : 0
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 13 }}>
      <span style={{ color: '#374151', width: 10, textAlign: 'right', fontWeight: 600 }}>{star}</span>
      <span style={{ color: ORANGE, fontSize: 11 }}>★</span>
      <div style={{ flex: 1, height: 7, borderRadius: 99, background: '#eef0f4', overflow: 'hidden' }}>
        <div style={{
          width: `${pct}%`, height: '100%', borderRadius: 99,
          background: `linear-gradient(90deg, ${ORANGE}, #fbbf24)`,
          transition: 'width 0.7s ease',
        }} />
      </div>
      <span style={{ color: '#9ca3af', width: 22, textAlign: 'right', fontSize: 11 }}>{count}</span>
    </div>
  )
}

const RATING_LABEL = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent']

function formatDate(iso) {
  const d  = new Date(iso)
  const dd = String(d.getDate()).padStart(2, '0')
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  return `${dd}/${mm}/${d.getFullYear()}`
}

// ── Single review card for carousel ──
function ReviewCard({ review, isOwn }) {
  return (
    <div style={{
      flexShrink: 0,
      width: 'min(82vw, 300px)',
      background: isOwn ? '#f0f5ff' : '#fff',
      border: `1.5px solid ${isOwn ? '#c7d7f5' : '#e5e7eb'}`,
      borderRadius: 16,
      padding: '18px 16px',
      display: 'flex',
      flexDirection: 'column',
      gap: 12,
      scrollSnapAlign: 'start',
    }}>
      {/* Top row */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
        <Avatar name={review.reviewer_name} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: '#111827', lineHeight: 1.3 }}>
            {review.reviewer_name}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 3 }}>
            <svg width="12" height="12" viewBox="0 0 20 20" fill="#16a34a">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span style={{ fontSize: 11, color: '#16a34a', fontWeight: 500 }}>Verified User</span>
            {isOwn && (
              <span style={{
                fontSize: 10, fontWeight: 700, color: BRAND_BLUE,
                background: '#dbeafe', padding: '1px 7px', borderRadius: 99,
                marginLeft: 4,
              }}>You</span>
            )}
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4 }}>
          <StarBadge rating={review.rating} />
          <span style={{ fontSize: 11, color: '#9ca3af' }}>{formatDate(review.created_at)}</span>
        </div>
      </div>

      {/* Review text */}
      <p style={{
        margin: 0, fontSize: 13, color: review.review_text ? '#374151' : '#9ca3af',
        lineHeight: 1.65, fontStyle: review.review_text ? 'normal' : 'italic',
        flexGrow: 1,
      }}>
        {review.review_text ? `"${review.review_text}"` : 'Rated without a written review.'}
      </p>
    </div>
  )
}

export default function ProductReviews({ productId, productName }) {
  const { user, openAuthModal } = useAuth()
  const [reviews,    setReviews]    = useState([])
  const [loading,    setLoading]    = useState(true)
  const [myReview,   setMyReview]   = useState(null)
  const [editing,    setEditing]    = useState(false)

  const [name,       setName]       = useState('')
  const [rating,     setRating]     = useState(0)
  const [text,       setText]       = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError,  setFormError]  = useState('')
  const [success,    setSuccess]    = useState(false)

  const scrollRef = useRef(null)

  const fetchReviews = async () => {
    setLoading(true)
    const pid = normId(productId)
    const { data, error } = await supabase
      .from('product_reviews')
      .select('*')
      .eq('product_id', pid)
      .order('created_at', { ascending: false })
    if (error) console.error('[Reviews] fetch error:', error)
    const list = data || []
    setReviews(list)
    setLoading(false)
  }

  // Fetch only when productId changes — NOT when user changes (avoids double-fetch)
  useEffect(() => { if (productId) fetchReviews() }, [productId])

  // Derive myReview from cached list whenever user or list updates (no extra network call)
  useEffect(() => {
    setMyReview(user ? (reviews.find(r => r.user_id === user.id) || null) : null)
  }, [user, reviews])

  useEffect(() => {
    if (myReview && editing) {
      setName(myReview.reviewer_name)
      setRating(myReview.rating)
      setText(myReview.review_text || '')
    } else if (!myReview && user) {
      const meta = user.user_metadata
      const defaultName = meta?.full_name || meta?.name
        || (user.email ? user.email.split('@')[0] : '')
        || user.phone || ''
      setName(defaultName)
      setRating(0)
      setText('')
    }
  }, [myReview, user, editing])

  const total = reviews.length
  const avg   = total > 0 ? reviews.reduce((s, r) => s + r.rating, 0) / total : 0

  const handleSubmit = async () => {
    setFormError('')
    if (!rating)        { setFormError('⭐ Please select a star rating first.'); return }
    if (!name.trim())   { setFormError('Please enter your display name.'); return }
    if (text.trim().length > 0 && text.trim().length < 5) { setFormError('Review text must be at least 5 characters.'); return }
    if (!productId)     { setFormError('Product ID missing — please reload the page.'); return }

    setSubmitting(true)
    const payload = {
      product_id:    normId(productId),
      product_name:  productName,
      user_id:       user.id,
      reviewer_name: name.trim(),
      rating,
      review_text:   text.trim(),
    }
    console.log('[Review] submit:', payload)

    let err
    if (myReview && editing) {
      const { error } = await supabase
        .from('product_reviews')
        .update({ reviewer_name: payload.reviewer_name, rating: payload.rating, review_text: payload.review_text })
        .eq('id', myReview.id).eq('user_id', user.id)
      err = error
    } else {
      const { error } = await supabase
        .from('product_reviews')
        .upsert(payload, { onConflict: 'product_id,user_id' })
      err = error
    }

    if (err) {
      console.error('[Review] error:', err)
      let msg = err.message || 'Something went wrong. Please try again.'
      if (err.code === '42P01') msg = 'Reviews table not found — please contact support.'
      if (err.code === '42501' || err.message?.includes('policy')) msg = 'Session expired. Please log out and log in again.'
      setFormError(msg)
    } else {
      setSuccess(true)
      setEditing(false)
      await fetchReviews()
      // Scroll carousel to start so user sees their new review
      setTimeout(() => scrollRef.current?.scrollTo({ left: 0, behavior: 'smooth' }), 300)
    }
    setSubmitting(false)
  }

  // All reviews for carousel: own first, then others newest-first
  const carouselReviews = user && myReview
    ? [myReview, ...reviews.filter(r => r.user_id !== user.id)]
    : reviews

  return (
    <div className="card p-4 sm:p-6 mb-6">

      {/* ── Section header ── */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontFamily: 'Poppins,sans-serif', fontWeight: 800, fontSize: 20, color: BRAND_BLUE, margin: 0 }}>
          Ratings &amp; Reviews by Users
        </h2>
        <div style={{ height: 3, width: 56, borderRadius: 99, background: ORANGE, marginTop: 8 }} />
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '28px 0', color: '#9ca3af', fontSize: 14 }}>Loading reviews…</div>
      ) : (
        <>
          {/* ── Rating summary strip ── */}
          {total > 0 && (
            <div style={{
              display: 'flex', gap: 24, flexWrap: 'wrap',
              padding: '16px 20px', background: '#f8faff',
              borderRadius: 14, border: '1px solid #e4ecfb', marginBottom: 20,
            }}>
              <div style={{ textAlign: 'center', minWidth: 72 }}>
                <div style={{ fontSize: 46, fontWeight: 900, lineHeight: 1, color: BRAND_BLUE, fontFamily: 'Poppins,sans-serif' }}>
                  {avg.toFixed(1)}
                </div>
                <div style={{ marginTop: 5 }}><StarsRow rating={avg} size={16} /></div>
                <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 4 }}>
                  {total} {total === 1 ? 'review' : 'reviews'}
                </div>
              </div>
              <div style={{ flex: 1, minWidth: 140, display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center' }}>
                {[5,4,3,2,1].map(s => (
                  <RatingBar key={s} star={s} count={reviews.filter(r => r.rating === s).length} total={total} />
                ))}
              </div>
            </div>
          )}

          {/* ── Reviews carousel ── */}
          {carouselReviews.length > 0 && (
            <div style={{ marginBottom: 20 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: '#6b7280', textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  {total} {total === 1 ? 'Review' : 'Reviews'}
                </span>
                {carouselReviews.length > 1 && (
                  <div style={{ display: 'flex', gap: 6 }}>
                    <button
                      onClick={() => scrollRef.current?.scrollBy({ left: -320, behavior: 'smooth' })}
                      style={{ width: 30, height: 30, borderRadius: '50%', border: '1.5px solid #e5e7eb', background: '#fff', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                    >‹</button>
                    <button
                      onClick={() => scrollRef.current?.scrollBy({ left: 320, behavior: 'smooth' })}
                      style={{ width: 30, height: 30, borderRadius: '50%', border: '1.5px solid #e5e7eb', background: '#fff', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                    >›</button>
                  </div>
                )}
              </div>
              <div
                ref={scrollRef}
                className="review-carousel"
                style={{
                  display: 'flex', gap: 12,
                  overflowX: 'auto',
                  scrollSnapType: 'x mandatory',
                  scrollBehavior: 'smooth',
                  WebkitOverflowScrolling: 'touch',
                  paddingBottom: 4,
                }}
              >
                {carouselReviews.map(review => (
                  <ReviewCard key={review.id} review={review} isOwn={user && review.user_id === user.id} />
                ))}
              </div>
              {/* Edit button below carousel for own review */}
              {user && myReview && !editing && (
                <div style={{ marginTop: 10 }}>
                  <button
                    onClick={() => { setEditing(true); setSuccess(false) }}
                    style={{
                      fontSize: 12, color: BRAND_BLUE, background: 'none',
                      border: `1.5px solid ${BRAND_BLUE}`, borderRadius: 8,
                      padding: '5px 14px', cursor: 'pointer', fontWeight: 600,
                    }}
                  >
                    Edit My Review
                  </button>
                </div>
              )}
            </div>
          )}

          {/* ── Auth gate ── */}
          {!user && (
            <div style={{
              border: '1.5px dashed #d1d5db', borderRadius: 14,
              padding: '20px', textAlign: 'center',
              marginBottom: total > 0 ? 0 : 0,
            }}>
              <div style={{ fontSize: 26, marginBottom: 8 }}>✍️</div>
              <p style={{ margin: '0 0 4px', fontWeight: 700, color: '#111827', fontSize: 15 }}>
                Rate &amp; review this product
              </p>
              <p style={{ margin: '0 0 14px', color: '#6b7280', fontSize: 13 }}>
                Login to share your experience with others.
              </p>
              <button
                onClick={() => openAuthModal()}
                style={{
                  background: BRAND_BLUE, color: '#fff', border: 'none',
                  borderRadius: 10, padding: '11px 26px', fontSize: 14,
                  fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit',
                }}
              >
                Login to Write a Review
              </button>
            </div>
          )}

          {/* ── Write / Edit form ── */}
          {user && (!myReview || editing) && (
            <div style={{
              border: '1.5px solid #e4ecfb', borderRadius: 14,
              padding: '20px',
              marginTop: carouselReviews.length > 0 ? 0 : 0,
            }}>
              <h3 style={{ fontFamily: 'Poppins,sans-serif', fontWeight: 700, fontSize: 15, color: '#111827', margin: '0 0 18px' }}>
                {editing ? 'Edit Your Review' : 'Write a Review'}
              </h3>

              {/* Stars */}
              <div style={{ marginBottom: 18 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Your Rating *
                </label>
                <ClickStars value={rating} onChange={v => { setRating(v); setFormError('') }} />
                {rating > 0 && (
                  <span style={{ display: 'block', marginTop: 4, fontSize: 13, color: '#6b7280' }}>{RATING_LABEL[rating]}</span>
                )}
              </div>

              {/* Display name */}
              <div style={{ marginBottom: 14 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Display Name *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={e => { setName(e.target.value); setFormError('') }}
                  placeholder="e.g. Priya S."
                  style={{ width: '100%', maxWidth: 300, border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '10px 14px', fontSize: 14, outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit' }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE }}
                  onBlur={e => { e.target.style.borderColor = '#e5e7eb' }}
                />
              </div>

              {/* Review text */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Your Review <span style={{ fontWeight: 400, textTransform: 'none', fontSize: 12 }}>(optional)</span>
                </label>
                <textarea
                  value={text}
                  onChange={e => { setText(e.target.value); setFormError('') }}
                  placeholder="Share your experience with this product…"
                  rows={3}
                  style={{ width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '10px 14px', fontSize: 14, outline: 'none', resize: 'vertical', boxSizing: 'border-box', fontFamily: 'inherit' }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE }}
                  onBlur={e => { e.target.style.borderColor = '#e5e7eb' }}
                />
              </div>

              {formError && (
                <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 10, padding: '10px 14px', marginBottom: 12, color: '#dc2626', fontSize: 13, fontWeight: 500 }}>
                  {formError}
                </div>
              )}
              {success && (
                <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 10, padding: '10px 14px', marginBottom: 12, color: '#16a34a', fontSize: 13, fontWeight: 600 }}>
                  ✓ Review submitted! Thank you.
                </div>
              )}

              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <button
                  onClick={handleSubmit}
                  disabled={submitting}
                  style={{
                    background: BRAND_BLUE, color: '#fff', border: 'none',
                    borderRadius: 10, padding: '11px 24px', fontSize: 14,
                    fontWeight: 700, cursor: submitting ? 'not-allowed' : 'pointer',
                    opacity: submitting ? 0.7 : 1, fontFamily: 'inherit',
                  }}
                >
                  {submitting ? 'Submitting…' : editing ? 'Update Review' : 'Submit Review'}
                </button>
                {editing && (
                  <button
                    onClick={() => { setEditing(false); setFormError('') }}
                    style={{ background: '#f3f4f6', color: '#374151', border: 'none', borderRadius: 10, padding: '11px 18px', fontSize: 14, fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit' }}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          )}

          {/* ── Empty state ── */}
          {total === 0 && user && !myReview && (
            <p style={{ textAlign: 'center', padding: '8px 0', color: '#9ca3af', fontSize: 14 }}>
              No reviews yet — be the first!
            </p>
          )}
        </>
      )}
    </div>
  )
}
