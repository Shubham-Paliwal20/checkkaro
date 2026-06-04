import { useState, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'

const MAX_SIZE_MB = 8
const MAX_PHOTOS  = 5
const LABELS      = ['FRONT', 'BACK', 'IMG 3', 'IMG 4', 'IMG 5']

export default function AddProductModal({ user, onClose, onSuccess }) {
  const [productName, setProductName] = useState('')
  const [files, setFiles]             = useState([])
  const [previews, setPreviews]       = useState([])
  const [upiOrMobile, setUpiOrMobile] = useState('')
  const [ingredients, setIngredients] = useState('')
  const [uploading, setUploading]     = useState(false)
  const [error, setError]             = useState(null)
  const [dragOver, setDragOver]       = useState(false)
  const inputRef = useRef()

  const remaining = MAX_PHOTOS - files.length

  const addFiles = (selected) => {
    const newFiles = Array.from(selected).filter(f => f.type.startsWith('image/'))
    if (!newFiles.length) return
    const oversized = newFiles.find(f => f.size > MAX_SIZE_MB * 1024 * 1024)
    if (oversized) { setError(`Each image must be under ${MAX_SIZE_MB}MB`); return }
    setError(null)
    const toAdd = newFiles.slice(0, remaining)
    setFiles(prev => [...prev, ...toAdd])
    setPreviews(prev => [...prev, ...toAdd.map(f => URL.createObjectURL(f))])
    if (inputRef.current) inputRef.current.value = ''
  }

  const removeFile = (i) => {
    URL.revokeObjectURL(previews[i])
    setFiles(f => f.filter((_, j) => j !== i))
    setPreviews(p => p.filter((_, j) => j !== i))
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    addFiles(e.dataTransfer.files)
  }

  const handleSubmit = async () => {
    const name = productName.trim()
    const upi  = upiOrMobile.trim()

    if (!name)         { setError('Product name is required'); return }
    if (!files.length) { setError('At least one product image is required'); return }
    if (!upi)          { setError('UPI ID or mobile number is required'); return }

    setUploading(true)
    setError(null)

    try {
      // Upload all images and collect public URLs
      const uploadedUrls = []
      for (const file of files) {
        const ext  = file.name.split('.').pop()?.toLowerCase() || 'jpg'
        const path = `new-submissions/${user.id}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
        const { error: upErr } = await supabase.storage
          .from('product-images')
          .upload(path, file, { contentType: file.type, upsert: false })
        if (upErr) throw new Error(`Image upload failed: ${upErr.message}`)
        const { data: { publicUrl } } = supabase.storage.from('product-images').getPublicUrl(path)
        uploadedUrls.push(publicUrl)
      }

      const { error: dbErr } = await supabase.from('product_submissions').insert({
        product_name_searched: name,
        images:                uploadedUrls,
        contact:               upi,
        email:                 user.email || null,
        ingredients_raw:       ingredients.trim() || null,
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

  const canSubmit = productName.trim() && files.length > 0 && upiOrMobile.trim() && !uploading

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

          {/* How it works */}
          <div style={{ marginBottom: 16, padding: '10px 14px', background: '#f0f9ff', border: '1px solid #bae6fd', borderRadius: 10, fontSize: 12, color: '#0369a1' }}>
            <strong>How it works:</strong> Submit the product name and at least one photo of the packaging.
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

          {/* Product Images */}
          <div style={{ marginBottom: 14 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 6 }}>
              Product Photos <span style={{ color: '#dc2626' }}>*</span>
              <span style={{ fontSize: 11, fontWeight: 400, color: '#9ca3af', marginLeft: 6 }}>
                min 1 · max {MAX_PHOTOS} · {files.length}/{MAX_PHOTOS} added
              </span>
            </label>

            {/* Drop zone — hide once 5 photos added */}
            {remaining > 0 && (
              <div
                onClick={() => inputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                style={{
                  border: `2px dashed ${dragOver ? '#FF9933' : '#e5e7eb'}`,
                  borderRadius: 12, padding: '16px', textAlign: 'center', cursor: 'pointer',
                  background: dragOver ? '#fff7ed' : '#fafafa', transition: 'all 0.15s', marginBottom: 10,
                }}
              >
                <div style={{ fontSize: 26, marginBottom: 4 }}>📷</div>
                <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#374151' }}>
                  {files.length === 0 ? 'Click to upload or drag & drop' : `Add more photos (${remaining} slot${remaining !== 1 ? 's' : ''} left)`}
                </p>
                <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>JPG, PNG, WEBP · max {MAX_SIZE_MB}MB each</p>
              </div>
            )}
            <input ref={inputRef} type="file" accept="image/*" multiple style={{ display: 'none' }} onChange={e => addFiles(e.target.files)} />

            {/* Thumbnails */}
            {previews.length > 0 && (
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {previews.map((src, i) => (
                  <div key={i} style={{ position: 'relative', width: 76, height: 76, borderRadius: 10, overflow: 'hidden', border: `1.5px solid ${i === 0 ? '#86efac' : i === 1 ? '#93c5fd' : '#e5e7eb'}`, background: '#f9fafb', flexShrink: 0 }}>
                    <img src={src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, background: 'rgba(0,0,0,0.5)', color: '#fff', fontSize: 9, textAlign: 'center', padding: '2px 0', fontWeight: 700 }}>
                      {LABELS[i]}
                    </div>
                    <button onClick={() => removeFile(i)}
                      style={{ position: 'absolute', top: 3, right: 3, width: 18, height: 18, borderRadius: '50%', background: 'rgba(0,0,0,0.65)', border: 'none', color: '#fff', fontSize: 11, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1 }}>×</button>
                  </div>
                ))}
              </div>
            )}
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
            {uploading
              ? `Uploading ${files.length} photo${files.length !== 1 ? 's' : ''}…`
              : 'Submit for Review · Earn ₹1'}
          </button>
        </div>
      </div>
    </div>
  )
}
