import { useState, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'
const MAX_SIZE_MB = 8
const MIN_PHOTOS = 2

export default function PhotoUploadModal({ productId, productName, currentCount, user, onClose, onSuccess }) {
  const [files, setFiles] = useState([])
  const [previews, setPreviews] = useState([])
  const [upiOrMobile, setUpiOrMobile] = useState('')
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const inputRef = useRef()

  const isAdmin = user?.email === ADMIN_EMAIL
  const remaining = Math.max(0, 5 - currentCount)

  const addFiles = (selected) => {
    const newArr = Array.from(selected).filter(f => f.type.startsWith('image/'))
    if (!newArr.length) return
    const oversized = newArr.filter(f => f.size > MAX_SIZE_MB * 1024 * 1024)
    if (oversized.length) { setError(`Each image must be under ${MAX_SIZE_MB}MB`); return }
    setError(null)
    // Append to existing, cap at remaining slots
    setFiles(prev => [...prev, ...newArr].slice(0, remaining))
    setPreviews(prev => [...prev, ...newArr.map(f => URL.createObjectURL(f))].slice(0, remaining))
    // Reset input so the same file can be picked again
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

  const handleUpload = async () => {
    if (!files.length || !user) return

    if (!isAdmin && files.length < MIN_PHOTOS) {
      setError(`Please upload at least ${MIN_PHOTOS} photos (front and back of product)`)
      return
    }
    if (!isAdmin && !upiOrMobile.trim()) {
      setError('Please enter your UPI ID or mobile number to receive payment')
      return
    }

    setUploading(true)
    setError(null)

    try {
      const uploadedUrls = []
      for (const file of files) {
        const ext = file.name.split('.').pop()?.toLowerCase() || 'jpg'
        const path = `${productId}/${Date.now()}_${Math.random().toString(36).slice(2)}.${ext}`
        const { error: upErr } = await supabase.storage
          .from('product-images')
          .upload(path, file, { contentType: file.type, upsert: false })
        if (upErr) throw new Error(`Upload failed: ${upErr.message}`)
        const { data: { publicUrl } } = supabase.storage.from('product-images').getPublicUrl(path)
        uploadedUrls.push({ url: publicUrl, path })
      }

      if (isAdmin) {
        const { error: dbErr } = await supabase.from('product_photos').insert(
          uploadedUrls.map(({ url, path }) => ({
            product_id: productId,
            image_url: url,
            storage_path: path,
            added_by: user.id,
            is_admin_added: true,
          }))
        )
        if (dbErr) throw new Error(dbErr.message)
        // Update the primary image_url so Products browse page reflects the new photo
        await supabase
          .from('ai_extracted_products')
          .update({ image_url: uploadedUrls[0].url })
          .eq('id', productId)
        onSuccess(`${uploadedUrls.length} photo(s) added to product.`, true, uploadedUrls[0].url)
      } else {
        const { error: dbErr } = await supabase.from('product_photo_submissions').insert({
          product_id: productId,
          product_name: productName,
          user_id: user.id,
          image_urls: uploadedUrls.map(u => u.url),
          upi_or_mobile: upiOrMobile.trim(),
          status: 'pending',
        })
        if (dbErr) throw new Error(dbErr.message)
        onSuccess('Submitted! You will earn ₹1 after admin approves your photos.', false)
      }
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  const canSubmit = isAdmin ? files.length > 0 : files.length >= MIN_PHOTOS && upiOrMobile.trim()

  return (
    <div
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}
      onClick={e => e.target === e.currentTarget && onClose()}
    >
      <div style={{ background: '#fff', borderRadius: 20, width: '100%', maxWidth: 460, maxHeight: '90vh', overflowY: 'auto', boxShadow: '0 20px 60px rgba(0,0,0,0.25)' }}>

        {/* Header */}
        <div style={{ padding: '18px 20px 14px', borderBottom: '1px solid #f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'space-between', position: 'sticky', top: 0, background: '#fff', zIndex: 1 }}>
          <div>
            <h3 style={{ margin: 0, fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827' }}>
              {isAdmin ? '📸 Add Product Photos' : '📸 Suggest a Product Image'}
            </h3>
            <p style={{ margin: '3px 0 0', fontSize: 12, color: '#9ca3af' }}>
              {isAdmin ? `Direct add · up to ${remaining} more (max 5 total)` : 'Upload front & back · earn ₹1 on approval'}
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: 22, color: '#9ca3af', cursor: 'pointer', lineHeight: 1, padding: 4 }}>×</button>
        </div>

        <div style={{ padding: '16px 20px 20px' }}>
          {remaining === 0 ? (
            <div style={{ textAlign: 'center', padding: '24px 0', color: '#6b7280', fontSize: 14 }}>
              This product already has the maximum 5 photos.
            </div>
          ) : (
            <>
              {/* Instructions for users */}
              {!isAdmin && (
                <div style={{ marginBottom: 14, padding: '10px 14px', background: '#f0f9ff', border: '1px solid #bae6fd', borderRadius: 10, fontSize: 12, color: '#0369a1' }}>
                  <strong>How it works:</strong> Upload the front and back of the product packaging.
                  Admin will review and credit <strong>₹1 to your UPI/mobile</strong> within 24 hours.
                </div>
              )}

              {/* Drop zone */}
              <div
                onClick={() => inputRef.current?.click()}
                onDrop={handleDrop}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                style={{
                  border: `2px dashed ${dragOver ? '#FF9933' : '#e5e7eb'}`,
                  borderRadius: 12, padding: '20px 16px', textAlign: 'center', cursor: 'pointer',
                  background: dragOver ? '#fff7ed' : '#fafafa', transition: 'all 0.15s',
                  marginBottom: 12,
                }}
              >
                <div style={{ fontSize: 30, marginBottom: 6 }}>📁</div>
                <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#374151' }}>
                  Click to browse or drag & drop
                </p>
                <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>
                  {isAdmin
                    ? `JPG, PNG, WEBP · max ${MAX_SIZE_MB}MB each`
                    : `Min 2 photos (front + back) · max ${MAX_SIZE_MB}MB each`}
                </p>
                <input
                  ref={inputRef} type="file" multiple accept="image/*"
                  style={{ display: 'none' }}
                  onChange={e => addFiles(e.target.files)}
                />
              </div>

              {/* Previews */}
              {previews.length > 0 && (
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14 }}>
                  {previews.map((src, i) => (
                    <div key={i} style={{ position: 'relative', width: 76, height: 76, borderRadius: 10, overflow: 'hidden', border: `1.5px solid ${i === 0 ? '#86efac' : i === 1 ? '#93c5fd' : '#e5e7eb'}`, background: '#f9fafb' }}>
                      <img src={src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                      <div style={{ position: 'absolute', bottom: 0, left: 0, right: 0, background: 'rgba(0,0,0,0.5)', color: '#fff', fontSize: 9, textAlign: 'center', padding: '2px 0', fontWeight: 700 }}>
                        {i === 0 ? 'FRONT' : i === 1 ? 'BACK' : `IMG ${i + 1}`}
                      </div>
                      <button onClick={() => removeFile(i)}
                        style={{ position: 'absolute', top: 2, right: 2, width: 18, height: 18, borderRadius: '50%', background: 'rgba(0,0,0,0.65)', border: 'none', color: '#fff', fontSize: 11, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1 }}>×</button>
                    </div>
                  ))}
                  {!isAdmin && files.length < MIN_PHOTOS && (
                    <button onClick={() => inputRef.current?.click()} style={{ width: 76, height: 76, borderRadius: 10, border: '2px dashed #fbbf24', background: '#fefce8', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 2, cursor: 'pointer', fontFamily: 'inherit' }}>
                      <span style={{ fontSize: 18 }}>📷</span>
                      <span style={{ fontSize: 9, color: '#92400e', fontWeight: 700 }}>TAP TO ADD</span>
                    </button>
                  )}
                </div>
              )}

              {/* UPI / Mobile for non-admin */}
              {!isAdmin && (
                <div style={{ marginBottom: 12 }}>
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
                  <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>
                    Admin will send ₹1 here after approving your photos
                  </p>
                </div>
              )}

              {error && (
                <div style={{ marginBottom: 12, padding: '9px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, color: '#dc2626', fontWeight: 600 }}>
                  {error}
                </div>
              )}

              {/* Earn badge for users */}
              {!isAdmin && (
                <div style={{ marginBottom: 12, padding: '9px 12px', background: '#fefce8', border: '1px solid #fde68a', borderRadius: 8, fontSize: 12, color: '#92400e', display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 18 }}>💰</span>
                  <span><strong>Earn ₹1 per product</strong> — credited after admin reviews your photos</span>
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!canSubmit || uploading}
                style={{
                  width: '100%', padding: '13px 0',
                  background: canSubmit && !uploading ? (isAdmin ? '#1B3F8A' : '#FF9933') : '#f3f4f6',
                  color: canSubmit && !uploading ? '#fff' : '#9ca3af',
                  border: 'none', borderRadius: 12, fontSize: 14, fontWeight: 700,
                  cursor: canSubmit && !uploading ? 'pointer' : 'not-allowed',
                  fontFamily: 'inherit', transition: 'background 0.15s',
                }}
              >
                {uploading
                  ? 'Uploading…'
                  : isAdmin
                    ? `Add ${files.length || 0} Photo(s)`
                    : files.length < MIN_PHOTOS
                      ? `Add ${MIN_PHOTOS - files.length} more photo(s) required`
                      : 'Submit for Review · Earn ₹1'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
