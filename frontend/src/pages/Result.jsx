import { useState, useEffect, useRef, useMemo } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import axios from 'axios'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'
import PhotoUploadModal from '../components/PhotoUploadModal'
import GradeBadge from '../components/GradeBadge'
import DisclaimerBox from '../components/DisclaimerBox'
import ProductReviews from '../components/ProductReviews'
import ProductNotFound from '../components/ProductNotFound'
import SEO from '../components/SEO'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'

const PREVIEW_LEN = 140
function ExpandableNote({ text, className = 'text-xs text-gray-600 mt-1' }) {
  const [expanded, setExpanded] = useState(false)
  if (!text) return null
  if (text.length <= PREVIEW_LEN) return <p className={className}>{text}</p>
  return (
    <div className="mt-1">
      <p className={className}>{expanded ? text : text.slice(0, PREVIEW_LEN) + '…'}</p>
      <button
        className="text-xs text-blue-500 hover:text-blue-700 mt-0.5 font-medium"
        onClick={e => { e.stopPropagation(); setExpanded(v => !v) }}
      >
        {expanded ? 'Read less' : 'Read more'}
      </button>
    </div>
  )
}

// Module-level cache — navigating back to a product is instant, no refetch
const _productCache = new Map()  // productName.lower → { data, ts }
const CACHE_MAX = 40
const CACHE_TTL_MS = 10 * 60 * 1000  // 10 min — matches Render's ~15min idle window
function cacheSet(key, value) {
  if (_productCache.size >= CACHE_MAX && !_productCache.has(key)) {
    _productCache.delete(_productCache.keys().next().value)
  }
  _productCache.set(key, { data: value, ts: Date.now() })
}
function cacheGet(key) {
  const entry = _productCache.get(key)
  if (!entry) return null
  if (Date.now() - entry.ts > CACHE_TTL_MS) { _productCache.delete(key); return null }
  return entry.data
}

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'

// Parse comma-separated ingredient text respecting parentheses depth
// Group-label pattern: "raising agents (INS 503(ii), INS 500(ii))" etc.
const _GROUP_LABEL_RE = /^(raising agents?|emulsifiers?|stabilisers?|stabilizers?|acidity regulators?|anti[- ]?caking agents?|permitted (?:synthetic )?food colou?rs?|colou?ring agents?|artificial colou?rs?|colou?rs?|preservatives?|antioxidants?|flavou?ring agents?|flavou?rings?|sequestrants?|thickeners?|humectants?|glazing agents?|modified starches?|food starches?)\s*\((.+)\)$/i

function _splitInner(inner) {
  const parts = []; let cur = '', d = 0
  for (const ch of inner) {
    if (ch === '(') d++
    else if (ch === ')') d--
    if (ch === ',' && d === 0) { if (cur.trim()) parts.push(cur.trim()); cur = '' }
    else cur += ch
  }
  if (cur.trim()) parts.push(cur.trim())
  return parts
}

function parseRawIngredients(raw) {
  // Step 1: split by commas at depth 0 (skip commas inside parentheses)
  const items = []
  let current = '', depth = 0
  for (const ch of raw) {
    if (ch === '(') depth++
    else if (ch === ')') depth--
    else if (ch === ',' && depth === 0) {
      const t = current.trim()
      if (t) items.push(t)
      current = ''
      continue
    }
    current += ch
  }
  const last = current.trim()
  if (last) items.push(last)

  // Step 2: expand grouped additive declarations
  const results = []
  for (const item of items) {
    const m = item.match(_GROUP_LABEL_RE)
    if (m) {
      const label = m[1], inner = m[2]
      const parts = _splitInner(inner)
      if (parts.length > 1) {
        const short = label.replace(/\b(permitted|synthetic|food|artificial)\b\s*/gi, '').replace(/s$/i, '').trim()
        parts.forEach(p => results.push(`${short} ${p}`))
        continue
      }
    }
    results.push(item)
  }
  return results
}

const UNDISCLOSED_INGREDIENT_RULES = [
  // ── Commonly Questioned ──────────────────────────────────────────────────
  {
    classification: 'commonly_questioned',
    match: /^(fragrance|parfum|perfume|cologne)$/i,
    note: 'Not fully disclosed — "Fragrance" is a legal catch-all that can conceal dozens of individual chemicals, some of which are known allergens, endocrine disruptors, or irritants. Brands are not required to name them individually.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(colour?s?|artificial\s*colour?s?|permitted\s*colour?s?|synthetic\s*colour?s?|fd&?c\s*colou?r)$/i,
    note: 'Not fully disclosed — the specific colorant names are hidden under a generic term. Several synthetic dyes are restricted or banned in some countries due to links with allergic reactions and hyperactivity.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(preservatives?|permitted\s*preservatives?)$/i,
    note: 'Not fully disclosed — the exact preservative chemicals are not named. Common undisclosed preservatives such as parabens, formaldehyde-releasers, and MIT are associated with hormone disruption and skin sensitisation.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(emulsifiers?|permitted\s*emulsifiers?)$/i,
    note: 'Not fully disclosed — the specific emulsifying agents are not named. Some emulsifiers are linked to gut microbiome disruption and digestive sensitivity at regular consumption levels.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(stabilizers?|stabilisers?|permitted\s*stabilizers?)$/i,
    note: 'Not fully disclosed — the exact stabilizing compounds are not named. Certain stabilizers used in processed foods and cosmetics have raised concerns around long-term safety.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(artificial\s*)?flavou?r(ing)?s?$/i,
    note: 'Not fully disclosed — flavoring compounds are grouped under one term. May include synthetic chemicals not individually disclosed, some of which are under ongoing regulatory review.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(added\s*)?flavou?rs?$/i,
    note: 'Not fully disclosed — the exact flavoring compounds are not listed individually by the brand.',
  },
  {
    classification: 'commonly_questioned',
    match: /^(natural\s*flavou?r(ing)?s?)$/i,
    note: 'Not fully disclosed — "natural flavour" can include a wide range of undisclosed aromatic or taste compounds, some of which may be processed with synthetic solvents.',
  },

  // ── Worth Knowing ────────────────────────────────────────────────────────
  {
    classification: 'worth_knowing',
    match: /^natural\s*fragrance$/i,
    note: 'Not fully disclosed — even "natural fragrance" can contain undisclosed aromatic compounds and synthetic carriers not individually listed on the label.',
  },
  {
    classification: 'worth_knowing',
    match: /^(sugandhit\s*dravya|sughandi\s*dravya|sugandhi\s*dravya|sugandhit\s*padarthi?)$/i,
    note: 'Not fully disclosed by brand — Hindi term meaning "fragrant substances". The individual aromatic compounds are not listed separately on the label.',
  },
  {
    classification: 'worth_knowing',
    match: /^excipients?$/i,
    note: 'Not fully disclosed by brand — a blanket pharmaceutical/cosmetic term for inactive filler ingredients. The specific compounds used are not listed individually.',
  },
  {
    classification: 'worth_knowing',
    match: /^(herbal\s*extracts?|plant\s*extracts?|botanical\s*extracts?|ayurvedic\s*extracts?|jadi\s*buti)$/i,
    note: 'Not fully disclosed — a collective term. The individual herbs or botanicals and their concentrations are not specified by the brand.',
  },
  {
    classification: 'worth_knowing',
    match: /^(proprietary\s*blend|herbal\s*blend|essential\s*oil\s*blend|active\s*blend)$/i,
    note: 'Not fully disclosed — a brand proprietary formulation. Individual components and concentrations are intentionally not revealed.',
  },
  {
    classification: 'worth_knowing',
    match: /^(other\s*ingredients?|misc\.?|q\.?\s*s\.?)$/i,
    note: 'Not fully disclosed — a generic placeholder. The actual ingredients hidden behind this term are not identified.',
  },
]

// Client-side reclassification overrides — applied to any product loaded from DB.
// Add entries here whenever the backend ingredient_database.py classification changes
// so stored products get corrected without needing a full DB re-save.
const CLASSIFICATION_OVERRIDES = [
  // pattern (case-insensitive substring match on ingredient name) → corrected classification
  { pattern: /disodium\s+5['-]?\s*ribonucleotides/i, classification: 'worth_knowing' },
  { pattern: /\be635\b/i,                              classification: 'worth_knowing' },
  { pattern: /tbhq|tertiary\s+butylhydroquinone/i,     classification: 'commonly_questioned' },
  { pattern: /titanium\s+dioxide|\be171\b/i,           classification: 'commonly_questioned' },
  { pattern: /potassium\s+nitrite|\be249\b/i,          classification: 'commonly_questioned' },
  { pattern: /amaranth\s+dye|\be123\b/i,               classification: 'commonly_questioned' },
  // EU-banned fragrance (CMR 1B reproductive toxicant — banned March 2022)
  { pattern: /butylphenyl\s*methylpropional|lilial/i,  classification: 'commonly_questioned' },
  // Antiseptic — anaphylaxis risk, EU restricted; ototoxic in ears
  { pattern: /chlorhexidine/i,                         classification: 'commonly_questioned' },
  // EU mandatory 26 fragrance allergens
  { pattern: /\blimonene\b/i,                          classification: 'worth_knowing' },
  { pattern: /\blinalool\b/i,                          classification: 'worth_knowing' },
  { pattern: /benzyl\s+salicylate/i,                   classification: 'worth_knowing' },
  { pattern: /hexyl\s+cinnamal/i,                      classification: 'worth_knowing' },
  { pattern: /\beugenol\b/i,                           classification: 'worth_knowing' },
  { pattern: /\bgeraniol\b/i,                          classification: 'worth_knowing' },
  { pattern: /\bcitronellol\b/i,                       classification: 'worth_knowing' },
  { pattern: /\bcoumarin\b/i,                          classification: 'worth_knowing' },
  { pattern: /\bisoeugenol\b/i,                        classification: 'worth_knowing' },
  { pattern: /cinnamyl\s+alcohol/i,                    classification: 'worth_knowing' },
  { pattern: /\bcinnamal\b/i,                          classification: 'worth_knowing' },
  { pattern: /\bfarnesol\b/i,                          classification: 'worth_knowing' },
  { pattern: /hydroxycitronellal/i,                    classification: 'worth_knowing' },
  { pattern: /benzyl\s+cinnamate/i,                    classification: 'worth_knowing' },
  { pattern: /benzyl\s+benzoate/i,                     classification: 'worth_knowing' },
  { pattern: /alpha.isomethyl\s+ionone/i,              classification: 'worth_knowing' },
  // Quaternary ammonium conditioners — EU concentration-restricted
  { pattern: /behentrimonium\s+chloride/i,             classification: 'worth_knowing' },
  { pattern: /cetrimonium\s+chloride/i,                classification: 'worth_knowing' },
  { pattern: /quaternium-33/i,                         classification: 'worth_knowing' },
  // Ethoxylated surfactant — trace 1,4-dioxane risk
  { pattern: /\btrideceth/i,                           classification: 'worth_knowing' },
  // IPA — skin barrier disruptor with repeated use
  { pattern: /isopropyl\s+alcohol|isopropanol/i,       classification: 'worth_knowing' },
  // Cosmetic preservative — safe at <1%; worth noting
  { pattern: /\bphenoxyethanol\b/i,                    classification: 'worth_knowing' },
]

function enrichIngredients(ingredients) {
  return ingredients.map(ing => {
    const trimmed = (ing.name || '').trim()

    // Apply reclassification overrides for ingredients whose DB classification is outdated.
    for (const { pattern, classification } of CLASSIFICATION_OVERRIDES) {
      if (pattern.test(trimmed)) {
        return { ...ing, classification }
      }
    }

    // Only apply undisclosed rules if the DB has no specific regulatory data for this ingredient.
    // A non-empty regulatory_note means the AI already analyzed it — trust that over our generic rules.
    const hasSpecificData = ing.regulatory_note && ing.regulatory_note.trim().length > 0
    if (!hasSpecificData) {
      for (const { match, classification, note } of UNDISCLOSED_INGREDIENT_RULES) {
        if (match.test(trimmed)) {
          return { ...ing, classification, one_line_note: note }
        }
      }
    }

    // Fix DB inconsistencies: if the note says "generally recognised" but the classification
    // is something stricter, the AI note is the accurate source — fix the classification.
    if (
      ing.classification !== 'generally_recognised' &&
      ing.one_line_note &&
      /generally\s*recogni[sz]ed|generally\s*recogni[sz]ed as safe/i.test(ing.one_line_note)
    ) {
      return { ...ing, classification: 'generally_recognised' }
    }

    return ing
  })
}

function ProductImageGallery({ imageUrl, images, name, dbPhotos, onDeleteDbPhoto, onDeleteBackendImage, isAdmin, user, onOpenUpload, onNeedLogin }) {
  const backendImgs = (images && images.length > 0) ? images : (imageUrl ? [imageUrl] : [])
  const dbImgUrls = (dbPhotos || []).map(p => p.image_url)

  // Merge, deduplicate
  const seen = new Set()
  const allImgs = [...backendImgs, ...dbImgUrls].filter(u => {
    if (!u || seen.has(u)) return false
    seen.add(u); return true
  })

  const [idx, setIdx] = useState(0)
  const touchStartX = useRef(null)

  useEffect(() => { if (idx >= allImgs.length && allImgs.length > 0) setIdx(allImgs.length - 1) }, [allImgs.length])

  const prev = () => setIdx(i => (i - 1 + allImgs.length) % allImgs.length)
  const next = () => setIdx(i => (i + 1) % allImgs.length)
  const onTouchStart = e => { touchStartX.current = e.touches[0].clientX }
  const onTouchEnd = e => {
    if (touchStartX.current === null) return
    const dx = e.changedTouches[0].clientX - touchStartX.current
    if (Math.abs(dx) > 40) { dx < 0 ? next() : prev() }
    touchStartX.current = null
  }

  // Find if current image is a db photo (deletable by admin)
  const currentDbPhoto = (dbPhotos || []).find(p => p.image_url === allImgs[idx])

  const noImage = allImgs.length === 0

  return (
    <div className="w-full md:w-64 flex-shrink-0 mx-auto md:mx-0" style={{ userSelect: 'none' }}>
      {/* Main image area */}
      <div className="relative rounded-xl overflow-hidden bg-gray-50"
        style={{ height: 240 }}
        onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
        {noImage ? (
          <div style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
            <svg className="w-16 h-16 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
            <span style={{ fontSize: 11, color: '#9ca3af' }}>No image yet</span>
          </div>
        ) : (
          <img
            src={allImgs[idx]}
            alt={name}
            className="w-full h-full object-contain p-3"
            fetchpriority="high"
            decoding="async"
            onError={e => { e.target.style.display = 'none' }}
          />
        )}

        {/* Navigation arrows */}
        {allImgs.length > 1 && (
          <>
            <button onClick={prev} className="absolute left-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full flex items-center justify-center text-white text-lg font-bold"
              style={{ background: 'rgba(0,0,0,0.4)', border: 'none', cursor: 'pointer' }}>‹</button>
            <button onClick={next} className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full flex items-center justify-center text-white text-lg font-bold"
              style={{ background: 'rgba(0,0,0,0.4)', border: 'none', cursor: 'pointer' }}>›</button>
            <span className="absolute top-2 right-2 text-white text-xs font-bold px-2 py-1 rounded-md"
              style={{ background: 'rgba(0,0,0,0.45)' }}>{idx + 1}/{allImgs.length}</span>
          </>
        )}

        {/* Admin: delete current image */}
        {isAdmin && currentDbPhoto && (
          <button
            onClick={() => window.confirm('Delete this uploaded photo?') && onDeleteDbPhoto(currentDbPhoto.id)}
            title="Delete this photo"
            style={{ position: 'absolute', bottom: 8, right: 8, background: '#dc2626', border: 'none', color: '#fff', borderRadius: 8, padding: '5px 10px', fontSize: 12, fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4 }}>
            🗑 Delete
          </button>
        )}
        {isAdmin && !currentDbPhoto && allImgs[idx] && (
          <button
            onClick={() => window.confirm('Delete this product image? This cannot be undone.') && onDeleteBackendImage(allImgs[idx])}
            title="Delete this photo"
            style={{ position: 'absolute', bottom: 8, right: 8, background: '#dc2626', border: 'none', color: '#fff', borderRadius: 8, padding: '5px 10px', fontSize: 12, fontWeight: 700, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 4 }}>
            🗑 Delete
          </button>
        )}

        {/* Admin badge */}
        {isAdmin && (
          <span style={{ position: 'absolute', top: 8, left: 8, background: '#1B3F8A', color: '#fff', fontSize: 10, fontWeight: 700, padding: '3px 7px', borderRadius: 6 }}>
            ADMIN
          </span>
        )}
      </div>

      {/* Thumbnails row */}
      <div className="flex gap-2 mt-2 overflow-x-auto pb-1" style={{ WebkitOverflowScrolling: 'touch' }}>
        {allImgs.map((src, i) => {
          const isDb = (dbPhotos || []).some(p => p.image_url === src)
          return (
            <div key={i} style={{ position: 'relative', flexShrink: 0 }}>
              <button onClick={() => setIdx(i)}
                style={{
                  width: 52, height: 52, borderRadius: 10, overflow: 'hidden', display: 'block',
                  border: i === idx ? '2.5px solid #FF9933' : '2px solid #e5e7eb',
                  background: '#f9fafb', padding: 0, cursor: 'pointer',
                }}>
                <img src={src} alt="" loading="lazy" decoding="async" style={{ width: '100%', height: '100%', objectFit: 'contain', padding: 3 }} />
              </button>
              {/* Admin: delete badge on thumbnail */}
              {isAdmin && isDb && (
                <button
                  onClick={() => window.confirm('Delete this photo?') && onDeleteDbPhoto((dbPhotos || []).find(p => p.image_url === src)?.id)}
                  title="Delete"
                  style={{ position: 'absolute', top: -5, right: -5, width: 16, height: 16, borderRadius: '50%', background: '#dc2626', border: '1.5px solid #fff', color: '#fff', fontSize: 10, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1, padding: 0 }}>×</button>
              )}
              {isAdmin && !isDb && (
                <button
                  onClick={() => window.confirm('Delete this image? Cannot be undone.') && onDeleteBackendImage(src)}
                  title="Delete"
                  style={{ position: 'absolute', top: -5, right: -5, width: 16, height: 16, borderRadius: '50%', background: '#dc2626', border: '1.5px solid #fff', color: '#fff', fontSize: 10, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1, padding: 0 }}>×</button>
              )}
            </div>
          )
        })}

        {/* Admin: + add button */}
        {isAdmin && allImgs.length < 5 && (
          <button
            onClick={onOpenUpload}
            title="Add photo"
            style={{ flexShrink: 0, width: 52, height: 52, borderRadius: 10, border: '2px dashed #1B3F8A', background: '#eff6ff', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22, color: '#1B3F8A' }}>+</button>
        )}
      </div>

      {/* Suggest photo — only when product has NO images at all, visible to everyone */}
      {!isAdmin && noImage && (
        <button
          onClick={user ? onOpenUpload : onNeedLogin}
          style={{ width: '100%', marginTop: 8, padding: '9px 0', background: '#fff7ed', border: '1.5px solid #fed7aa', borderRadius: 10, color: '#c2410c', fontSize: 12, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }}>
          📸 Suggest a product image · earn ₹1
        </button>
      )}
    </div>
  )
}

function Result() {
  const { productName } = useParams()
  const navigate = useNavigate()
  const { user, openAuthModal } = useAuth()
  const [loading,          setLoading]          = useState(true)
  const [error,            setError]            = useState(null)
  const [productNotFound,  setProductNotFound]  = useState(false)
  const [product,          setProduct]          = useState(null)
  const [showCorrectionForm, setShowCorrectionForm] = useState(false)
  const [correctionText, setCorrectionText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [dbPhotos, setDbPhotos] = useState([])
  const [showReportForm, setShowReportForm] = useState(false)
  const [reportText, setReportText] = useState('')
  const [reportReason, setReportReason] = useState('')
  const [reportSubmitting, setReportSubmitting] = useState(false)
  const [reportSuccess, setReportSuccess] = useState(false)
  const [adminEditMode, setAdminEditMode] = useState(false)
  const [adminIngText, setAdminIngText] = useState('')
  const [adminSaving, setAdminSaving] = useState(false)
  const [adminDbId, setAdminDbId] = useState(null) // cached Supabase UUID for static products
  const [adminNameEdit, setAdminNameEdit] = useState(false)
  const [adminNameText, setAdminNameText] = useState('')
  const [adminNameSaving, setAdminNameSaving] = useState(false)
  const [showPhotoModal, setShowPhotoModal] = useState(false)
  const [photoToast, setPhotoToast] = useState(null)

  const isAdmin = user?.email === ADMIN_EMAIL

  useEffect(() => {
    setProductNotFound(false)
    setDbPhotos([])
    setAdminDbId(null)
    fetchProduct()
  }, [productName])

  // Re-fetch when user returns to the tab after a long idle.
  // Render.com free tier spins down after ~15 min — if the user was away longer
  // than the cache TTL, the cached data is already expired so fetchProduct()
  // will hit the network again, warming up the backend automatically.
  useEffect(() => {
    let hiddenAt = 0
    const onVisibility = () => {
      if (document.hidden) {
        hiddenAt = Date.now()
      } else if (hiddenAt > 0 && Date.now() - hiddenAt > CACHE_TTL_MS) {
        // Cache TTL expired while away — re-fetch so stale data isn't shown
        // and the Render dyno is warmed up before the user interacts.
        fetchProduct()
      }
    }
    document.addEventListener('visibilitychange', onVisibility)
    return () => document.removeEventListener('visibilitychange', onVisibility)
  }, [productName])

  const fetchDbPhotos = async (productId, staticKey) => {
    try {
      const API = import.meta.env.VITE_API_BASE_URL || ''
      const ids = [productId, ...(staticKey && staticKey !== productId ? [staticKey] : [])]
      const results = await Promise.all(
        ids.map(id => fetch(`${API}/api/photos/${id}`).then(r => r.json()).catch(() => ({ photos: [] })))
      )
      const seen = new Set()
      const photos = []
      results.forEach(({ photos: list = [] }) => {
        list.forEach(p => { if (!seen.has(p.id)) { seen.add(p.id); photos.push(p) } })
      })
      setDbPhotos(photos)
    } catch { /* silent */ }
  }

  const handleDeletePhoto = async (photoId) => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token
      if (!token) { alert('Session expired. Please log in again.'); return }
      const API = import.meta.env.VITE_API_BASE_URL || ''
      const res = await fetch(`${API}/api/photos/${photoId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      })
      if (res.ok) {
        setDbPhotos(prev => prev.filter(p => p.id !== photoId))
      } else {
        const err = await res.json().catch(() => ({}))
        alert(`Delete failed: ${err.detail || res.status}`)
      }
    } catch (e) {
      console.error('[handleDeletePhoto]', e)
    }
  }

  const handleDeleteBackendImage = async (url) => {
    if (!product?.id) return
    const currentImages = (product.images && product.images.length > 0) ? product.images : (product.image_url ? [product.image_url] : [])
    const newImages = currentImages.filter(u => u !== url)
    const newImageUrl = newImages.length > 0 ? newImages[0] : null
    try {
      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token
      const API = import.meta.env.VITE_API_BASE_URL || ''
      const res = await fetch(`${API}/api/photos/primary`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ product_id: product.id, image_url: newImageUrl, images: newImages.length > 0 ? newImages : null }),
      })
      if (res.ok) {
        const updated = { ...product, image_url: newImageUrl, images: newImages.length > 0 ? newImages : null }
        setProduct(updated)
        cacheSet(productName.toLowerCase(), updated)
      }
    } catch { /* silent */ }
  }

  const handlePhotoSuccess = (msg, isAdminAdd, firstUploadedUrl) => {
    setPhotoToast(msg)
    if (isAdminAdd && product?.id) {
      fetchDbPhotos(product.id, product.static_key)
      // Update local product state + cache so the gallery shows the new primary image immediately
      if (firstUploadedUrl) {
        const updated = { ...product, image_url: firstUploadedUrl }
        setProduct(updated)
        cacheSet(productName.toLowerCase(), updated)
      }
    }
    setTimeout(() => setPhotoToast(null), 4000)
  }

  const totalPhotoCount = useMemo(() => {
    const backendImgs = (product?.images?.length > 0) ? product.images : (product?.image_url ? [product.image_url] : [])
    return [...new Set([...backendImgs, ...dbPhotos.map(p => p.image_url)])].length
  }, [product, dbPhotos])

  // Secondary backend search with a longer timeout (replaces former direct-DB fallback)
  const _supabaseSearch = async (name) => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/product/search`, {
        params: { name },
        timeout: 20000,
      })
      return res.data || null
    } catch {
      return null
    }
  }

  const fetchProduct = async () => {
    try {
      setLoading(true)
      setError(null)

      // ── Cache hit → instant render ───────────────────────────────────────
      const cacheKey = productName.toLowerCase()
      const cached = cacheGet(cacheKey)
      if (cached) {
        setProduct(cached)
        setLoading(false)
        return
      }

      // Try backend — retry once with a longer timeout to handle Render cold starts
      const tryBackend = async (timeout) => axios.get(`${API_BASE_URL}/api/product/search`, {
        params: { name: productName },
        timeout,
      })
      try {
        let response
        try {
          response = await tryBackend(10000)
        } catch (firstErr) {
          // Cold start: timed out or network hiccup — wait briefly then retry
          if (firstErr.code === 'ECONNABORTED' || firstErr.code === 'ERR_NETWORK') {
            await new Promise(r => setTimeout(r, 2000))
            response = await tryBackend(25000)
          } else {
            throw firstErr
          }
        }
        cacheSet(cacheKey, response.data)
        setProduct(response.data)
        // Kick off photo fetch immediately without blocking product display
        if (response.data?.id) fetchDbPhotos(response.data.id, response.data.static_key)

        return
      } catch (backendErr) {
        if (backendErr.response?.status && backendErr.response.status !== 404 && backendErr.response.status !== 500) {
          throw backendErr
        }
      }

      // Supabase direct fallback with multi-strategy search
      const p = await _supabaseSearch(productName)

      if (p) {
        const rawImages = p.images || (p.image_url ? [p.image_url] : [])
        // Prefer stored classified ingredients; only parse raw as last resort
        const ingredients = (p.ingredients && p.ingredients.length > 0)
          ? p.ingredients
          : p.ingredients_raw
            ? parseRawIngredients(p.ingredients_raw).map(name => ({ name, classification: 'generally_recognised', one_line_note: '', regulatory_note: '' }))
            : []
        const productData = {
          id: String(p.id),
          name: p.name,
          brand: p.brand || 'Unknown',
          category: p.category || 'General',
          image_url: p.image_url || null,
          images: rawImages.length > 0 ? rawImages : null,
          grade: p.grade || 'C',
          awareness_score: p.grade === 'A' ? 90 : p.grade === 'B' ? 75 : p.grade === 'D' ? 30 : 55,
          summary: p.summary || '',
          fssai_note: p.fssai_note || '',
          verdict: p.verdict || '',
          recommendation: p.recommendation || '',
          ingredients,
          ingredients_raw: p.ingredients_raw || null,
          data_source: p.static_key ? 'database_verified' : 'community_verified',
          confidence: p.static_key ? 'high' : 'medium',
          is_complete: true,
        }
        cacheSet(cacheKey, productData)
        setProduct(productData)
        if (p.id) fetchDbPhotos(String(p.id), p.static_key)
        return
      }

      // Nothing found anywhere
      setProductNotFound(true)
    } catch (err) {
      if (err.response?.status === 404 || (err.response?.data?.detail || '').toLowerCase().includes('not found')) {
        setProductNotFound(true)
      } else {
        setError(err.response?.data?.detail || 'Failed to fetch product information')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleVerifyCorrect = async () => {
    try {
      await axios.post(`${API_BASE_URL}/api/product/verify`, null, {
        params: { product_name: productName, is_correct: true }
      })
      alert('Thank you for verifying!')
    } catch (err) {
      console.error('Error verifying:', err)
    }
  }

  const handleSubmitCorrection = async () => {
    if (!correctionText.trim()) {
      alert('Please enter the ingredients')
      return
    }

    try {
      setSubmitting(true)
      await axios.post(`${API_BASE_URL}/api/product/correct`, null, {
        params: {
          product_name: productName,
          ingredients: correctionText,
          product_id: product?.id
        }
      })
      alert('Thank you! Your correction has been submitted for review.')
      setShowCorrectionForm(false)
      setCorrectionText('')
    } catch (err) {
      alert('Error submitting correction. Please try again.')
      console.error('Error submitting correction:', err)
    } finally {
      setSubmitting(false)
    }
  }

  // Categorize ingredients — must be before any early returns (Rules of Hooks)
  const { allIngredients, generally_recognised, worth_knowing, commonly_questioned, effectiveGrade } = useMemo(() => {
    const all = enrichIngredients(product?.ingredients || [])
    const gr = all.filter(i => i.classification === 'generally_recognised')
    const wk = all.filter(i => i.classification === 'worth_knowing')
    const cq = all.filter(i => i.classification === 'commonly_questioned')
    const dbGrade = product?.grade || 'C'
    let effectiveGrade = dbGrade
    if (cq.length > 0 && (dbGrade === 'A' || dbGrade === 'B')) effectiveGrade = 'C'
    else if (wk.length > 0 && dbGrade === 'A') effectiveGrade = 'B'
    return { allIngredients: all, generally_recognised: gr, worth_knowing: wk, commonly_questioned: cq, effectiveGrade }
  }, [product?.ingredients, product?.grade])

  // Grade auto-sync removed — grade corrections go through backend admin endpoints now

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary mx-auto mb-4"></div>
          <p className="text-gray-600">Analyzing {productName}...</p>
        </div>
      </div>
    )
  }

  if (productNotFound) {
    return <ProductNotFound productName={productName} />
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md text-center">
          <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
          </svg>
          <h2 className="text-2xl font-poppins font-bold text-navy mb-2">Something went wrong</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button onClick={() => window.history.back()} className="btn-primary">
            Go Back
          </button>
        </div>
      </div>
    )
  }

  if (!product) return null

  const grade = effectiveGrade

  const productSEO = product ? (() => {
    const cqCount = allIngredients.filter(i => i.classification === 'commonly_questioned').length
    const wkCount = allIngredients.filter(i => i.classification === 'worth_knowing').length
    const ingList = allIngredients.slice(0, 8).map(i => i.name).join(', ')
    const desc = `${product.name} by ${product.brand || 'Indian brand'} — Ingredient Grade ${grade}. Contains ${allIngredients.length} ingredients including ${ingList}. ${wkCount > 0 ? `${wkCount} ingredients worth knowing.` : ''} ${cqCount > 0 ? `${cqCount} commonly questioned ingredients.` : ''} Full FSSAI-verified ingredient breakdown.`.trim()
    return {
      title: `${product.name} Ingredients — Is It Safe? Grade ${grade} | Parkho`,
      description: desc.slice(0, 155),
      keywords: `${product.name} ingredients, is ${product.name} safe, ${product.brand || ''} ingredients, ${product.name} food additives, ${product.name} FSSAI, check ${product.name}`,
      canonical: `/result/${encodeURIComponent(productName)}`,
      ogImage: product.image_url || undefined,
      ogType: 'article',
      structuredData: [
        {
          '@context': 'https://schema.org',
          '@type': 'Product',
          name: product.name,
          brand: { '@type': 'Brand', name: product.brand || 'Unknown' },
          description: product.summary || product.verdict || desc,
          image: product.image_url || undefined,
          category: product.category,
          url: `https://www.parkho.in/result/${encodeURIComponent(productName)}`,
          additionalProperty: [
            { '@type': 'PropertyValue', name: 'Ingredient Grade', value: grade },
            { '@type': 'PropertyValue', name: 'Total Ingredients', value: String(allIngredients.length) },
            { '@type': 'PropertyValue', name: 'Commonly Questioned', value: String(cqCount) },
            { '@type': 'PropertyValue', name: 'FSSAI Verified', value: 'Yes' },
          ],
        },
        {
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: [
            { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://www.parkho.in' },
            { '@type': 'ListItem', position: 2, name: 'Products', item: 'https://www.parkho.in/products' },
            { '@type': 'ListItem', position: 3, name: product.name, item: `https://www.parkho.in/result/${encodeURIComponent(productName)}` },
          ],
        },
      ],
    }
  })() : null

  return (
    <>
      {productSEO && <SEO {...productSEO} />}

      {showPhotoModal && product && (
        <PhotoUploadModal
          productId={product.id}
          productName={product.name}
          currentCount={totalPhotoCount}
          user={user}
          onClose={() => setShowPhotoModal(false)}
          onSuccess={handlePhotoSuccess}
        />
      )}

      {photoToast && (
        <div style={{ position: 'fixed', bottom: 24, left: '50%', transform: 'translateX(-50%)', zIndex: 999, background: '#111827', color: '#fff', padding: '12px 20px', borderRadius: 12, fontSize: 13, fontWeight: 600, boxShadow: '0 8px 24px rgba(0,0,0,0.25)', maxWidth: 340, textAlign: 'center' }}>
          {photoToast}
        </div>
      )}

    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft py-8"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Product Header Card */}
        <div className="card p-4 sm:p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4 sm:gap-6">
            {/* Product Image Gallery */}
            <ProductImageGallery
              imageUrl={product.image_url}
              images={product.images}
              name={product.name}
              dbPhotos={dbPhotos}
              onDeleteDbPhoto={handleDeletePhoto}
              onDeleteBackendImage={handleDeleteBackendImage}
              isAdmin={isAdmin}
              user={user}
              onOpenUpload={() => setShowPhotoModal(true)}
              onNeedLogin={() => openAuthModal('main')}
            />

            {/* Product Info */}
            <div className="flex-1 text-center md:text-left">
              {product.brand && (
                <p className="text-sm text-primary uppercase font-semibold mb-1">{product.brand}</p>
              )}
              {isAdmin && adminNameEdit ? (
                <div className="flex items-center gap-2 mb-3">
                  <input
                    value={adminNameText}
                    onChange={e => setAdminNameText(e.target.value)}
                    className="font-poppins font-bold text-xl sm:text-2xl text-navy border border-indigo-300 rounded-lg px-3 py-1 flex-1 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    autoFocus
                  />
                  <button
                    disabled={adminNameSaving || !adminNameText.trim()}
                    onClick={async () => {
                      if (!adminNameText.trim()) return
                      setAdminNameSaving(true)
                      try {
                        const isUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(product.id)
                        if (isUUID) {
                          const { data: { session } } = await supabase.auth.getSession()
                          const res = await fetch(`${API_BASE_URL}/api/admin-products/${product.id}/name`, {
                            method: 'PATCH',
                            headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${session?.access_token}` },
                            body: JSON.stringify({ name: adminNameText.trim() }),
                          })
                          if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Save failed') }
                        }
                        _productCache.delete(productName.toLowerCase())
                        setProduct(prev => ({ ...prev, name: adminNameText.trim() }))
                        setAdminNameEdit(false)
                      } catch (e) {
                        alert(`Save failed: ${e.message}`)
                      } finally {
                        setAdminNameSaving(false)
                      }
                    }}
                    className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-xs font-bold rounded-lg px-3 py-1.5 cursor-pointer disabled:cursor-not-allowed whitespace-nowrap"
                  >
                    {adminNameSaving ? 'Saving…' : 'Save'}
                  </button>
                  <button
                    onClick={() => { setAdminNameEdit(false); setAdminNameText('') }}
                    className="text-gray-400 hover:text-gray-600 text-xs font-semibold px-2 py-1.5"
                  >
                    Cancel
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-2 mb-3 justify-center md:justify-start">
                  <h1 className="font-poppins font-bold text-xl sm:text-2xl md:text-3xl text-navy">{product.name}</h1>
                  {isAdmin && (
                    <button
                      onClick={() => { setAdminNameText(product.name); setAdminNameEdit(true) }}
                      title="Edit name"
                      className="text-indigo-400 hover:text-indigo-600 flex-shrink-0"
                    >
                      <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536M9 13l6.586-6.586a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-1.414.586H9v-2a2 2 0 01.586-1.414z"/>
                      </svg>
                    </button>
                  )}
                </div>
              )}
              
              <div className="flex flex-wrap gap-2 mb-4 justify-center md:justify-start">
                {product.category && (
                  <span className="inline-block px-3 py-1 bg-primary-light text-primary rounded-full text-sm">
                    {product.category}
                  </span>
                )}
                <span className="inline-block px-3 py-1 bg-amber-50 text-amber-700 rounded-full text-sm">
                  FSSAI Regulated
                </span>
              </div>
            </div>

            {/* Ingredient Grade */}
            <div className="flex justify-center md:justify-end">
              <GradeBadge grade={grade} size="large" showLabel={true} />
            </div>
          </div>
        </div>

        {/* Quick Insight Section */}
        {(() => {
          let insight, insightBg, insightBorder, insightTextColor, insightIcon

          if (grade === 'A') {
            insight = "The composition suggests a balanced, largely clean formulation that most users may find suitable."
            insightBg = "bg-green-50"
            insightBorder = "border-green-300"
            insightTextColor = "text-green-700"
            insightIcon = (
              <svg className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
              </svg>
            )
          } else if (grade === 'B') {
            insight = "Mostly clean formulation with some commonly noted additives. Suitable for most people."
            insightBg = "bg-blue-50"
            insightBorder = "border-blue-300"
            insightTextColor = "text-blue-700"
            insightIcon = (
              <svg className="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
              </svg>
            )
          } else if (grade === 'C') {
            insight = "This formulation includes several commonly questioned ingredients. Worth reviewing before regular use."
            insightBg = "bg-amber-50"
            insightBorder = "border-amber-300"
            insightTextColor = "text-amber-700"
            insightIcon = (
              <svg className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
              </svg>
            )
          } else {
            insight = "Proportion of questioned or banned ingredients. Review the ingredient details closely before choosing this product."
            insightBg = "bg-red-50"
            insightBorder = "border-red-300"
            insightTextColor = "text-red-700"
            insightIcon = (
              <svg className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd"/>
              </svg>
            )
          }

          return (
            <div className={`card p-4 sm:p-6 mb-6 border-2 ${insightBg} ${insightBorder}`}>
              <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-3">Quick Insight</h2>
              <div className={`flex items-start gap-2 rounded-lg p-3 border ${insightBorder} bg-white`}>
                {insightIcon}
                <p className={`text-sm sm:text-base font-medium ${insightTextColor}`}>{insight}</p>
              </div>
              {(() => {
                const hasFragrance = allIngredients.some(i =>
                  /\b(fragrance|parfum|perfume|cologne)\b/i.test(i.name) &&
                  !/certified organic/i.test(i.name) &&
                  !/ifra|allergen.?free/i.test(i.name)
                )
                const cqCount = commonly_questioned.length
                const fragranceNote = 'If you have sensitive, reactive, or acne-prone skin, it is best to avoid products that only list "fragrance" or "parfum" and look for brands that voluntarily disclose their full ingredient lists.'

                let rec = ''
                if (grade === 'A') {
                  rec = 'This product has a clean ingredient profile and is suitable for most people. Always check for personal allergens before use.'
                } else if (grade === 'B') {
                  rec = 'This product is generally suitable for regular use. It has a few worth-noting ingredients but nothing of serious concern for most people.'
                } else if (grade === 'C') {
                  rec = `This product contains ${cqCount} commonly questioned ingredient${cqCount !== 1 ? 's' : ''}. Review the ingredient details below before regular use, especially if you have skin sensitivities or dietary restrictions.`
                } else {
                  rec = `This product has questioned ingredients. We strongly recommend reviewing the ingredient breakdown below before purchasing, and considering alternatives with cleaner formulations.`
                }

                if (hasFragrance) rec += ' ' + fragranceNote

                return (
                  <div className="mt-3 bg-white rounded-lg p-3 sm:p-4 border border-gray-200">
                    <p className="text-sm font-semibold text-navy mb-1">Recommendation:</p>
                    <p className="text-sm text-gray-700">{rec}</p>
                  </div>
                )
              })()}
            </div>
          )
        })()}

        {/* Complete Ingredients List */}
        <div className="card p-4 sm:p-6 mb-6">
          <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-4">
            Complete Ingredients List ({allIngredients.length} ingredients)
          </h2>
          <div className="bg-gray-50 rounded-lg p-3 sm:p-4">
            <p className="text-sm text-gray-600 leading-relaxed">
              {allIngredients.map((ing, idx) => (
                <span key={idx}>
                  {(ing.classification === 'commonly_questioned' || ing.classification === 'worth_knowing') ? (
                    <span
                      className={`cursor-pointer hover:underline inline-flex items-center gap-0.5 ${
                        ing.classification === 'commonly_questioned' ? 'text-red-700 font-semibold' : 'text-red-500 font-semibold'
                      }`}
                      title="Click to learn more"
                      onClick={() => navigate(`/check-ingredient?q=${encodeURIComponent(ing.name)}`)}
                    >
                      {ing.name}
                      <svg className="w-3 h-3 flex-shrink-0 opacity-60 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </span>
                  ) : (
                    <span className="text-gray-700">{ing.name}</span>
                  )}
                  {ing.aliases && <span className="text-gray-500"> ({ing.aliases})</span>}
                  {idx < allIngredients.length - 1 && ', '}
                </span>
              ))}
            </p>
          </div>

          {/* Admin direct-edit ingredients */}
          {isAdmin && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              {!adminEditMode ? (
                <button
                  onClick={() => {
                    const current = product.ingredients_raw ||
                      (product.ingredients || []).map(i => typeof i === 'string' ? i : i.name).filter(Boolean).join(', ')
                    setAdminIngText(current)
                    setAdminEditMode(true)
                  }}
                  className="text-sm font-semibold text-indigo-600 hover:text-indigo-800 underline cursor-pointer bg-transparent border-none p-0"
                >
                  Admin: Edit ingredients directly
                </button>
              ) : (
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Edit ingredients list (will update database immediately):
                  </label>
                  <textarea
                    value={adminIngText}
                    onChange={e => setAdminIngText(e.target.value)}
                    rows={5}
                    className="w-full border border-indigo-300 rounded-lg p-3 text-sm font-mono resize-vertical focus:outline-none focus:ring-2 focus:ring-indigo-400"
                    placeholder="Water, Sugar, Salt, ..."
                  />
                  <div className="flex gap-2 mt-2">
                    <button
                      disabled={adminSaving || !adminIngText.trim()}
                      onClick={async () => {
                        if (!adminIngText.trim()) return
                        setAdminSaving(true)
                        const rawText = adminIngText.trim()
                        const payload = { ingredients_raw: rawText, ingredients: [] }
                        const isUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(product.id)

                        try {
                          let saveErr = null
                          let resolvedId = adminDbId // use cached ID if we have it
                          const { data: { session: adminSession } } = await supabase.auth.getSession()
                          const adminToken = adminSession?.access_token

                          if (isUUID) {
                            resolvedId = product.id
                          } else if (!resolvedId) {
                            // First edit for a static product — look up or insert via backend
                            const lookupRes = await fetch(`${API_BASE_URL}/api/admin-products/lookup-or-insert`, {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${adminToken}` },
                              body: JSON.stringify({ name: product.name }),
                            })
                            if (!lookupRes.ok) { const e = await lookupRes.json().catch(() => ({})); saveErr = { message: e.detail || 'Lookup failed' } }
                            else { const lj = await lookupRes.json(); resolvedId = lj.id; setAdminDbId(lj.id) }
                          }

                          if (!saveErr && resolvedId) {
                            const updateRes = await fetch(`${API_BASE_URL}/api/admin-products/${resolvedId}/ingredients`, {
                              method: 'PATCH',
                              headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${adminToken}` },
                              body: JSON.stringify(payload),
                            })
                            if (!updateRes.ok) { const e = await updateRes.json().catch(() => ({})); saveErr = { message: e.detail || 'Update failed' } }
                          }

                          if (saveErr) {
                            alert(`Save failed: ${saveErr.message}`)
                            return
                          }

                          // Optimistic update — show new ingredients immediately without waiting for backend
                          const parsed = parseRawIngredients(rawText)
                          setProduct(prev => ({
                            ...prev,
                            ingredients_raw: rawText,
                            ingredients: parsed.map(name => ({
                              name, aliases: '', classification: 'generally_recognised',
                              one_line_note: '', regulatory_note: ''
                            }))
                          }))
                          setAdminEditMode(false)
                          setAdminIngText('')

                          // Reload in background for proper classifications
                          fetchProduct()
                        } finally {
                          setAdminSaving(false)
                        }
                      }}
                      className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-sm font-bold rounded-lg px-4 py-2 cursor-pointer disabled:cursor-not-allowed"
                    >
                      {adminSaving ? 'Saving...' : 'Save Changes'}
                    </button>
                    <button
                      onClick={() => { setAdminEditMode(false); setAdminIngText('') }}
                      className="bg-white text-gray-600 border border-gray-300 hover:border-gray-400 text-sm font-semibold rounded-lg px-4 py-2 cursor-pointer"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* User ingredient report — inside the card */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            {!showReportForm && !reportSuccess && (
              <button
                onClick={() => {
                  if (!user) {
                    setShowReportForm('login')
                  } else {
                    setShowReportForm(true)
                  }
                }}
                className="w-full bg-red-600 hover:bg-red-700 active:bg-red-800 text-white font-semibold rounded-lg px-4 py-2.5 text-sm transition-colors cursor-pointer border-none"
              >
                Ingredients wrong or incomplete? Report it
              </button>
            )}

            {showReportForm === 'login' && (
              <div className="flex items-center justify-between gap-3 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
                <span className="text-sm text-red-700 font-medium">Login to report incorrect ingredients</span>
                <button
                  onClick={() => openAuthModal()}
                  className="bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg px-4 py-2 cursor-pointer border-none"
                >
                  Login
                </button>
              </div>
            )}

            {showReportForm === true && !reportSuccess && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-4">
                <h3 className="font-poppins font-bold text-base text-red-700 mb-3">
                  Report Incorrect Ingredients
                </h3>
                <div className="mb-3">
                  <label className="block text-sm font-semibold text-red-800 mb-1.5">
                    Paste the correct ingredients list from the product label:
                  </label>
                  <textarea
                    value={reportText}
                    onChange={e => setReportText(e.target.value)}
                    placeholder="e.g. Water, Sugar, Palm Oil, Citric Acid (E330), Preservative (E211)..."
                    rows={4}
                    className="w-full border border-red-300 rounded-lg p-3 text-sm resize-vertical focus:outline-none focus:ring-2 focus:ring-red-400 bg-white text-gray-900"
                  />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-semibold text-red-800 mb-1.5">
                    Reason (optional)
                  </label>
                  <input
                    type="text"
                    value={reportReason}
                    onChange={e => setReportReason(e.target.value)}
                    placeholder="e.g. Missing 3 ingredients, wrong order"
                    className="w-full border border-red-300 rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-red-400 bg-white text-gray-900"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    disabled={reportSubmitting || !reportText.trim()}
                    onClick={async () => {
                      if (!reportText.trim()) return
                      setReportSubmitting(true)
                      try {
                        const { data: { session: rptSession } } = await supabase.auth.getSession()
                        const rptRes = await fetch(`${API_BASE_URL}/api/admin-products/reports`, {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${rptSession?.access_token}` },
                          body: JSON.stringify({
                            product_id: product.id,
                            product_name: product.name,
                            reported_ingredients: reportText.trim(),
                            reason: reportReason.trim() || null,
                          }),
                        })
                        if (!rptRes.ok) { const e = await rptRes.json().catch(() => ({})); throw new Error(e.detail || 'Report failed') }
                        setReportSuccess(true)
                        setShowReportForm(false)
                      } catch (e) {
                        alert(`Could not submit report: ${e.message || 'Please try again.'}`)
                      } finally {
                        setReportSubmitting(false)
                      }
                    }}
                    className="bg-red-600 hover:bg-red-700 disabled:bg-gray-300 text-white text-sm font-bold rounded-lg px-5 py-2.5 cursor-pointer disabled:cursor-not-allowed border-none"
                  >
                    {reportSubmitting ? 'Submitting...' : 'Submit Report'}
                  </button>
                  <button
                    onClick={() => { setShowReportForm(false); setReportText(''); setReportReason('') }}
                    className="bg-white text-gray-600 border border-gray-300 hover:border-gray-400 text-sm font-semibold rounded-lg px-5 py-2.5 cursor-pointer"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            )}

            {reportSuccess && (
              <div className="bg-green-50 border border-green-200 rounded-lg px-4 py-3 text-sm text-green-700 font-semibold text-center">
                Thank you! Our team will review your submission and approve it shortly.
              </div>
            )}
          </div>
        </div>

        {/* Commonly Questioned Ingredients */}
        {commonly_questioned.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6 border-l-4 border-red-600">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-red-700 mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-red-600 rounded-full"></span>
              Commonly Questioned ({commonly_questioned.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Ingredients flagged, restricted, or banned in one or more countries. Associated with potential health concerns — worth avoiding or limiting where possible.
            </p>
            <div className="space-y-4">
              {commonly_questioned.map((ing, idx) => (
                <div key={idx} className="bg-red-100 rounded-lg p-3 sm:p-4 border border-red-300">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-sm sm:text-base flex items-center gap-1.5 flex-wrap">
                      <span
                        className="text-red-700 hover:text-red-900 hover:underline cursor-pointer flex items-center gap-1"
                        onClick={() => navigate(`/check-ingredient?q=${encodeURIComponent(ing.name)}`)}
                        title="Learn more about this ingredient"
                      >
                        {ing.name}
                        <svg className="w-3 h-3 flex-shrink-0 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </span>
                      {ing.aliases && <span className="text-xs sm:text-sm text-gray-500 font-normal">({ing.aliases})</span>}
                    </h3>
                  </div>
                  <ExpandableNote text={ing.one_line_note} className="text-sm text-gray-600 mb-2" />
                  {ing.detailed_effects && (
                    <div className="mt-3 pt-3 border-t border-red-300">
                      <p className="text-sm font-semibold text-navy mb-1">Detailed Information:</p>
                      <p className="text-sm text-gray-700 leading-relaxed">{ing.detailed_effects}</p>
                    </div>
                  )}
                  {ing.regulatory_note && (
                    <div className="mt-2 text-xs text-gray-600 italic">
                      Regulatory: {ing.regulatory_note}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Worth Knowing Ingredients */}
        {worth_knowing.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6 border-l-4 border-red-400">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-red-600 mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-red-400 rounded-full"></span>
              Worth Knowing ({worth_knowing.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Ingredients with some concerns or restrictions. May cause issues in sensitive individuals or at high doses. Mixed scientific findings — fine for most people in small amounts.
            </p>
            <div className="space-y-4">
              {worth_knowing.map((ing, idx) => (
                <div key={idx} className="bg-red-50 rounded-lg p-3 sm:p-4 border border-red-200">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-semibold text-sm sm:text-base flex items-center gap-1.5 flex-wrap">
                      <span
                        className="text-red-600 hover:text-red-800 hover:underline cursor-pointer flex items-center gap-1"
                        onClick={() => navigate(`/check-ingredient?q=${encodeURIComponent(ing.name)}`)}
                        title="Learn more about this ingredient"
                      >
                        {ing.name}
                        <svg className="w-3 h-3 flex-shrink-0 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                      </span>
                      {ing.aliases && <span className="text-xs sm:text-sm text-gray-500 font-normal">({ing.aliases})</span>}
                    </h3>
                  </div>
                  {ing.recommendation && (
                    <div className="mb-2 flex items-start gap-2 bg-amber-50 border border-amber-300 rounded-lg px-3 py-2">
                      <svg className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                      <p className="text-sm text-amber-800 font-medium leading-snug">{ing.recommendation}</p>
                    </div>
                  )}
                  <ExpandableNote text={ing.one_line_note} className="text-sm text-gray-600 mb-2" />
                  {ing.detailed_effects && (
                    <div className="mt-3 pt-3 border-t border-red-200">
                      <p className="text-sm font-semibold text-navy mb-1">Detailed Information:</p>
                      <p className="text-sm text-gray-700 leading-relaxed">{ing.detailed_effects}</p>
                    </div>
                  )}
                  {ing.regulatory_note && (
                    <div className="mt-2 text-xs text-gray-600 italic">
                      Regulatory: {ing.regulatory_note}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Generally Recognised Ingredients */}
        {generally_recognised.length > 0 && (
          <div className="card p-4 sm:p-6 mb-6">
            <h2 className="font-poppins font-bold text-lg sm:text-xl text-navy mb-1 flex items-center gap-2">
              <span className="w-3 h-3 bg-green-500 rounded-full"></span>
              Generally Recognised ({generally_recognised.length} ingredients)
            </h2>
            <p className="text-xs text-gray-500 mb-4 leading-relaxed">
              Safe ingredients with no known adverse effects at normal consumption levels. Approved by major regulatory bodies worldwide without restrictions.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {generally_recognised.map((ing, idx) => (
                <div key={idx} className="bg-green-50 rounded-lg p-3 border border-green-200">
                  <h3 className="font-semibold text-navy text-sm">
                    {ing.name}
                    {ing.aliases && <span className="text-xs text-gray-500 font-normal ml-2">({ing.aliases})</span>}
                  </h3>
                  <ExpandableNote text={ing.one_line_note} />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Summary */}
        {product.summary && (
          <div className="card p-6 mb-6">
            <h3 className="font-poppins font-semibold text-navy mb-3">Summary</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{product.summary.replace(/\.?\s*(Awareness\s+)?[Ss]core:\s*\d+\/100\.?/g, '').replace(/\s{2,}/g, ' ').trim()}</p>
          </div>
        )}

        {/* FSSAI Note */}
        {product.fssai_note && (
          <div className="card p-6 mb-6 bg-amber-50 border border-amber-200">
            <h3 className="font-poppins font-semibold text-navy mb-2">FSSAI Position</h3>
            <p className="text-sm text-gray-700">{product.fssai_note}</p>
          </div>
        )}

        {/* Help Improve This Section - Show when data is AI estimated or low confidence */}
        {(product.data_source === 'ai_estimated' || product.confidence === 'low') && (
          <div className="card p-4 sm:p-6 mb-6 bg-yellow-50 border-2 border-yellow-400">
            <div className="flex flex-col sm:flex-row items-start gap-4">
              <div className="flex-shrink-0 mx-auto sm:mx-0">
                <svg className="w-8 h-8 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="flex-1 text-center sm:text-left">
                <h3 className="font-poppins font-bold text-base sm:text-lg text-yellow-900 mb-2">
                  Help Improve This Data
                </h3>
                <p className="text-sm text-yellow-800 mb-4">
                  These ingredients are AI estimated and may be incomplete. Do you have this product with you?
                </p>
                
                {!showCorrectionForm ? (
                  <div className="flex flex-col sm:flex-row flex-wrap gap-3 justify-center sm:justify-start">
                    <button
                      onClick={handleVerifyCorrect}
                      className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium text-sm transition-colors"
                    >
                      ✓ Ingredients look correct
                    </button>
                    <button
                      onClick={() => setShowCorrectionForm(true)}
                      className="px-4 py-2 bg-primary hover:bg-primary-dark text-white rounded-lg font-medium text-sm transition-colors"
                    >
                      Submit correct ingredients
                    </button>
                  </div>
                ) : (
                  <div className="bg-white rounded-lg p-3 sm:p-4 border border-yellow-300">
                    <label className="block text-sm font-semibold text-navy mb-2">
                      Paste the complete ingredients list from the product label:
                    </label>
                    <textarea
                      value={correctionText}
                      onChange={(e) => setCorrectionText(e.target.value)}
                      placeholder="Example: Water, Sugar, Wheat Flour, Palm Oil, Salt, Citric Acid (E330), Preservative (E211)..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
                      rows="4"
                    />
                    <div className="flex flex-col sm:flex-row gap-3 mt-3">
                      <button
                        onClick={handleSubmitCorrection}
                        disabled={submitting}
                        className="px-4 py-2 bg-primary hover:bg-primary-dark text-white rounded-lg font-medium text-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {submitting ? 'Submitting...' : 'Submit Correction'}
                      </button>
                      <button
                        onClick={() => {
                          setShowCorrectionForm(false)
                          setCorrectionText('')
                        }}
                        className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-medium text-sm transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Ratings & Reviews */}
        <ProductReviews productId={product.id} productName={product.name} />

        {/* Disclaimer */}
        <div className="mb-6">
          <DisclaimerBox variant="info">
            The Ingredient Grade (A/B/C/D) is based on published international regulatory data. Grade D means one or more commonly questioned or banned ingredients are present. Grade A means all ingredients are generally recognised as safe. It is not a safety rating, health claim, or medical assessment. Parkho does not certify any product as safe or unsafe. Always read the actual product label and consult a qualified professional for personal health decisions.
          </DisclaimerBox>
        </div>
      </div>
    </motion.div>
    </>
  )
}

export default Result
