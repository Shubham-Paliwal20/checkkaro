import { useState, useRef } from 'react'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'
const MAX_SIZE_MB = 8

export default function PhotoUploadModal({ productId, productName, currentCount, user, onClose, onSuccess }) {
  const [files, setFiles] = useState([])
  const [previews, setPreviews] = useState([])
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const inputRef = useRef()

  const isAdmin = user?.email === ADMIN_EMAIL
  const remaining = Math.max(0, 5 - currentCount)

  const addFiles = (selected) => {
    const arr = Array.from(selected)
      .filter(f => f.type.startsWith('image/'))
      .slice(0, remaining)
    if (!arr.length) return
    const oversized = arr.filter(f => f.size > MAX_SIZE_MB * 1024 * 1024)
    if (oversized.length) { setError(`Each image must be under ${MAX_SIZE_MB}MB`); return }
    setError(null)
    setFiles(arr)
    setPreviews(arr.map(f => URL.createObjectURL(f)))
  }

  const removeFile = (i) => {
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
        onSuccess(`${uploadedUrls.length} photo(s) added to product.`, true)
      } else {
        const { error: dbErr } = await supabase.from('product_photo_submissions').insert({
          product_id: productId,
          product_name: productName,
          user_id: user.id,
          image_urls: uploadedUrls.map(u => u.url),
          status: 'pending',
        })
        if (dbErr) throw new Error(dbErr.message)
        onSuccess(`Photo submitted! You'll earn ₹${uploadedUrls.length} after admin approval.`, false)
      }
      onClose()
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div
      style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.55)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px' }}
      onClick={e => e.target === e.currentTarget && onClose()}
    >
      <div style={{ background: '#fff', borderRadius: 20, width: '100%', maxWidth: 460, overflow: 'hidden', boxShadow: '0 20px 60px rgba(0,0,0,0.25)' }}>
        {/* Header */}
        <div style={{ padding: '18px 20px 14px', borderBottom: '1px solid #f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ margin: 0, fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827' }}>
              {isAdmin ? '📸 Add Product Photos' : '📸 Suggest a Photo'}
            </h3>
            <p style={{ margin: '3px 0 0', fontSize: 12, color: '#9ca3af' }}>
              {isAdmin
                ? `Direct add · up to ${remaining} more (max 5 total)`
                : `Earn ₹1 per approved photo · up to ${remaining} more`}
            </p>
          </div>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: 20, color: '#9ca3af', cursor: 'pointer', lineHeight: 1, padding: 4 }}>×</button>
        </div>

        <div style={{ padding: '16px 20px 20px' }}>
          {remaining === 0 ? (
            <div style={{ textAlign: 'center', padding: '24px 0', color: '#6b7280', fontSize: 14 }}>
              This product already has the maximum 5 photos.
            </div>
          ) : (
            <>
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
                  marginBottom: previews.length ? 12 : 0,
                }}
              >
                <div style={{ fontSize: 28, marginBottom: 6 }}>📁</div>
                <p style={{ margin: 0, fontSize: 13, fontWeight: 600, color: '#374151' }}>
                  Click to browse or drag & drop
                </p>
                <p style={{ margin: '4px 0 0', fontSize: 11, color: '#9ca3af' }}>
                  JPG, PNG, WEBP · max {MAX_SIZE_MB}MB each · up to {remaining} photo{remaining !== 1 ? 's' : ''}
                </p>
                <input
                  ref={inputRef} type="file" multiple accept="image/*"
                  style={{ display: 'none' }}
                  onChange={e => addFiles(e.target.files)}
                />
              </div>

              {/* Previews */}
              {previews.length > 0 && (
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
                  {previews.map((src, i) => (
                    <div key={i} style={{ position: 'relative', width: 72, height: 72, borderRadius: 10, overflow: 'hidden', border: '1.5px solid #e5e7eb', background: '#f9fafb' }}>
                      <img src={src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                      <button
                        onClick={() => removeFile(i)}
                        style={{ position: 'absolute', top: 2, right: 2, width: 18, height: 18, borderRadius: '50%', background: 'rgba(0,0,0,0.6)', border: 'none', color: '#fff', fontSize: 11, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1 }}
                      >×</button>
                    </div>
                  ))}
                </div>
              )}

              {error && (
                <div style={{ marginBottom: 10, padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, color: '#dc2626', fontWeight: 600 }}>
                  {error}
                </div>
              )}

              {!isAdmin && (
                <div style={{ marginBottom: 12, padding: '10px 12px', background: '#fefce8', border: '1px solid #fde68a', borderRadius: 8, fontSize: 12, color: '#92400e' }}>
                  💰 <strong>Earn ₹{files.length || 1} per photo</strong> after admin approves your submission.
                </div>
              )}

              <button
                onClick={handleUpload}
                disabled={!files.length || uploading}
                style={{
                  width: '100%', padding: '13px 0',
                  background: files.length && !uploading ? (isAdmin ? '#1B3F8A' : '#FF9933') : '#f3f4f6',
                  color: files.length && !uploading ? '#fff' : '#9ca3af',
                  border: 'none', borderRadius: 12, fontSize: 14, fontWeight: 700,
                  cursor: files.length && !uploading ? 'pointer' : 'not-allowed',
                  fontFamily: 'inherit', transition: 'background 0.15s',
                }}
              >
                {uploading ? 'Uploading…' : isAdmin ? `Add ${files.length || 0} Photo(s)` : `Submit ${files.length || 0} Photo(s) for Review`}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
