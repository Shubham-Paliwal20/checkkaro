import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const BRAND_BLUE = '#1B3F8A'
const ORANGE = '#FF9933'

// Avatar colours cycle through a palette
const AVATAR_COLORS = ['#1B3F8A', '#0d7c66', '#9333ea', '#c2410c', '#0369a1', '#b45309']

function getAvatarColor(name) {
  let hash = 0
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash)
  return AVATAR_COLORS[Math.abs(hash) % AVATAR_COLORS.length]
}

function Avatar({ name, size = 46 }) {
  const parts = (name || 'U').trim().split(/\s+/)
  const init = parts.length >= 2
    ? parts[0][0].toUpperCase() + parts[parts.length - 1][0].toUpperCase()
    : parts[0][0].toUpperCase()
  return (
    <div style={{
      width: size, height: size, borderRadius: '50%', flexShrink: 0,
      background: getAvatarColor(name), color: '#fff',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontWeight: 700, fontSize: size * 0.38, fontFamily: 'Poppins, sans-serif',
    }}>{init}</div>
  )
}

function StarBadge({ rating }) {
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: 4,
      background: '#15803d', color: '#fff',
      borderRadius: 6, padding: '3px 10px',
      fontSize: 13, fontWeight: 700,
    }}>
      {rating} <span style={{ fontSize: 12 }}>★</span>
    </span>
  )
}

function StarsRow({ rating, size = 16 }) {
  return (
    <span style={{ display: 'inline-flex', gap: 2 }}>
      {[1, 2, 3, 4, 5].map(s => (
        <span key={s} style={{ fontSize: size, color: s <= Math.round(rating) ? ORANGE : '#d1d5db', lineHeight: 1 }}>★</span>
      ))}
    </span>
  )
}

function ClickStars({ value, onChange }) {
  const [hover, setHover] = useState(0)
  return (
    <span style={{ display: 'inline-flex', gap: 6 }}>
      {[1, 2, 3, 4, 5].map(s => (
        <span
          key={s}
          onClick={() => onChange(s)}
          onMouseEnter={() => setHover(s)}
          onMouseLeave={() => setHover(0)}
          style={{
            fontSize: 40, lineHeight: 1, cursor: 'pointer',
            color: s <= (hover || value) ? ORANGE : '#d1d5db',
            transition: 'color 0.1s',
          }}
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
      <span style={{ color: ORANGE, fontSize: 12 }}>★</span>
      <div style={{ flex: 1, height: 8, borderRadius: 99, background: '#eef0f4', overflow: 'hidden' }}>
        <div style={{
          width: `${pct}%`, height: '100%', borderRadius: 99,
          background: `linear-gradient(90deg, ${ORANGE}, #fbbf24)`,
          transition: 'width 0.7s ease',
        }} />
      </div>
      <span style={{ color: '#9ca3af', width: 24, textAlign: 'right', fontSize: 12 }}>{count}</span>
    </div>
  )
}

const RATING_LABEL = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent']

function formatDate(iso) {
  const d = new Date(iso)
  const dd = String(d.getDate()).padStart(2, '0')
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const yyyy = d.getFullYear()
  return `${dd}/${mm}/${yyyy}`
}

// Single review card — Nykaa style
function ReviewCard({ review, isOwn }) {
  return (
    <div style={{ padding: '22px 0' }}>
      {/* Top row: avatar + name/badge | star badge + date */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14, marginBottom: 14 }}>
        <Avatar name={review.reviewer_name} />

        {/* Name + verified */}
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
            <span style={{ fontWeight: 700, fontSize: 15, color: '#111827' }}>
              {review.reviewer_name}
            </span>
            {isOwn && (
              <span style={{
                fontSize: 10, fontWeight: 700, color: BRAND_BLUE,
                background: '#dbeafe', padding: '2px 8px', borderRadius: 99,
                textTransform: 'uppercase', letterSpacing: '0.05em',
              }}>Your Review</span>
            )}
          </div>
          {/* Verified buyer */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 3 }}>
            <svg width="13" height="13" viewBox="0 0 20 20" fill="#16a34a">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            <span style={{ fontSize: 12, color: '#16a34a', fontWeight: 500 }}>Verified User</span>
          </div>
        </div>

        {/* Star badge + date */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 4, flexShrink: 0 }}>
          <StarBadge rating={review.rating} />
          <span style={{ fontSize: 12, color: '#9ca3af' }}>{formatDate(review.created_at)}</span>
        </div>
      </div>

      {/* Review text */}
      {review.review_text ? (
        <p style={{
          margin: '0 0 0 60px', fontSize: 14, color: '#374151',
          lineHeight: 1.7,
        }}>
          "{review.review_text}"
        </p>
      ) : (
        <p style={{ margin: '0 0 0 60px', fontSize: 13, color: '#9ca3af', fontStyle: 'italic' }}>
          Rated without a written review.
        </p>
      )}
    </div>
  )
}

export default function ProductReviews({ productId, productName }) {
  const { user, openAuthModal } = useAuth()
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(true)
  const [myReview, setMyReview] = useState(null)
  const [editing, setEditing] = useState(false)

  const [name, setName] = useState('')
  const [rating, setRating] = useState(0)
  const [text, setText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [formError, setFormError] = useState('')
  const [success, setSuccess] = useState(false)

  const fetchReviews = async () => {
    setLoading(true)
    const { data } = await supabase
      .from('product_reviews')
      .select('*')
      .eq('product_id', productId)
      .order('created_at', { ascending: false })
    const list = data || []
    setReviews(list)
    if (user) {
      setMyReview(list.find(r => r.user_id === user.id) || null)
    }
    setLoading(false)
  }

  useEffect(() => {
    if (productId) fetchReviews()
  }, [productId, user])

  useEffect(() => {
    if (myReview && editing) {
      setName(myReview.reviewer_name)
      setRating(myReview.rating)
      setText(myReview.review_text || '')
    } else if (!myReview && user) {
      const meta = user.user_metadata
      setName(meta?.full_name || meta?.name || '')
      setRating(0)
      setText('')
    }
  }, [myReview, user, editing])

  const total = reviews.length
  const avg = total > 0 ? reviews.reduce((s, r) => s + r.rating, 0) / total : 0

  const handleSubmit = async () => {
    if (!rating) { setFormError('Please select a star rating.'); return }
    if (!name.trim()) { setFormError('Please enter your display name.'); return }
    if (text.trim() && text.trim().length < 5) { setFormError('Review text must be at least 5 characters.'); return }
    setSubmitting(true)
    setFormError('')

    const payload = {
      product_id: productId,
      product_name: productName,
      user_id: user.id,
      reviewer_name: name.trim(),
      rating,
      review_text: text.trim(),
    }

    let err
    if (myReview && editing) {
      const { error } = await supabase
        .from('product_reviews')
        .update({ reviewer_name: payload.reviewer_name, rating: payload.rating, review_text: payload.review_text })
        .eq('id', myReview.id)
      err = error
    } else {
      const { error } = await supabase.from('product_reviews').insert(payload)
      err = error
    }

    if (err) {
      setFormError(err.message || 'Something went wrong. Please try again.')
    } else {
      setSuccess(true)
      setEditing(false)
      await fetchReviews()
    }
    setSubmitting(false)
  }

  // Reviews to show below (exclude own — shown separately in its card)
  const otherReviews = user && myReview ? reviews.filter(r => r.user_id !== user.id) : reviews

  return (
    <div className="card p-4 sm:p-6 mb-6">

      {/* ── Section header ── */}
      <div style={{ marginBottom: 24 }}>
        <h2 style={{
          fontFamily: 'Poppins, sans-serif', fontWeight: 800, fontSize: 20,
          color: BRAND_BLUE, margin: 0,
        }}>
          Ratings &amp; Reviews by Users
        </h2>
        <div style={{ height: 3, width: 64, borderRadius: 99, background: ORANGE, marginTop: 8 }} />
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '32px 0', color: '#9ca3af', fontSize: 14 }}>
          Loading reviews…
        </div>
      ) : (
        <>
          {/* ── Rating summary strip ── */}
          {total > 0 && (
            <div style={{
              display: 'flex', gap: 32, flexWrap: 'wrap',
              padding: '20px 24px', background: '#f8faff',
              borderRadius: 14, border: '1px solid #e4ecfb',
              marginBottom: 28,
            }}>
              {/* Big score */}
              <div style={{ textAlign: 'center', minWidth: 88 }}>
                <div style={{
                  fontSize: 52, fontWeight: 900, lineHeight: 1,
                  color: BRAND_BLUE, fontFamily: 'Poppins, sans-serif',
                }}>{avg.toFixed(1)}</div>
                <div style={{ marginTop: 6 }}><StarsRow rating={avg} size={18} /></div>
                <div style={{ fontSize: 12, color: '#9ca3af', marginTop: 5 }}>
                  {total} {total === 1 ? 'review' : 'reviews'}
                </div>
              </div>
              {/* Distribution */}
              <div style={{ flex: 1, minWidth: 160, display: 'flex', flexDirection: 'column', gap: 7, justifyContent: 'center' }}>
                {[5, 4, 3, 2, 1].map(star => (
                  <RatingBar key={star} star={star} count={reviews.filter(r => r.rating === star).length} total={total} />
                ))}
              </div>
            </div>
          )}

          {/* ── Auth gate ── */}
          {!user && (
            <div style={{
              border: '1.5px dashed #d1d5db', borderRadius: 14,
              padding: '24px', textAlign: 'center',
              marginBottom: total > 0 ? 28 : 0,
            }}>
              <div style={{ fontSize: 28, marginBottom: 10 }}>✍️</div>
              <p style={{ margin: '0 0 6px', fontWeight: 700, color: '#111827', fontSize: 15 }}>
                Rate &amp; review this product
              </p>
              <p style={{ margin: '0 0 16px', color: '#6b7280', fontSize: 13 }}>
                Login to share your experience. Only verified users can submit reviews.
              </p>
              <button
                onClick={openAuthModal}
                style={{
                  background: BRAND_BLUE, color: '#fff', border: 'none',
                  borderRadius: 10, padding: '11px 28px', fontSize: 14,
                  fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit',
                }}
              >
                Login to Write a Review
              </button>
            </div>
          )}

          {/* ── User's own review (read mode) ── */}
          {user && myReview && !editing && (
            <div style={{
              border: `1.5px solid #c7d7f5`, borderRadius: 14,
              padding: '4px 20px', marginBottom: otherReviews.length > 0 ? 0 : 0,
              background: '#f0f5ff',
            }}>
              <ReviewCard review={myReview} isOwn />
              <div style={{ paddingBottom: 14 }}>
                <button
                  onClick={() => { setEditing(true); setSuccess(false) }}
                  style={{
                    fontSize: 13, color: BRAND_BLUE, background: 'none',
                    border: `1.5px solid ${BRAND_BLUE}`, borderRadius: 8,
                    padding: '5px 16px', cursor: 'pointer', fontWeight: 600,
                  }}
                >
                  Edit Review
                </button>
              </div>
            </div>
          )}

          {/* ── Write / edit form ── */}
          {user && (!myReview || editing) && (
            <div style={{
              border: '1.5px solid #e4ecfb', borderRadius: 14,
              padding: '22px 24px',
              marginBottom: total > 0 || (user && myReview) ? 0 : 0,
            }}>
              <h3 style={{
                fontFamily: 'Poppins, sans-serif', fontWeight: 700,
                fontSize: 16, color: '#111827', margin: '0 0 20px',
              }}>
                {editing ? 'Edit Your Review' : 'Write a Review'}
              </h3>

              {/* Stars */}
              <div style={{ marginBottom: 20 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Your Rating *
                </label>
                <ClickStars value={rating} onChange={v => { setRating(v); setFormError('') }} />
                {rating > 0 && (
                  <span style={{ display: 'block', marginTop: 5, fontSize: 13, color: '#6b7280' }}>
                    {RATING_LABEL[rating]}
                  </span>
                )}
              </div>

              {/* Display name */}
              <div style={{ marginBottom: 16 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Display Name *
                </label>
                <input
                  type="text"
                  value={name}
                  onChange={e => { setName(e.target.value); setFormError('') }}
                  placeholder="e.g. Priya S."
                  style={{
                    width: '100%', maxWidth: 320, border: '1.5px solid #e5e7eb',
                    borderRadius: 10, padding: '10px 14px', fontSize: 14,
                    outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit',
                  }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE; e.target.style.boxShadow = `0 0 0 2px ${BRAND_BLUE}22` }}
                  onBlur={e => { e.target.style.borderColor = '#e5e7eb'; e.target.style.boxShadow = '' }}
                />
              </div>

              {/* Review text */}
              <div style={{ marginBottom: 18 }}>
                <label style={{ fontSize: 11, fontWeight: 700, color: '#6b7280', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
                  Your Review{' '}
                  <span style={{ fontWeight: 400, textTransform: 'none', letterSpacing: 0, fontSize: 12 }}>(optional)</span>
                </label>
                <textarea
                  value={text}
                  onChange={e => { setText(e.target.value); setFormError('') }}
                  placeholder="Share your experience with this product…"
                  rows={3}
                  style={{
                    width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10,
                    padding: '10px 14px', fontSize: 14, outline: 'none',
                    resize: 'vertical', boxSizing: 'border-box', fontFamily: 'inherit',
                  }}
                  onFocus={e => { e.target.style.borderColor = BRAND_BLUE; e.target.style.boxShadow = `0 0 0 2px ${BRAND_BLUE}22` }}
                  onBlur={e => { e.target.style.borderColor = '#e5e7eb'; e.target.style.boxShadow = '' }}
                />
              </div>

              {formError && <p style={{ color: '#ef4444', fontSize: 13, margin: '0 0 12px' }}>{formError}</p>}
              {success && <p style={{ color: '#16a34a', fontSize: 13, margin: '0 0 12px' }}>✓ Review submitted! Thank you.</p>}

              <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                <button
                  onClick={handleSubmit}
                  disabled={submitting}
                  style={{
                    background: BRAND_BLUE, color: '#fff', border: 'none',
                    borderRadius: 10, padding: '11px 26px', fontSize: 14,
                    fontWeight: 700, cursor: submitting ? 'not-allowed' : 'pointer',
                    opacity: submitting ? 0.7 : 1, fontFamily: 'inherit',
                  }}
                >
                  {submitting ? 'Submitting…' : editing ? 'Update Review' : 'Submit Review'}
                </button>
                {editing && (
                  <button
                    onClick={() => { setEditing(false); setFormError('') }}
                    style={{
                      background: '#f3f4f6', color: '#374151', border: 'none',
                      borderRadius: 10, padding: '11px 20px', fontSize: 14,
                      fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit',
                    }}
                  >
                    Cancel
                  </button>
                )}
              </div>
            </div>
          )}

          {/* ── Empty state ── */}
          {total === 0 && user && !myReview && (
            <div style={{ textAlign: 'center', padding: '12px 0 4px', color: '#9ca3af', fontSize: 14 }}>
              No reviews yet — be the first to review this product!
            </div>
          )}

          {/* ── Customer reviews — vertical stacked ── */}
          {otherReviews.length > 0 && (
            <div style={{ marginTop: (user && myReview && !editing) || (user && (!myReview || editing)) ? 24 : 0 }}>
              <h3 style={{
                fontWeight: 700, fontSize: 13, color: '#6b7280',
                margin: '0 0 0', textTransform: 'uppercase', letterSpacing: '0.06em',
                borderBottom: '1px solid #f3f4f6', paddingBottom: 12,
              }}>
                Customer Reviews ({otherReviews.length})
              </h3>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                {otherReviews.map((review, idx) => (
                  <div
                    key={review.id}
                    style={{
                      borderBottom: idx < otherReviews.length - 1 ? '1px solid #f3f4f6' : 'none',
                    }}
                  >
                    <ReviewCard review={review} isOwn={false} />
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
