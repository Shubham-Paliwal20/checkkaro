import { useState, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'

const MAX_SIZE_MB = 8

export default function AddProductModal({ user, onClose, onSuccess }) {
  const [productName, setProductName]     = useState('')
  const [imageFile, setImageFile]         = useState(null)
  const [imagePreview, setImagePreview]   = useState(null)
  const [upiOrMobile, setUpiOrMobile]     = useState('')
  const [ingredients, setIngredients]     = useState('')
  const [uploading, setUploading]         = useState(false)
  const [error, setError]                 = useState(null)
  const [dragOver, setDragOver]           = useState(false)
  const inputRef = useRef()

  const handleImageSelect = (files) => {
    const file = Array.from(files).find(f => f.type.startsWith('image/'))
    if (!file) return
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setError(`Image must be under ${MAX_SIZE_MB}MB`)
      return
    }
    setError(null)
    if (imagePreview) URL.revokeObjectURL(imagePreview)
    setImageFile(file)
    setImagePreview(URL.createObjectURL(file))
    if (inputRef.current) inputRef.current.value = ''
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    handleImageSelect(e.dataTransfer.files)
  }

  const handleSubmit = async () => {
    const name = productName.trim()
    const upi  = upiOrMobile.trim()

    if (!name)      { setError('Product name is required'); return }
    if (!imageFile) { setError('Product image is required'); return }
    if (!upi)       { setError('UPI ID or mobile number is required'); return }

    setUploading(true)
    setError(null)

    try {
      // Upload image to Supabase storage
      const ext  = imageFile.name.split('.').pop()?.toLowerCase() || 'jpg'
      const path = `new-submissions/${user.id}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
      const { error: upErr } = await supabase.storage
        .from('product-images')
        .upload(path, imageFile, { contentType: imageFile.type, upsert: false })
      if (upErr) throw new Error(`Image upload failed: ${upErr.message}`)

      const { data: { publicUrl } } = supabase.storage.from('product-images').getPublicUrl(path)

      // Insert into product_submissions — same table the Admin panel reads
      const { error: dbErr } = await supabase.from('product_submissions').insert({
        product_name_searched: name,
        images:                [publicUrl],
        contact:               upi,
        email:                 user.email || null,
        user_id:               user.id,
        status:                'pending',
      })
      if (dbErr) throw new Error(dbErr.message)

      onSuccess('Submitted! You will earn ₹1 after admin approves your product.')
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const canSubmit = productName.trim() && imageFile && upiOrMobile.trim() && !uploading

  return (
    <div
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}
      onClick={e => e.target === e.currentTarget && onClose()}
    >
      <div style={{ background: '#fff', borderRadius: 20, width: '100%', maxWidth: 480, maxHeight: '92vh', overflowY: 'auto', boxShadow: '0 20px 60px rgba(0,0,0,0.25)' }}>

        {/* Header */}
        <div style={{ padding: '18px 20px 14px', borderBottom: '1px solid #f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, background: '#fff', zIndex: 1 }}>
          <div>
            <h3 style={{ margin: 0, fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827' }}>
              📦 Add a New Product
            </h3>
            <p style={{ margin: '3px 0 0', fontSize: 12, color: '#9ca3af' }}>
              Help grow our database · earn ₹1 on approval
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: 22, color: '#9ca3af', cursor: 'pointer', lineHeight: 1, padding: 4 }}>×</button>
        </div>

        <div style={{ padding: '16px 20px 20px' }}>

          {/* How it works banner */}
          <div style={{ marginBottom: 16, padding: '10px 14px', background: '#f0f9ff', border: '1px solid #bae6fd', borderRadius: 10, fontSize: 12, color: '#0369a1' }}>
            <strong>How it works:</strong> Submit the product name, a photo of the packaging, and your UPI/mobile.
            Admin will review and credit <strong>₹1 to your UPI/mobile</strong> within 24 hours.
          </div>

          {/* Product Name */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 6 }}>
              Product Name <span style={{ color: '#dc2626' }}>*</span>
            </label>
            <input
              type="text"
              placeholder="e.g. Amul Butter 100g"
              value={productName}
              onChange={e => setProductName(e.target.value)}
              style={{ width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '10px 12px', fontSize: 13, fontFamily: 'inherit', outline: 'none', color: '#111827' }}
            />
          </div>

          {/* Product Image */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 6 }}>
              Product Image <span style={{ color: '#dc2626' }}>*</span>
            </label>

            {imagePreview ? (
              <div style={{ position: 'relative', width: 100, height: 100, borderRadius: 12, overflow: 'hidden', border: '2px solid #86efac', background: '#f9fafb', marginBottom: 8 }}>
                <img src={imagePreview} alt="preview" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                <button
                  onClick={() => { URL.revokeObjectURL(imagePreview); setImageFile(null); setImagePreview(null) }}
                  style={{ position: 'absolute', top: 4, right: 4, width: 20, height: 20, borderRadius: '50%', background: 'rgba(0,0,0,0.65)', border: 'none', color: '#fff', fontSize: 12, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1 }}
                >×</button>
                <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, background: 'rgba(0,0,0,0.5)', color: '#fff', fontSize: 9, textAlign: 'center', padding: '2px 0', fontWeight: 700 }}>FRONT</div>
              </div>
            ) : (
              <div
                onClick={() => inputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                style={{
                  border: `2px dashed ${dragOver ? '#FF9933' : '#e5e7eb'}`,
                  borderRadius: 12, padding: '20px 16px', textAlign: 'center', cursor: 'pointer',
                  background: dragOver ? '#fff7ed' : '#fafafa', transition: 'all 0.15s', marginBottom: 8,
                }}
              >
                <div style={{ fontSize: 28, marginBottom: 4 }}>📷</div>
                <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#374151' }}>Click to upload or drag & drop</p>
                <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>JPG, PNG, WEBP · max {MAX_SIZE_MB}MB</p>
              </div>
            )}
            <input ref={inputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={e => handleImageSelect(e.target.files)} />
          </div>

          {/* UPI / Mobile */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 6 }}>
              UPI ID or Mobile Number <span style={{ color: '#dc2626' }}>*</span>
            </label>
            <input
              type="text"
              placeholder="e.g. name@upi  or  9876543210"
              value={upiOrMobile}
              onChange={e => setUpiOrMobile(e.target.value)}
              style={{ width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '10px 12px', fontSize: 13, fontFamily: 'inherit', outline: 'none', color: '#111827' }}
            />
            <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>Admin will send ₹1 here after approving your submission</p>
          </div>

          {/* Ingredients — optional */}
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 6 }}>
              Ingredients <span style={{ fontSize: 11, fontWeight: 400, color: '#9ca3af' }}>(optional — paste from product label)</span>
            </label>
            <textarea
              placeholder="e.g. Wheat Flour, Sugar, Edible Vegetable Oil, Salt, Raising Agents (INS 500, INS 503)..."
              value={ingredients}
              onChange={e => setIngredients(e.target.value)}
              rows={3}
              style={{ width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '10px 12px', fontSize: 13, fontFamily: 'inherit', outline: 'none', color: '#111827', resize: 'vertical', minHeight: 72 }}
            />
          </div>

          {/* Error */}
          {error && (
            <div style={{ marginBottom: 12, padding: '9px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, color: '#dc2626', fontWeight: 600 }}>
              {error}
            </div>
          )}

          {/* Earn badge */}
          <div style={{ marginBottom: 14, padding: '9px 12px', background: '#fefce8', border: '1px solid #fde68a', borderRadius: 8, fontSize: 12, color: '#92400e', display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: 18 }}>💰</span>
            <span><strong>Earn ₹1 per product</strong> — credited after admin reviews your submission</span>
          </div>

          <button
            onClick={handleSubmit}
            disabled={!canSubmit}
            style={{
              width: '100%', padding: '13px 0',
              background: canSubmit ? '#FF9933' : '#f3f4f6',
              color: canSubmit ? '#fff' : '#9ca3af',
              border: 'none', borderRadius: 12, fontSize: 14, fontWeight: 700,
              cursor: canSubmit ? 'pointer' : 'not-allowed',
              fontFamily: 'inherit', transition: 'background 0.15s',
            }}
          >
            {uploading ? 'Submitting…' : 'Submit for Review · Earn ₹1'}
          </button>
        </div>
      </div>
    </div>
  )
}
