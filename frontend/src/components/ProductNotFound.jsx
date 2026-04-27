import { useState, useRef } from 'react'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const MAX_IMAGES = 3
const MAX_FILE_MB = 8

export default function ProductNotFound({ productName }) {
  const { user, openAuthModal } = useAuth()
  const [images,   setImages]   = useState([])   // File[]
  const [previews, setPreviews] = useState([])   // data URLs
  const [contact,  setContact]  = useState('')
  const [loading,  setLoading]  = useState(false)
  const [success,  setSuccess]  = useState(false)
  const [error,    setError]    = useState('')
  const fileRef = useRef()

  const handleFiles = (files) => {
    const remaining = MAX_IMAGES - images.length
    if (remaining <= 0) { setError('Maximum 3 images already added.'); return }
    const accepted = Array.from(files).slice(0, remaining).filter(f => {
      if (!f.type.startsWith('image/')) { setError('Only image files are allowed.'); return false }
      if (f.size > MAX_FILE_MB * 1024 * 1024) { setError(`Each image must be under ${MAX_FILE_MB}MB.`); return false }
      return true
    })
    if (!accepted.length) return
    setImages(prev => [...prev, ...accepted])
    accepted.forEach(f => {
      const r = new FileReader()
      r.onload = ev => setPreviews(prev => [...prev, ev.target.result])
      r.readAsDataURL(f)
    })
    setError('')
  }

  const removeImage = (idx) => {
    setImages(p  => p.filter((_, i) => i !== idx))
    setPreviews(p => p.filter((_, i) => i !== idx))
  }

  const handleDrop = (e) => {
    e.preventDefault()
    handleFiles(e.dataTransfer.files)
  }

  const handleSubmit = async () => {
    if (images.length === 0) { setError('Please add at least 1 photo of the product.'); return }
    if (!contact.trim())     { setError('Please enter your mobile number or UPI ID.'); return }
    setLoading(true); setError('')

    try {
      const imageUrls = []
      for (const file of images) {
        const ext  = file.name.split('.').pop()
        const path = `${user.id}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
        const { error: uploadErr } = await supabase.storage
          .from('product-submissions')
          .upload(path, file, { upsert: false })
        if (uploadErr) throw uploadErr
        const { data: urlData } = supabase.storage
          .from('product-submissions')
          .getPublicUrl(path)
        imageUrls.push(urlData.publicUrl)
      }

      const { error: dbErr } = await supabase.from('product_submissions').insert({
        user_id:              user.id,
        email:                user.email || '',
        product_name_searched: productName,
        images:               imageUrls,
        contact:              contact.trim(),
        status:               'pending',
      })
      if (dbErr) throw dbErr
      setSuccess(true)
    } catch (e) {
      setError(e.message || 'Submission failed. Please try again.')
    }
    setLoading(false)
  }

  if (success) {
    return (
      <div style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
        <div style={{ textAlign: 'center', maxWidth: 420 }}>
          <div style={{ fontSize: 72, marginBottom: 16 }}>🎉</div>
          <h2 style={{ fontFamily: 'Poppins, sans-serif', fontSize: 24, fontWeight: 800, color: '#0D1B2A', margin: '0 0 12px' }}>
            Submission Received!
          </h2>
          <p style={{ color: '#6b7280', fontSize: 15, lineHeight: 1.6, margin: '0 0 24px' }}>
            Thank you for contributing. Our team will review your submission and add it to CheckKaro.
            Once approved, <strong>₹1 will be sent to your UPI / mobile number</strong>.
          </p>
          <button onClick={() => window.history.back()}
            style={{ background: '#FF9933', color: '#fff', border: 'none', borderRadius: 999, padding: '12px 32px', fontSize: 15, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
            ← Go Back
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: 560, margin: '0 auto', padding: '40px 20px 60px' }}>

      {/* Hero */}
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <div style={{ fontSize: 64, marginBottom: 12 }}>📦</div>
        <h1 style={{ fontFamily: 'Poppins, sans-serif', fontSize: 26, fontWeight: 800, color: '#0D1B2A', margin: '0 0 8px' }}>
          Product Not Found
        </h1>
        <p style={{ color: '#6b7280', fontSize: 15, margin: '0 0 20px' }}>
          We don't have <strong>"{productName}"</strong> in our database yet.
        </p>

        {/* Earn badge */}
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10, background: 'linear-gradient(135deg, #fff8e1, #fff3cd)', border: '1.5px solid #fbbf24', borderRadius: 14, padding: '12px 22px' }}>
          <span style={{ fontSize: 28 }}>💰</span>
          <div style={{ textAlign: 'left' }}>
            <div style={{ fontWeight: 800, fontSize: 15, color: '#92400e' }}>Add Product &amp; Earn ₹1</div>
            <div style={{ fontSize: 12, color: '#b45309' }}>Upload product photos → get approved → receive reward</div>
          </div>
        </div>
      </div>

      {!user ? (
        /* ── Not logged in ── */
        <div style={{ background: '#f9fafb', border: '1.5px solid #e5e7eb', borderRadius: 16, padding: '28px 24px', textAlign: 'center' }}>
          <div style={{ fontSize: 36, marginBottom: 12 }}>🔐</div>
          <h3 style={{ fontFamily: 'Poppins, sans-serif', fontSize: 17, fontWeight: 700, color: '#111827', margin: '0 0 8px' }}>
            Login to contribute
          </h3>
          <p style={{ color: '#6b7280', fontSize: 14, margin: '0 0 20px' }}>
            Sign in to add this product and earn ₹1 when it's approved.
          </p>
          <button onClick={() => openAuthModal()}
            style={{ background: '#FF9933', color: '#fff', border: 'none', borderRadius: 999, padding: '12px 32px', fontSize: 15, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
            Login / Sign up
          </button>
        </div>
      ) : (
        /* ── Logged in: show form ── */
        <div style={{ background: '#fff', border: '1.5px solid #e5e7eb', borderRadius: 16, padding: '24px 20px', boxShadow: '0 2px 16px rgba(0,0,0,0.06)' }}>

          {/* Image upload */}
          <label style={{ fontSize: 12, fontWeight: 700, color: '#374151', display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Product Photos <span style={{ color: '#ef4444' }}>*</span>
            <span style={{ fontWeight: 400, textTransform: 'none', letterSpacing: 0, color: '#9ca3af' }}> (min 1, max 3)</span>
          </label>

          {/* Previews row */}
          {previews.length > 0 && (
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginBottom: 12 }}>
              {previews.map((src, i) => (
                <div key={i} style={{ position: 'relative', width: 88, height: 88, borderRadius: 10, overflow: 'hidden', border: '1.5px solid #e5e7eb', flexShrink: 0 }}>
                  <img src={src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  <button onClick={() => removeImage(i)}
                    style={{ position: 'absolute', top: 4, right: 4, background: 'rgba(0,0,0,0.6)', color: '#fff', border: 'none', borderRadius: '50%', width: 22, height: 22, fontSize: 12, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 0, lineHeight: 1 }}>
                    ✕
                  </button>
                </div>
              ))}
              {images.length < MAX_IMAGES && (
                <button onClick={() => fileRef.current?.click()}
                  style={{ width: 88, height: 88, borderRadius: 10, border: '1.5px dashed #d1d5db', background: '#f9fafb', cursor: 'pointer', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 4, color: '#9ca3af', fontSize: 11, fontWeight: 600 }}>
                  <span style={{ fontSize: 22 }}>+</span>
                  Add
                </button>
              )}
            </div>
          )}

          {/* Drop zone (shown when no images yet) */}
          {images.length === 0 && (
            <div
              onDrop={handleDrop}
              onDragOver={e => e.preventDefault()}
              onClick={() => fileRef.current?.click()}
              style={{ border: '2px dashed #d1d5db', borderRadius: 12, padding: '28px 20px', textAlign: 'center', cursor: 'pointer', marginBottom: 18, background: '#fafafa', transition: 'border-color 0.2s' }}
            >
              <div style={{ fontSize: 36, marginBottom: 6 }}>📷</div>
              <p style={{ color: '#6b7280', fontSize: 14, margin: '0 0 4px', fontWeight: 600 }}>Tap to add photos</p>
              <p style={{ color: '#9ca3af', fontSize: 12, margin: 0 }}>or drag &amp; drop here • up to 3 images • max {MAX_FILE_MB}MB each</p>
            </div>
          )}

          <input ref={fileRef} type="file" accept="image/*" multiple style={{ display: 'none' }}
            onChange={e => { handleFiles(e.target.files); e.target.value = '' }} />

          {/* Contact */}
          <label style={{ fontSize: 12, fontWeight: 700, color: '#374151', display: 'block', marginBottom: 6, textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: images.length > 0 ? 4 : 0 }}>
            Mobile Number or UPI ID <span style={{ color: '#ef4444' }}>*</span>
          </label>
          <input
            type="text"
            placeholder="e.g. 9876543210 or name@upi"
            value={contact}
            onChange={e => { setContact(e.target.value); setError('') }}
            style={{ width: '100%', border: '1.5px solid #e5e7eb', borderRadius: 10, padding: '12px 14px', fontSize: 15, outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit', marginBottom: 8 }}
          />
          <p style={{ color: '#9ca3af', fontSize: 12, margin: '0 0 18px' }}>
            We'll send your ₹1 reward here once your submission is approved.
          </p>

          {/* Searched for */}
          <div style={{ background: '#f3f4f6', borderRadius: 8, padding: '8px 12px', marginBottom: 18, fontSize: 13, color: '#6b7280' }}>
            Submitting for: <strong style={{ color: '#374151' }}>"{productName}"</strong>
          </div>

          {error && (
            <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: 8, padding: '10px 14px', marginBottom: 14 }}>
              <p style={{ color: '#dc2626', fontSize: 13, margin: 0 }}>{error}</p>
            </div>
          )}

          <button onClick={handleSubmit} disabled={loading}
            style={{ width: '100%', background: loading ? '#d1d5db' : 'linear-gradient(135deg, #FF9933, #e8880a)', color: '#fff', border: 'none', borderRadius: 10, padding: 15, fontSize: 15, fontWeight: 700, cursor: loading ? 'not-allowed' : 'pointer', fontFamily: 'inherit' }}>
            {loading ? 'Uploading & Submitting…' : '📤 Submit Product'}
          </button>

          <p style={{ textAlign: 'center', color: '#9ca3af', fontSize: 12, margin: '12px 0 0' }}>
            Logged in as <strong>{user.email}</strong>
          </p>
        </div>
      )}
    </div>
  )
}
