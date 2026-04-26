import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const BRAND_BLUE   = '#1B3F8A'
const ORANGE       = '#FF9933'
const AVATAR_COLORS = ['#1B3F8A', '#0d7c66', '#9333ea', '#c2410c', '#0369a1', '#b45309']

// Strip "sample-" prefix so reviews match regardless of backend path
function normId(id) { return id ? String(id).replace(/^sample-/, '') : '' }

function getAvatarColor(name) {
  let h = 0
  for (let i = 0; i < name.length; i++) h = name.charCodeAt(i) + ((h << 5) - h)
  return AVATAR_COLORS[Math.abs(h) % AVATAR_COLORS.length]
}

function Avatar({ name, size = 44 }) {
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
      background: rating >= 4 ? '#15803d' : rating >= 3 ? '#d97706' : '#dc2626',
      color: '#fff', borderRadius: 6, padding: '3px 9px', fontSize: 13, fontWeight: 700,
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
        <span key={s} onClick={() => onChange(s)} onMouseEnter={() => setHover(s)} onMouseLeave={() => setHover(0)}
          style={{ fontSize: 36, lineHeight: 1, cursor: 'pointer', color: s <= (hover || value) ? ORANGE : '#d1d5db', transition: 'color 0.1s' }}>★</span>
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
        <div style={{ width: `${pct}%`, height: '100%', borderRadius: 99, background: `linear-gradient(90deg, ${ORANGE}, #fbbf24)`, transition: 'width 0.7s ease' }} />
      </div>
      <span style={{ color: '#9ca3af', width: 22, textAlign: 'right', fontSize: 11 }}>{count}</span>
    </div>
  )
}

const RATING_LABEL = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent']

function formatDate(iso) {
  const d = new Date(iso)
  return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}/${d.getFullYear()}`
}

// ── Nykaa-style vertical review card ──
function ReviewCard({ review, isOwn, onEdit }) {
  return (
    <div style={{
      padding: '20px 0',
      borderBottom: '1px solid #f3f4f6',
      background: isOwn ? '#f8fbff' : 'transparent',
      borderRadius: isOwn ? 12 : 0,
      padding: isOwn ? '20px 16px' : '20px 0',
      marginBottom: isOwn ? 4 : 0,
      border: isOwn ? '1.5px solid #dbeafe' : 'none',
      borderBottom: isOwn ? '1.5px solid #dbeafe' : '1px solid #f3f4f6',
    }}>
      {/* Row 1: avatar + name/verified + star + date */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14, marginBottom: 12 }}>
        <Avatar name={review.reviewer_name} />
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 8, marginBottom: 3 }}>
            <span style={{ fontWeight: 700, fontSize: 15, color: '#111827' }}>{review.reviewer_name}</span>
            {isOwn && (
              <span style={{ fontSize: 10, fontWeight: 700, color: BRAND_BLUE, background: '#dbeafe', padding: '2px 8px', borderRadius: 99, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Your Review
              </span>
            )}
          </div>
          {/* Verified + date row */}
          <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <svg width="13" height="13" viewBox="0 0 20 20" fill="#16a34a">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span style={{ fontSize: 12, color: '#16a34a', fontWeight: 500 }}>Verified User</span>
            </div>
            <span style={{ fontSize: 12, color: '#9ca3af' }}>{formatDate(review.created_at)}</span>
          </div>
        </div>
        {/* Star badge — right side */}
        <StarBadge rating={review.rating} />
      </div>

      {/* Row 2: review text */}
      <div style={{ paddingLeft: 58 }}>
        {review.review_text ? (
          <p style={{ margin: 0, fontSize: 14, color: '#374151', lineHeight: 1.75 }}>
            {review.review_text}
          </p>
        ) : (
          <p style={{ margin: 0, fontSize: 13, color: '#9ca3af', fontStyle: 'italic' }}>
            Rated without a written review.
          </p>
        )}
        {isOwn && (
          <button onClick={onEdit}
            style={{ marginTop: 12, fontSize: 12, color: BRAND_BLUE, background: 'none', border: `1.5px solid ${BRAND_BLUE}`, borderRadius: 8, padding: '5px 14px', cursor: 'pointer', fontWeight: 600, fontFamily: 'inherit' }}>
            Edit Review
          </button>
        )}
      </div>
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

  const fetchReviews = async () => {
    setLoading(true)
    const { data, error } = await supabase
      .from('product_reviews')
      .select('*')
      .eq('product_id', normId(productId))
      .order('created_at', { ascending: false })
    if (error) console.error('[Reviews] fetch error:', error)
    const list = data || []
    setReviews(list)
    setLoading(false)
  }

  // Fetch once per product — NOT on user change to avoid double-fetch
  useEffect(() => { if (productId) fetchReviews() }, [productId])

  // Derive myReview from cached list — zero extra network calls
  useEffect(() => {
    setMyReview(user ? (reviews.find(r => r.user_id === user.id) || null) : null)
  }, [user, reviews])

  // Pre-fill form
  useEffect(() => {
    if (myReview && editing) {
      setName(myReview.reviewer_name); setRating(myReview.rating); setText(myReview.review_text || '')
    } else if (!myReview && user) {
      const meta = user.user_metadata
      setName(meta?.full_name || meta?.name || (user.email ? user.email.split('@')[0] : '') || user.phone || '')
      setRating(0); setText('')
    }
  }, [myReview, user, editing])

  const total = reviews.length
  const avg   = total > 0 ? reviews.reduce((s, r) => s + r.rating, 0) / total : 0

  const handleSubmit = async () => {
    setFormError('')
    if (!rating)      { setFormError('⭐ Please select a star rating first.'); return }
    if (!name.trim()) { setFormError('Please enter your display name.'); return }
    if (text.trim().length > 0 && text.trim().length < 5) { setFormError('Review text must be at least 5 characters.'); return }
    if (!productId)   { setFormError('Product ID missing — please reload the page.'); return }

    setSubmitting(true)
    const payload = { product_id: normId(productId), product_name: productName, user_id: user.id, reviewer_name: name.trim(), rating, review_text: text.trim() }
    console.log('[Review] submit:', payload)

    let err
    if (myReview && editing) {
      const { error } = await supabase.from('product_reviews')
        .update({ reviewer_name: payload.reviewer_name, rating: payload.rating, review_text: payload.review_text })
        .eq('id', myReview.id).eq('user_id', user.id)
      err = error
    } else {
      const { error } = await supabase.from('product_reviews').upsert(payload, { onConflict: 'product_id,user_id' })
      err = error
    }

    if (err) {
      console.error('[Review] error:', err)
      let msg = err.message || 'Something went wrong. Please try again.'
      if (err.code === '42P01') msg = 'Reviews table not found — please contact support.'
      if (err.code === '42501' || err.message?.includes('policy')) msg = 'Session expired. Please log out and log in again.'
      setFormError(msg)
    } else {
      setSuccess(true); setEditing(false)
      await fetchReviews()
    }
    setSubmitting(false)
  }

  const otherReviews = user && myReview ? reviews.filter(r => r.user_id !== user.id) : reviews

  return (
    <div className="card p-4 sm:p-6 mb-6">

      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontFamily: 'Poppins,sans-serif', fontWeight: 800, fontSize: 20, color: BRAND_BLUE, margin: 0 }}>
          Ratings &amp; Reviews by Users
        </h2>
        <div style={{ height: 3, width: 56, borderRadius: 99, background: ORANGE, marginTop: 8 }} />
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '32px 0', color: '#9ca3af', fontSize: 14 }}>Loading reviews…</div>
      ) : (
        <>
          {/* Rating summary strip */}
          {total > 0 && (
            <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', padding: '16px 20px', background: '#f8faff', borderRadius: 14, border: '1px solid #e4ecfb', marginBottom: 24 }}>
              <div style={{ textAlign: 'center', minWidth: 72 }}>
                <div style={{ fontSize: 46, fontWeight: 900, lineHeight: 1, color: BRAND_BLUE, fontFamily: 'Poppins,sans-serif' }}>{avg.toFixed(1)}</div>
                <div style={{ marginTop: 5 }}><StarsRow rating={avg} size={16} /></div>
                <div style={{ fontSize: 11, color: '#9ca3af', marginTop: 4 }}>{total} {total === 1 ? 'review' : 'reviews'}</div>
              </div>
              <div style={{ flex: 1, minWidth: 140, display: 'flex', flexDirection: 'column', gap: 6, justifyContent: 'center' }}>
                {[5,4,3,2,1].map(s => (
                  <RatingBar key={s} star={s} count={reviews.filter(r => r.rating === s).length} total={total} />
                ))}
              </div>
            </div>
          )}

          {/* Auth gate */}
          {!user && (
            <div style={{ border: '1.5px dashed #d1d5db', borderRadius: 14, padding: '20px', textAlign: 'center', marginBottom: total > 0 ? 24 : 0 }}>
              <div style={{ fontSize: 26, marginBottom: 8 }}>✍️</div>
              <p style={{ margin: '0 0 4px', fontWeight: 700, color: '#111827', fontSize: 15 }}>Rate &amp; review this product</p>
              <p style={{ margin: '0 0 14px', color: '#6b7280', fontSize: 13 }}>Login to share your experience with others.</p>
              <button onClick={() => openAuthModal()}
                style={{ background: BRAND_BLUE, color: '#fff', border: 'none', borderRadius: 10, padding: '11px 26px', fontSize: 14, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                Login to Write a Review
              </button>
            </div>
          )}

          {/* User's own review — shown at top */}
          {user && myReview && !editing && (
            <ReviewCard review={myReview} isOwn onEdit={() => { setEditing(true); setSuccess(false) }} />
          )}

          {/* Write / Edit form */}
          {user && (!myReview || editing) && (
            <div style={{ border: '1.5px solid #e4ecfb', borderRadius: 14, padding: '20px', marginBottom: 24 }}>
              <h3 style={{ fontFamily: 'Poppins,sans-serif', fontWeight: 700, fontSize: 15, color: '#111827', margin: '0 0 18px' }}>
                {editing ? 'Edit Your Review' : 'Write a Review'}
              </h3>

              <div style={{ marginBottom: 18 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Your Rating *</label>
                <ClickStars value={rating} onChange={v => { setRating(v); setFormError('') }} />
                {rating > 0 && <span style={{ display: 'block', marginTop: 4, fontSize: 13, color: '#6b7280' }}>{RATING_LABEL[rating]}</span>}
              </div>

              <div style={{ marginBottom: 14 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Display Name *</label>
                <input type="text" value={name} onChange={e => { setName(e.target.value); setFormError('') }} placeholder="e.g. Priya S."
                  style={{ width: '100%', maxWidth: 300, border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '10px 14px', fontSize: 14, outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit' }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE }} onBlur={e => { e.target.style.borderColor = '#e5e7eb' }} />
              </div>

              <div style={{ marginBottom: 16 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Your Review <span style={{ fontWeight: 400, textTransform: 'none', fontSize: 12 }}>(optional)</span>
                </label>
                <textarea value={text} onChange={e => { setText(e.target.value); setFormError('') }} placeholder="Share your experience with this product…" rows={3}
                  style={{ width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '10px 14px', fontSize: 14, outline: 'none', resize: 'vertical', boxSizing: 'border-box', fontFamily: 'inherit' }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE }} onBlur={e => { e.target.style.borderColor = '#e5e7eb' }} />
              </div>

              {formError && (
                <div style={{ background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 10, padding: '10px 14px', marginBottom: 12, color: '#dc2626', fontSize: 13, fontWeight: 500 }}>{formError}</div>
              )}
              {success && (
                <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 10, padding: '10px 14px', marginBottom: 12, color: '#16a34a', fontSize: 13, fontWeight: 600 }}>✓ Review submitted! Thank you.</div>
              )}

              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={handleSubmit} disabled={submitting}
                  style={{ background: BRAND_BLUE, color: '#fff', border: 'none', borderRadius: 10, padding: '11px 24px', fontSize: 14, fontWeight: 700, cursor: submitting ? 'not-allowed' : 'pointer', opacity: submitting ? 0.7 : 1, fontFamily: 'inherit' }}>
                  {submitting ? 'Submitting…' : editing ? 'Update Review' : 'Submit Review'}
                </button>
                {editing && (
                  <button onClick={() => { setEditing(false); setFormError('') }}
                    style={{ background: '#f3f4f6', color: '#374151', border: 'none', borderRadius: 10, padding: '11px 18px', fontSize: 14, fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit' }}>
                    Cancel
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Other reviews — vertical stacked, Nykaa/Amazon style */}
          {otherReviews.length > 0 && (
            <div>
              {/* Divider with count */}
              {(user && myReview) && (
                <div style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '8px 0 4px' }}>
                  <div style={{ flex: 1, height: 1, background: '#f3f4f6' }} />
                  <span style={{ fontSize: 12, color: '#9ca3af', fontWeight: 600, whiteSpace: 'nowrap' }}>
                    {otherReviews.length} more {otherReviews.length === 1 ? 'review' : 'reviews'}
                  </span>
                  <div style={{ flex: 1, height: 1, background: '#f3f4f6' }} />
                </div>
              )}
              {otherReviews.map((review, idx) => (
                <div key={review.id} style={{ borderBottom: idx < otherReviews.length - 1 ? '1px solid #f3f4f6' : 'none' }}>
                  <ReviewCard review={review} isOwn={false} />
                </div>
              ))}
            </div>
          )}

          {/* Empty state */}
          {total === 0 && user && !myReview && (
            <p style={{ textAlign: 'center', padding: '8px 0', color: '#9ca3af', fontSize: 14 }}>No reviews yet — be the first!</p>
          )}
        </>
      )}
    </div>
  )
}
