import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'
const STATUS_TABS  = ['pending', 'approved', 'rejected', 'extracted', 'photos', 'reports']
const BRAND_BLUE   = '#1B3F8A'
const STATUS_COLOR = { pending: '#f59e0b', approved: '#16a34a', rejected: '#dc2626', extracted: '#7c3aed', photos: '#0ea5e9', reports: '#3b82f6' }
const STATUS_BG    = { pending: '#fef3c7', approved: '#f0fdf4', rejected: '#fef2f2', extracted: '#f5f3ff', photos: '#f0f9ff', reports: '#eff6ff' }

const CATEGORIES = ['Personal Care', 'Skincare', 'Haircare', 'Food & Beverages', 'Supplements', 'Baby Care', 'Other']

const ALL_CATEGORIES = [
  'Skincare', 'Hair Care', 'Personal Care', 'Cosmetics', 'Food', 'Snacks', 'Beverages',
  'Soft Drink', 'Health Drink', 'Biscuits', 'Chocolate', 'Nutrition', 'Protein Supplement',
  'Baby Care', 'Oral Care', 'Household', 'Dairy', 'Instant Noodles', 'Spices', 'Condiments',
  'Cooking Oil', 'Breakfast Cereal', 'Energy Drink', 'Sports Drink', 'Health Supplement',
  'Confectionery', 'Bakery', 'Ready to Eat', 'Pickles', 'Fruit Drink', 'Fruit Juice', 'Dessert', 'Other',
]

// ── Ingredient classification keyword lists ───────────────────────────────────
const COMMONLY_QUESTIONED = [
  // Parabens
  'methylparaben', 'ethylparaben', 'propylparaben', 'butylparaben', 'isobutylparaben',
  // SLS (strong irritant)
  'sodium lauryl sulfate',
  // Formaldehyde releasers
  'dmdm hydantoin', 'imidazolidinyl urea', 'diazolidinyl urea', 'quaternium-15', 'bronopol', '2-bromo-2-nitropropane', 'formaldehyde',
  // Phthalates
  'dibutyl phthalate', 'diethyl phthalate', 'dimethyl phthalate',
  // Antimicrobials
  'triclosan', 'triclocarban',
  // Preservatives with serious concerns (forms benzene, EU carcinogen concern)
  'sodium benzoate', 'e211',
  'sodium metabisulphite', 'e223',
  'sulfur dioxide', 'e220',
  // Preservatives in personal care (EU banned in leave-on products)
  'methylisothiazolinone', 'methylchloroisothiazolinone',
  // Antioxidants (potential carcinogens)
  'butylated hydroxyanisole', 'butylated hydroxytoluene', 'tbhq',
  // EU-restricted food colours (with E-number aliases for label matching)
  'allura red', 'red 40', 'e129',
  'tartrazine', 'yellow 5', 'e102',
  'sunset yellow', 'yellow 6', 'e110',
  'carmoisine', 'azorubine', 'e122',
  'ponceau 4r', 'e124',
  'erythrosine', 'red 3', 'e127',
  'patent blue v', 'e131',
  'indigo carmine', 'e132',
  'brown ht', 'e155',
  'brilliant blue', 'e133',
  'quinoline yellow', 'e104',
  // Flavor enhancers with MSG-like concerns
  'disodium guanylate', 'e627',
  'disodium inosinate', 'e631',
  // Acids with bone/tooth concerns
  'phosphoric acid', 'e338',
  // Caramel (Class III/IV — contains 4-MEI)
  'caramel colour', 'caramel color', 'e150',
  // Sweeteners
  'aspartame', 'e951',
  'acesulfame-k', 'acesulfame k', 'e950',
  // Meat preservatives
  'sodium nitrite', 'e250', 'sodium nitrate', 'e251',
  // Others
  'potassium bromate', 'azodicarbonamide', 'brominated vegetable oil',
  // Antioxidant preservatives (by abbreviation — full names above)
  'bha', 'bht',
  // Talc (potential asbestos contamination; IARC Group 1 when asbestos-contaminated)
  'talc', 'talcum',
  // CI food/cosmetic colorants banned or restricted in multiple countries
  'ci 47000',  // Quinoline Yellow E104 — banned USA, Canada, Japan, Australia
  'ci 19140',  // Tartrazine E102 — EU warning label, banned several countries
  'ci 15985',  // Sunset Yellow E110 — banned Norway, Finland; EU warning label
  'ci 16035',  // Allura Red E129 — EU warning label; banned several European countries
  'ci 42090',  // Brilliant Blue E133 — banned in 6 EU countries; neurotoxicity data
]

const WORTH_KNOWING = [
  // SLES (milder than SLS but can be irritant)
  'sodium laureth sulfate', 'ammonium laureth sulfate',
  // Preservatives
  'phenoxyethanol', 'potassium sorbate', 'e202', 'benzyl alcohol',
  // Fragrance (hides unknowns)
  'fragrance', 'parfum', 'artificial flavor', 'artificial flavour',
  // Sensitizers
  'cocamidopropyl betaine',
  // Silicones
  'dimethicone', 'cyclomethicone', 'cyclopentasiloxane', 'cyclohexasiloxane', 'dimethiconol', 'amodimethicone',
  // PEGs
  'peg-', 'polyethylene glycol',
  // Petroleum-derived
  'mineral oil', 'petrolatum', 'paraffinum liquidum', 'paraffin wax',
  // Alcohol
  'alcohol denat', 'denatured alcohol', 'sd alcohol',
  // Allergens
  'lanolin', 'wool wax',
  // Sweeteners (moderate evidence)
  'sucralose', 'e955', 'saccharin', 'e954',
  // Food additives
  'high fructose corn syrup', 'monosodium glutamate', 'e621',
  'carrageenan', 'e407',
  'hydrogenated', 'partially hydrogenated',
  // Titanium Dioxide (EU banned as food additive E171; nanoparticle concerns)
  'titanium dioxide',
  // CI cosmetic colorants (permitted, limited long-term safety data)
  'ci 26100', 'ci 61565', 'ci 17200', 'ci 15510', 'ci 45410',
  // Iron oxides (ci 77491/77492/77499) are safe mineral pigments — not listed here,
  // they fall through to generally_recognised
]

function classifyIngredient(name) {
  // Normalize: "CI No. 47000" → "ci 47000", collapse spaces
  const n = name.toLowerCase()
    .replace(/\bno\.\s*/g, '')
    .replace(/\s+/g, ' ')
    .trim()
  for (const kw of COMMONLY_QUESTIONED) {
    if (n.includes(kw)) return 'commonly_questioned'
  }
  for (const kw of WORTH_KNOWING) {
    if (n.includes(kw)) return 'worth_knowing'
  }
  return 'generally_recognised'
}

function parseIngredients(text) {
  return text
    .split(/[,;]/)
    .map(s => s.trim())
    .filter(s => s.length > 0)
    .map(name => ({
      name: name.slice(0, 100),
      aliases: '',
      classification: classifyIngredient(name),
      one_line_note: '',
      regulatory_note: '',
    }))
}

function calculateScore(ingredients) {
  let score = 100
  for (const ing of ingredients) {
    if (ing.classification === 'commonly_questioned') score -= 20
    else if (ing.classification === 'worth_knowing') score -= 8
  }
  return Math.max(0, score)
}

function verdictFromScore(score) {
  if (score >= 80) return 'Clean formulation'
  if (score >= 60) return 'Average formulation'
  if (score >= 40) return 'Worth reviewing'
  return 'Review carefully'
}

function recommendationFromScore(score) {
  if (score >= 80) return 'Generally suitable for regular use. Check for personal allergies.'
  if (score >= 60) return 'Suitable for most people. Some ingredients may warrant attention.'
  if (score >= 40) return 'Review ingredient list before regular use, especially for sensitive individuals.'
  return 'Consider checking with a professional before regular use.'
}

async function downloadImg(url, filename) {
  try {
    const resp = await fetch(url, { mode: 'cors' })
    if (!resp.ok) throw new Error()
    const blob = await resp.blob()
    const blobUrl = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = blobUrl
    a.download = filename || 'image.jpg'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    setTimeout(() => URL.revokeObjectURL(blobUrl), 1000)
  } catch {
    window.open(url, '_blank')
  }
}

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 640)
  useEffect(() => {
    const fn = () => setIsMobile(window.innerWidth < 640)
    window.addEventListener('resize', fn)
    return () => window.removeEventListener('resize', fn)
  }, [])
  return isMobile
}

function ImageViewer({ imgs }) {
  const [idx, setIdx] = useState(0)
  const touchStartX = useRef(null)

  const prev = () => setIdx(i => (i - 1 + imgs.length) % imgs.length)
  const next = () => setIdx(i => (i + 1) % imgs.length)
  const onTouchStart = e => { touchStartX.current = e.touches[0].clientX }
  const onTouchEnd = e => {
    if (touchStartX.current === null) return
    const dx = e.changedTouches[0].clientX - touchStartX.current
    if (Math.abs(dx) > 40) { dx < 0 ? next() : prev() }
    touchStartX.current = null
  }

  if (!imgs.length) return (
    <div style={{ height: 200, background: '#f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <span style={{ color: '#9ca3af', fontSize: 13 }}>No images</span>
    </div>
  )

  return (
    <div style={{ position: 'relative', height: 220, background: '#111', overflow: 'hidden', userSelect: 'none' }}
      onTouchStart={onTouchStart} onTouchEnd={onTouchEnd}>
      <img src={imgs[idx]} alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
      {imgs.length > 1 && (
        <>
          <button onClick={prev} style={{ position: 'absolute', left: 6, top: '50%', transform: 'translateY(-50%)', background: 'rgba(0,0,0,0.45)', border: 'none', color: '#fff', borderRadius: '50%', width: 32, height: 32, fontSize: 16, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>‹</button>
          <button onClick={next} style={{ position: 'absolute', right: 6, top: '50%', transform: 'translateY(-50%)', background: 'rgba(0,0,0,0.45)', border: 'none', color: '#fff', borderRadius: '50%', width: 32, height: 32, fontSize: 16, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>›</button>
          <div style={{ position: 'absolute', bottom: 8, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 5 }}>
            {imgs.map((_, i) => (
              <button key={i} onClick={() => setIdx(i)}
                style={{ width: i === idx ? 20 : 7, height: 7, borderRadius: 99, border: 'none', cursor: 'pointer', background: i === idx ? '#FF9933' : 'rgba(255,255,255,0.5)', padding: 0, transition: 'all 0.2s' }} />
            ))}
          </div>
        </>
      )}
      <a href={imgs[idx]} target="_blank" rel="noreferrer"
        style={{ position: 'absolute', top: 8, right: 8, background: 'rgba(0,0,0,0.5)', color: '#fff', borderRadius: 6, padding: '4px 10px', fontSize: 11, textDecoration: 'none', fontWeight: 600 }}>
        Full ↗
      </a>
      <span style={{ position: 'absolute', top: 8, left: 8, background: 'rgba(0,0,0,0.5)', color: '#fff', borderRadius: 6, padding: '3px 8px', fontSize: 11, fontWeight: 600 }}>
        {idx + 1}/{imgs.length}
      </span>
    </div>
  )
}

function SubmissionCard({ sub, onApprove, onReject, onSave, saving, cardMsg }) {
  const imgs = sub.images || []
  const [ingredients, setIngredients] = useState('')
  const [brand,       setBrand]       = useState('')
  const [category,    setCategory]    = useState('Personal Care')

  const isSaving = saving === sub.id

  // Live classification preview
  const parsed = ingredients.trim() ? parseIngredients(ingredients) : []
  const autoScore = parsed.length > 0 ? calculateScore(parsed) : null
  const cq = parsed.filter(i => i.classification === 'commonly_questioned').length
  const wk = parsed.filter(i => i.classification === 'worth_knowing').length
  const gr = parsed.filter(i => i.classification === 'generally_recognised').length

  const field = {
    width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db',
    borderRadius: 8, padding: '9px 12px', fontSize: 13, fontFamily: 'inherit',
    outline: 'none', color: '#111827', background: '#fff',
  }

  return (
    <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 14, overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.05)' }}>
      <ImageViewer imgs={imgs} />

      <div style={{ padding: '14px 16px' }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8, marginBottom: 10 }}>
          <div style={{ minWidth: 0 }}>
            <p style={{ margin: 0, fontWeight: 700, fontSize: 14, color: '#111827', wordBreak: 'break-word' }}>
              {sub.product_name_searched}
            </p>
            <p style={{ margin: '3px 0 0', fontSize: 12, color: '#9ca3af' }}>{formatDate(sub.created_at)}</p>
          </div>
          <span style={{ flexShrink: 0, background: STATUS_BG[sub.status], color: STATUS_COLOR[sub.status], fontSize: 11, fontWeight: 700, padding: '4px 10px', borderRadius: 99, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            {sub.status}
          </span>
        </div>

        {/* Info */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 7, marginBottom: 14 }}>
          <div style={{ display: 'flex', gap: 8 }}>
            <span style={{ fontSize: 15 }}>📧</span>
            <span style={{ fontSize: 13, color: '#374151', wordBreak: 'break-all' }}>{sub.email || '—'}</span>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <span style={{ fontSize: 15 }}>💳</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: '#1d4ed8', wordBreak: 'break-all' }}>{sub.contact}</span>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <span style={{ fontSize: 15 }}>🖼️</span>
            <span style={{ fontSize: 13, color: '#6b7280' }}>{imgs.length} image{imgs.length !== 1 ? 's' : ''}</span>
          </div>
        </div>

        {/* Pending */}
        {sub.status === 'pending' && (
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => onApprove(sub.id)}
              style={{ flex: 1, background: '#16a34a', color: '#fff', border: 'none', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
              ✓ Approve
            </button>
            <button onClick={() => onReject(sub.id)}
              style={{ flex: 1, background: '#fff', color: '#dc2626', border: '1.5px solid #dc2626', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
              ✕ Reject
            </button>
          </div>
        )}

        {/* Approved — manual form */}
        {sub.status === 'approved' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>

            {/* Brand + Category */}
            <div style={{ display: 'flex', gap: 8 }}>
              <input
                placeholder="Brand (e.g. Dove)"
                value={brand}
                onChange={e => setBrand(e.target.value)}
                style={{ ...field, flex: 1 }}
                disabled={isSaving}
              />
              <select
                value={category}
                onChange={e => setCategory(e.target.value)}
                style={{ ...field, flex: 1, cursor: 'pointer' }}
                disabled={isSaving}
              >
                {CATEGORIES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>

            {/* Ingredients textarea */}
            <div>
              <p style={{ margin: '0 0 5px', fontSize: 12, color: '#6b7280', fontWeight: 600 }}>
                Paste ingredients (comma-separated, from back label):
              </p>
              <textarea
                value={ingredients}
                onChange={e => setIngredients(e.target.value)}
                placeholder="Water, Glycerin, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Fragrance..."
                rows={5}
                style={{ ...field, resize: 'vertical' }}
                disabled={isSaving}
              />
            </div>

            {/* Live classification preview */}
            {parsed.length > 0 && (
              <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8, padding: '10px 12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: '#374151' }}>
                    {parsed.length} ingredients detected
                  </span>
                  <span style={{ fontSize: 14, fontWeight: 800, color: autoScore >= 80 ? '#16a34a' : autoScore >= 60 ? '#ca8a04' : autoScore >= 40 ? '#ea580c' : '#dc2626' }}>
                    Score: {autoScore}/100
                  </span>
                </div>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {gr > 0 && <span style={{ fontSize: 11, fontWeight: 600, background: '#f0fdf4', color: '#16a34a', border: '1px solid #bbf7d0', borderRadius: 99, padding: '2px 8px' }}>🟢 {gr} clean</span>}
                  {wk > 0 && <span style={{ fontSize: 11, fontWeight: 600, background: '#fefce8', color: '#ca8a04', border: '1px solid #fde68a', borderRadius: 99, padding: '2px 8px' }}>🟡 {wk} worth knowing</span>}
                  {cq > 0 && <span style={{ fontSize: 11, fontWeight: 600, background: '#fef2f2', color: '#dc2626', border: '1px solid #fecaca', borderRadius: 99, padding: '2px 8px' }}>🔴 {cq} questioned</span>}
                </div>
              </div>
            )}

            {/* Save button */}
            <button
              onClick={() => onSave(sub.id, { text: ingredients, brand, category })}
              disabled={isSaving || !ingredients.trim()}
              style={{
                width: '100%',
                background: isSaving ? '#d1fae5' : !ingredients.trim() ? '#f3f4f6' : '#059669',
                color: isSaving || !ingredients.trim() ? '#9ca3af' : '#fff',
                border: 'none', borderRadius: 10, padding: '12px 0', fontSize: 15, fontWeight: 700,
                cursor: isSaving || !ingredients.trim() ? 'not-allowed' : 'pointer',
                fontFamily: 'inherit', transition: 'background 0.2s',
              }}>
              {isSaving ? '⏳ Saving…' : '💾 Save to Database'}
            </button>

            {cardMsg && (
              <div style={{
                padding: '10px 14px', borderRadius: 8, fontSize: 13, fontWeight: 600, lineHeight: 1.5,
                background: cardMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
                color: cardMsg.type === 'success' ? '#16a34a' : '#dc2626',
                border: `1px solid ${cardMsg.type === 'success' ? '#bbf7d0' : '#fecaca'}`,
              }}>
                {cardMsg.text}
              </div>
            )}
          </div>
        )}

        {/* Extracted — success + downloadable images */}
        {sub.status === 'extracted' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <div style={{ fontSize: 13, color: '#7c3aed', fontWeight: 700 }}>
              ✓ Added to database
            </div>
            {imgs.length > 0 && (
              <div>
                <p style={{ margin: '0 0 6px', fontSize: 12, fontWeight: 600, color: '#6b7280' }}>
                  Download product images:
                </p>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                  {imgs.map((url, i) => (
                    <button key={i}
                      onClick={() => downloadImg(url, `${sub.product_name_searched.replace(/\s+/g, '_')}_${i + 1}.jpg`)}
                      style={{ background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: 8, padding: '7px 14px', fontSize: 12, fontWeight: 700, color: '#1d4ed8', cursor: 'pointer', fontFamily: 'inherit' }}>
                      ⬇ Image {i + 1}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function AddProductForm({ isMobile }) {
  const navigate = useNavigate()
  const [name,        setName]        = useState('')
  const [brand,       setBrand]       = useState('')
  const [category,    setCategory]    = useState('Skincare')
  const [ingredients, setIngredients] = useState('')
  const [imageUrl,    setImageUrl]    = useState('')
  const [imageFile,   setImageFile]   = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [saving,      setSaving]      = useState(false)
  const [msg,         setMsg]         = useState(null)
  const fileRef = useRef(null)

  const parsed   = ingredients.trim() ? parseIngredients(ingredients) : []
  const score    = parsed.length > 0 ? calculateScore(parsed) : null
  const cq       = parsed.filter(i => i.classification === 'commonly_questioned').length
  const wk       = parsed.filter(i => i.classification === 'worth_knowing').length
  const gr       = parsed.filter(i => i.classification === 'generally_recognised').length

  const gradeFromScore = s => s >= 80 ? 'A' : s >= 60 ? 'B' : s >= 40 ? 'C' : 'D'

  const handleFileChange = (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setImageFile(file)
    setImageUrl('')
    const reader = new FileReader()
    reader.onload = ev => setImagePreview(ev.target.result)
    reader.readAsDataURL(file)
  }

  const handleUrlChange = (e) => {
    setImageUrl(e.target.value)
    setImageFile(null)
    setImagePreview(e.target.value || null)
  }

  const uploadImage = async (productId) => {
    if (!imageFile) return imageUrl || null
    try {
      const ext  = imageFile.name.split('.').pop()
      const path = `products/${productId}.${ext}`
      const { error } = await supabase.storage.from('product-images').upload(path, imageFile, { upsert: true })
      if (error) throw error
      const { data: { publicUrl } } = supabase.storage.from('product-images').getPublicUrl(path)
      return publicUrl
    } catch (e) {
      console.warn('Image upload failed:', e.message)
      return null
    }
  }

  const makeStaticKey = (n) => n.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

  const handleSave = async () => {
    if (!name.trim() || !ingredients.trim()) {
      setMsg({ type: 'error', text: 'Product name and ingredients are required.' })
      return
    }
    setSaving(true)
    setMsg(null)
    try {
      const key   = makeStaticKey(name.trim())
      const grade = gradeFromScore(score ?? 50)

      // Insert first to get the UUID, then upload image with that UUID
      const { data: inserted, error: insertErr } = await supabase
        .from('ai_extracted_products')
        .insert({
          name:            name.trim(),
          brand:           brand.trim() || null,
          category,
          ingredients_raw: ingredients.trim(),
          ingredients:     [],
          grade,
          static_key:      key,
          summary:         `${name.trim()} by ${brand.trim() || 'Unknown'}. Grade ${grade}.`,
          fssai_note:      'Subject to FSSAI regulations.',
          verdict:         verdictFromScore(score ?? 50),
          recommendation:  recommendationFromScore(score ?? 50),
          image_url:       imageUrl || null,
        })
        .select('id')
        .single()

      if (insertErr) throw new Error(insertErr.message)

      // Now upload the image file if provided, and update the record
      if (imageFile) {
        const uploadedUrl = await uploadImage(inserted.id)
        if (uploadedUrl) {
          await supabase.from('ai_extracted_products')
            .update({ image_url: uploadedUrl })
            .eq('id', inserted.id)
        }
      }

      setMsg({ type: 'success', text: `"${name.trim()}" saved successfully! Grade ${grade}. It will appear in search and browse immediately.` })
      // Reset form
      setName(''); setBrand(''); setIngredients(''); setImageUrl(''); setImageFile(null); setImagePreview(null)
    } catch (e) {
      setMsg({ type: 'error', text: `Save failed: ${e.message}` })
    } finally {
      setSaving(false)
    }
  }

  const field = {
    width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db',
    borderRadius: 10, padding: '10px 14px', fontSize: 14, fontFamily: 'inherit',
    outline: 'none', color: '#111827', background: '#fff',
  }

  return (
    <div style={{ maxWidth: 640, margin: '0 auto' }}>
      <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 16, padding: isMobile ? '20px 16px' : '28px 28px', boxShadow: '0 4px 20px rgba(0,0,0,0.06)' }}>
        <h2 style={{ fontFamily: 'Poppins,sans-serif', fontSize: 18, fontWeight: 800, color: BRAND_BLUE, margin: '0 0 20px' }}>
          Add New Product
        </h2>

        {/* Name + Brand row */}
        <div style={{ display: 'flex', gap: 10, marginBottom: 12, flexDirection: isMobile ? 'column' : 'row' }}>
          <div style={{ flex: 2 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 5 }}>Product Name *</label>
            <input
              value={name}
              onChange={e => setName(e.target.value)}
              placeholder="e.g. Dove Beauty Bar Soap"
              style={field}
              disabled={saving}
            />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 5 }}>Brand</label>
            <input
              value={brand}
              onChange={e => setBrand(e.target.value)}
              placeholder="e.g. Dove"
              style={field}
              disabled={saving}
            />
          </div>
        </div>

        {/* Category */}
        <div style={{ marginBottom: 12 }}>
          <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 5 }}>Category</label>
          <select value={category} onChange={e => setCategory(e.target.value)} style={{ ...field, cursor: 'pointer' }} disabled={saving}>
            {ALL_CATEGORIES.map(c => <option key={c}>{c}</option>)}
          </select>
        </div>

        {/* Image */}
        <div style={{ marginBottom: 14 }}>
          <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 5 }}>Product Image (optional)</label>
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', flexDirection: isMobile ? 'column' : 'row' }}>
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 6 }}>
              <input
                value={imageUrl}
                onChange={handleUrlChange}
                placeholder="Paste image URL…"
                style={{ ...field, fontSize: 13 }}
                disabled={saving || !!imageFile}
              />
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <hr style={{ flex: 1, border: 'none', borderTop: '1px solid #e5e7eb' }} />
                <span style={{ fontSize: 11, color: '#9ca3af', fontWeight: 600 }}>OR</span>
                <hr style={{ flex: 1, border: 'none', borderTop: '1px solid #e5e7eb' }} />
              </div>
              <button
                type="button"
                onClick={() => fileRef.current?.click()}
                disabled={saving || !!imageUrl}
                style={{ padding: '9px 0', borderRadius: 8, border: '1.5px dashed #d1d5db', background: imageFile ? '#f0fdf4' : '#f9fafb', color: imageFile ? '#16a34a' : '#6b7280', fontSize: 13, fontWeight: 600, cursor: saving || !!imageUrl ? 'not-allowed' : 'pointer', fontFamily: 'inherit', opacity: imageUrl ? 0.5 : 1 }}>
                {imageFile ? `✓ ${imageFile.name}` : '📁 Upload from device'}
              </button>
              <input ref={fileRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileChange} />
            </div>
            {imagePreview && (
              <div style={{ flexShrink: 0, width: 90, height: 90, border: '2px solid #e5e7eb', borderRadius: 10, overflow: 'hidden', background: '#f9fafb', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                <img src={imagePreview} alt="Preview" style={{ width: '100%', height: '100%', objectFit: 'contain', padding: 4 }} onError={() => setImagePreview(null)} />
                <button onClick={() => { setImageUrl(''); setImageFile(null); setImagePreview(null) }}
                  style={{ position: 'absolute', top: 3, right: 3, width: 18, height: 18, borderRadius: '50%', background: '#dc2626', border: 'none', color: '#fff', fontSize: 11, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', lineHeight: 1, padding: 0 }}>
                  ×
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Ingredients */}
        <div style={{ marginBottom: 14 }}>
          <label style={{ display: 'block', fontSize: 12, fontWeight: 700, color: '#374151', marginBottom: 5 }}>
            Ingredients * <span style={{ fontWeight: 400, color: '#9ca3af' }}>(comma-separated, from product label)</span>
          </label>
          <textarea
            value={ingredients}
            onChange={e => setIngredients(e.target.value)}
            placeholder="Water, Glycerin, Sodium Laureth Sulfate, Cocamidopropyl Betaine, Fragrance, Citric Acid..."
            rows={5}
            style={{ ...field, resize: 'vertical', lineHeight: 1.6 }}
            disabled={saving}
          />
        </div>

        {/* Live classification preview */}
        {parsed.length > 0 && (
          <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, padding: '12px 14px', marginBottom: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: '#374151' }}>{parsed.length} ingredients detected</span>
              <div style={{ display: 'flex', align: 'center', gap: 8 }}>
                <span style={{ fontSize: 12, color: '#6b7280' }}>Score {score}/100</span>
                <span style={{
                  fontSize: 14, fontWeight: 800, padding: '2px 10px', borderRadius: 8,
                  background: score >= 80 ? '#f0fdf4' : score >= 60 ? '#eff6ff' : score >= 40 ? '#fffbeb' : '#fef2f2',
                  color: score >= 80 ? '#16a34a' : score >= 60 ? '#2563eb' : score >= 40 ? '#d97706' : '#dc2626',
                }}>
                  Grade {gradeFromScore(score)}
                </span>
              </div>
            </div>
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {gr > 0 && <span style={{ fontSize: 12, fontWeight: 600, background: '#f0fdf4', color: '#16a34a', border: '1px solid #bbf7d0', borderRadius: 99, padding: '3px 10px' }}>🟢 {gr} clean</span>}
              {wk > 0 && <span style={{ fontSize: 12, fontWeight: 600, background: '#fefce8', color: '#ca8a04', border: '1px solid #fde68a', borderRadius: 99, padding: '3px 10px' }}>🟡 {wk} worth knowing</span>}
              {cq > 0 && <span style={{ fontSize: 12, fontWeight: 600, background: '#fef2f2', color: '#dc2626', border: '1px solid #fecaca', borderRadius: 99, padding: '3px 10px' }}>🔴 {cq} questioned</span>}
            </div>
          </div>
        )}

        {/* Save button */}
        <button
          onClick={handleSave}
          disabled={saving || !name.trim() || !ingredients.trim()}
          style={{
            width: '100%', padding: '14px 0', borderRadius: 12, border: 'none', fontFamily: 'inherit',
            fontSize: 16, fontWeight: 800, cursor: saving || !name.trim() || !ingredients.trim() ? 'not-allowed' : 'pointer',
            background: saving ? '#e0e7ff' : !name.trim() || !ingredients.trim() ? '#f3f4f6' : BRAND_BLUE,
            color: saving ? BRAND_BLUE : !name.trim() || !ingredients.trim() ? '#9ca3af' : '#fff',
            transition: 'all 0.2s',
          }}>
          {saving ? 'Saving product…' : 'Save Product to Database'}
        </button>

        {msg && (
          <div style={{
            marginTop: 14, padding: '12px 16px', borderRadius: 10, fontSize: 14, fontWeight: 600, lineHeight: 1.5,
            background: msg.type === 'success' ? '#f0fdf4' : '#fef2f2',
            color: msg.type === 'success' ? '#16a34a' : '#dc2626',
            border: `1.5px solid ${msg.type === 'success' ? '#bbf7d0' : '#fecaca'}`,
          }}>
            {msg.text}
            {msg.type === 'success' && name === '' && (
              <button onClick={() => navigate(`/result/${encodeURIComponent(name)}`)}
                style={{ display: 'block', marginTop: 8, background: BRAND_BLUE, color: '#fff', border: 'none', borderRadius: 8, padding: '7px 16px', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                View Product Page
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function DeleteProductSection({ isMobile }) {
  const [query,       setQuery]       = useState('')
  const [results,     setResults]     = useState([])
  const [searching,   setSearching]   = useState(false)
  const [confirmId,   setConfirmId]   = useState(null)
  const [deleting,    setDeleting]    = useState(null)
  const [msg,         setMsg]         = useState(null)
  const debounceRef = useRef(null)

  const GRADE_STYLE = {
    A: { bg: '#f0fdf4', color: '#16a34a', border: '#bbf7d0' },
    B: { bg: '#eff6ff', color: '#2563eb', border: '#bfdbfe' },
    C: { bg: '#fffbeb', color: '#d97706', border: '#fde68a' },
    D: { bg: '#fef2f2', color: '#dc2626', border: '#fecaca' },
  }

  const search = async (q) => {
    if (!q.trim()) { setResults([]); return }
    setSearching(true)
    try {
      const { data } = await supabase
        .from('ai_extracted_products')
        .select('id, name, brand, category, grade, static_key')
        .or(`name.ilike.%${q}%,brand.ilike.%${q}%`)
        .order('static_key', { nullsFirst: false })
        .limit(15)
      setResults(data || [])
    } catch { setResults([]) }
    finally { setSearching(false) }
  }

  const handleChange = (e) => {
    const val = e.target.value
    setQuery(val)
    setConfirmId(null)
    setMsg(null)
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => search(val), 300)
  }

  const handleDelete = async (product) => {
    setDeleting(product.id)
    setMsg(null)
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (!session) throw new Error('Not authenticated — please log out and log back in')

      const url = `${API_BASE_URL}/api/admin/product/${product.id}`
      console.log('[DELETE] calling', url)

      let resp
      try {
        resp = await fetch(url, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${session.access_token}` },
        })
      } catch (networkErr) {
        throw new Error(`Network error — backend may be sleeping (Render cold start). Wait 30s and retry. ${networkErr.message}`)
      }

      const body = await resp.text()
      console.log('[DELETE] status', resp.status, 'body', body)

      if (!resp.ok) {
        let detail = body
        try { detail = JSON.parse(body)?.detail || body } catch {}
        throw new Error(`Server error ${resp.status}: ${detail}`)
      }

      setResults(prev => prev.filter(p => p.id !== product.id))
      setConfirmId(null)
      setMsg({ type: 'success', text: `"${product.name}" permanently deleted from database.` })
    } catch (e) {
      console.error('[DELETE ERROR]', e)
      setMsg({ type: 'error', text: `Delete failed: ${e.message}` })
    } finally {
      setDeleting(null)
    }
  }

  return (
    <div style={{ maxWidth: 640, margin: '0 auto' }}>
      <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 16, padding: isMobile ? '20px 16px' : '28px 28px', boxShadow: '0 4px 20px rgba(0,0,0,0.06)' }}>
        <h2 style={{ fontFamily: 'Poppins,sans-serif', fontSize: 18, fontWeight: 800, color: '#dc2626', margin: '0 0 6px' }}>
          Delete Product
        </h2>
        <p style={{ margin: '0 0 18px', fontSize: 13, color: '#9ca3af' }}>
          Search by name or brand — this permanently removes the product from the database.
        </p>

        {/* Search input */}
        <div style={{ position: 'relative', marginBottom: 14 }}>
          <svg style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', width: 16, height: 16, color: '#9ca3af' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            value={query}
            onChange={handleChange}
            placeholder="Search product name or brand…"
            style={{ width: '100%', boxSizing: 'border-box', paddingLeft: 38, paddingRight: query ? 36 : 14, paddingTop: 10, paddingBottom: 10, border: '1.5px solid #d1d5db', borderRadius: 10, fontSize: 14, fontFamily: 'inherit', outline: 'none', color: '#111827', background: '#fff' }}
          />
          {query && (
            <button onClick={() => { setQuery(''); setResults([]); setMsg(null); setConfirmId(null) }}
              style={{ position: 'absolute', right: 10, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', fontSize: 18, color: '#9ca3af', cursor: 'pointer', lineHeight: 1, padding: 0 }}>
              ×
            </button>
          )}
        </div>

        {/* Status message */}
        {msg && (
          <div style={{ marginBottom: 14, padding: '10px 14px', borderRadius: 10, fontSize: 13, fontWeight: 600,
            background: msg.type === 'success' ? '#f0fdf4' : '#fef2f2',
            color: msg.type === 'success' ? '#16a34a' : '#dc2626',
            border: `1.5px solid ${msg.type === 'success' ? '#bbf7d0' : '#fecaca'}` }}>
            {msg.text}
          </div>
        )}

        {/* Results */}
        {searching && (
          <div style={{ textAlign: 'center', padding: '24px 0', color: '#9ca3af', fontSize: 13 }}>Searching…</div>
        )}

        {!searching && query && results.length === 0 && (
          <div style={{ textAlign: 'center', padding: '24px 0', color: '#9ca3af', fontSize: 13 }}>No products found for "{query}"</div>
        )}

        {!searching && results.length > 0 && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {results.map(p => {
              const g = p.grade || 'C'
              const gs = GRADE_STYLE[g] || GRADE_STYLE.C
              const isConfirm = confirmId === p.id
              const isDeleting = deleting === p.id

              return (
                <div key={p.id} style={{ border: `1.5px solid ${isConfirm ? '#fca5a5' : '#e5e7eb'}`, borderRadius: 12, padding: '12px 14px', background: isConfirm ? '#fff5f5' : '#fff', transition: 'all 0.15s' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                    {/* Grade pill */}
                    <span style={{ flexShrink: 0, fontSize: 12, fontWeight: 800, padding: '3px 10px', borderRadius: 99, background: gs.bg, color: gs.color, border: `1px solid ${gs.border}` }}>
                      Grade {g}
                    </span>

                    {/* Info */}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <p style={{ margin: 0, fontWeight: 700, fontSize: 14, color: '#111827', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{p.name}</p>
                      <p style={{ margin: '2px 0 0', fontSize: 12, color: '#9ca3af' }}>{[p.brand, p.category].filter(Boolean).join(' · ')}</p>
                    </div>

                    {/* Action */}
                    {!isConfirm && (
                      <button
                        onClick={() => { setConfirmId(p.id); setMsg(null) }}
                        style={{ flexShrink: 0, background: '#fff', color: '#dc2626', border: '1.5px solid #fca5a5', borderRadius: 8, padding: '6px 14px', fontSize: 12, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                        Delete
                      </button>
                    )}
                  </div>

                  {/* Confirm row */}
                  {isConfirm && (
                    <div style={{ marginTop: 10, padding: '10px 12px', background: '#fef2f2', borderRadius: 8, border: '1px solid #fecaca' }}>
                      <p style={{ margin: '0 0 10px', fontSize: 13, fontWeight: 600, color: '#dc2626' }}>
                        Permanently delete "{p.name}"? This cannot be undone.
                      </p>
                      <div style={{ display: 'flex', gap: 8 }}>
                        <button
                          onClick={() => handleDelete(p)}
                          disabled={isDeleting}
                          style={{ flex: 1, background: '#dc2626', color: '#fff', border: 'none', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: isDeleting ? 'not-allowed' : 'pointer', fontFamily: 'inherit', opacity: isDeleting ? 0.7 : 1 }}>
                          {isDeleting ? 'Deleting…' : 'Yes, Delete'}
                        </button>
                        <button
                          onClick={() => setConfirmId(null)}
                          disabled={isDeleting}
                          style={{ flex: 1, background: '#fff', color: '#374151', border: '1.5px solid #d1d5db', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                          Cancel
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default function Admin() {
  const { user, loading: authLoading } = useAuth()
  const navigate = useNavigate()
  const isMobile = useIsMobile()
  const [tab,        setTab]        = useState('pending')
  const [subs,       setSubs]       = useState([])
  const [counts,     setCounts]     = useState({ pending: 0, approved: 0, rejected: 0, extracted: 0, photos: 0, reports: 0 })
  const [ingredientReports, setIngredientReports] = useState([])
  const [fetching,   setFetching]   = useState(false)
  const [saving,     setSaving]     = useState(null)
  const [cardMsgs,   setCardMsgs]   = useState({})
  const [fetchError, setFetchError] = useState(null)
  const [photoSubs,  setPhotoSubs]  = useState([])
  const [photoFetching, setPhotoFetching] = useState(false)
  const [photoTab, setPhotoTab] = useState('pending')
  const [photoCounts, setPhotoCounts] = useState({ pending: 0, approved: 0, rejected: 0 })

  const isAdmin = user?.email === ADMIN_EMAIL

  useEffect(() => {
    if (!authLoading && !isAdmin) navigate('/')
  }, [user, authLoading, isAdmin, navigate])

  useEffect(() => {
    if (!isAdmin) return
    let cancelled = false

    const run = async () => {
      // Counts (always refresh)
      try {
        const [{ data }, { data: allPhotoData }, { data: repData }] = await Promise.all([
          supabase.from('product_submissions').select('status'),
          supabase.from('product_photo_submissions').select('status'),
          supabase.from('ingredient_reports').select('status'),
        ])
        if (cancelled) return
        const c = { pending: 0, approved: 0, rejected: 0, extracted: 0, photos: 0, reports: 0 }
        if (data) data.forEach(r => { if (c[r.status] !== undefined) c[r.status]++ })
        const pc = { pending: 0, approved: 0, rejected: 0 }
        if (allPhotoData) allPhotoData.forEach(r => { if (pc[r.status] !== undefined) pc[r.status]++ })
        c.photos = pc.pending
        if (repData) c.reports = repData.filter(r => r.status === 'pending').length
        setCounts(c)
        setPhotoCounts(pc)
      } catch (e) {
        if (!cancelled) setFetchError(`Count exception: ${e.message}`)
      }

      if (cancelled) return

      // Tab content
      if (tab === 'photos') {
        setPhotoFetching(true)
        const { data, error } = await supabase
          .from('product_photo_submissions').select('*')
          .eq('status', photoTab).order('created_at', { ascending: false })
        if (!cancelled) {
          if (error) setFetchError(`Photo fetch error: ${error.message}`)
          setPhotoSubs(data || [])
          setPhotoFetching(false)
        }
      } else if (tab === 'reports') {
        const { data } = await supabase
          .from('ingredient_reports').select('*').order('created_at', { ascending: false })
        if (!cancelled) setIngredientReports(data || [])
      } else {
        setFetching(true)
        setFetchError(null)
        try {
          const { data, error } = await supabase
            .from('product_submissions').select('*')
            .eq('status', tab).order('created_at', { ascending: false })
          if (!cancelled) {
            if (error) setFetchError(`DB error: ${error.message} (${error.code})`)
            setSubs(data || [])
          }
        } catch (e) {
          if (!cancelled) { setFetchError(`Exception: ${e.message}`); setSubs([]) }
        } finally {
          if (!cancelled) setFetching(false)
        }
      }
    }

    run()
    return () => { cancelled = true }
  }, [isAdmin, tab, photoTab])

  const fetchAll = async () => {
    try {
      const [{ data }, { data: allPhotoData }, { data: repData }] = await Promise.all([
        supabase.from('product_submissions').select('status'),
        supabase.from('product_photo_submissions').select('status'),
        supabase.from('ingredient_reports').select('status'),
      ])
      const c = { pending: 0, approved: 0, rejected: 0, extracted: 0, photos: 0, reports: 0 }
      if (data) data.forEach(r => { if (c[r.status] !== undefined) c[r.status]++ })
      const pc = { pending: 0, approved: 0, rejected: 0 }
      if (allPhotoData) allPhotoData.forEach(r => { if (pc[r.status] !== undefined) pc[r.status]++ })
      c.photos = pc.pending
      if (repData) c.reports = repData.filter(r => r.status === 'pending').length
      setCounts(c)
      setPhotoCounts(pc)
    } catch (e) {
      setFetchError(`Count exception: ${e.message}`)
    }
  }

  const fetchSubs = async (status) => {
    setFetching(true)
    setFetchError(null)
    try {
      const { data, error } = await supabase
        .from('product_submissions').select('*')
        .eq('status', status).order('created_at', { ascending: false })
      if (error) setFetchError(`DB error: ${error.message} (${error.code})`)
      setSubs(data || [])
    } catch (e) {
      setFetchError(`Exception: ${e.message}`)
      setSubs([])
    } finally {
      setFetching(false)
    }
  }

  const fetchReports = async () => {
    const { data } = await supabase
      .from('ingredient_reports').select('*').order('created_at', { ascending: false })
    setIngredientReports(data || [])
  }

  const handleApproveReport = async (report) => {
    const isUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(report.product_id)

    // Helper: merge existing ingredients_raw with new reported ones (no duplicates)
    const mergeRaw = (existing, incoming) => {
      if (!existing) return incoming
      const existingParts = existing.split(',').map(s => s.trim().toLowerCase())
      const newParts = incoming.split(',').map(s => s.trim()).filter(s => {
        return s && !existingParts.includes(s.toLowerCase())
      })
      return newParts.length > 0 ? existing + ', ' + newParts.join(', ') : existing
    }

    let productErr = null

    if (isUUID) {
      // Fetch current ingredients_raw, merge, then update
      const { data: current } = await supabase
        .from('ai_extracted_products')
        .select('ingredients_raw')
        .eq('id', report.product_id)
        .limit(1)

      const merged = mergeRaw(current?.[0]?.ingredients_raw, report.reported_ingredients)
      const res = await supabase
        .from('ai_extracted_products')
        .update({ ingredients_raw: merged, ingredients: [] })
        .eq('id', report.product_id)
      productErr = res.error
    } else {
      // Static/slug product — find by name
      const { data: existing } = await supabase
        .from('ai_extracted_products')
        .select('id, ingredients_raw')
        .ilike('name', report.product_name)
        .limit(1)

      if (existing && existing.length > 0) {
        const merged = mergeRaw(existing[0].ingredients_raw, report.reported_ingredients)
        const res = await supabase
          .from('ai_extracted_products')
          .update({ ingredients_raw: merged, ingredients: [] })
          .eq('id', existing[0].id)
        productErr = res.error
      } else {
        // First approval for this static product — insert new record
        const res = await supabase
          .from('ai_extracted_products')
          .insert({ name: report.product_name, ingredients_raw: report.reported_ingredients, ingredients: [] })
        productErr = res.error
      }
    }

    if (productErr) {
      alert(`Approval failed: ${productErr.message}`)
      return
    }

    await supabase
      .from('ingredient_reports')
      .update({ status: 'approved', reviewed_at: new Date().toISOString() })
      .eq('id', report.id)

    fetchAll(); fetchReports()
  }

  const handleRejectReport = async (id) => {
    const { error } = await supabase
      .from('ingredient_reports')
      .update({ status: 'rejected', reviewed_at: new Date().toISOString() })
      .eq('id', id)

    if (error) {
      alert(`Reject failed: ${error.message}`)
      return
    }

    fetchAll(); fetchReports()
  }

  const fetchPhotoSubs = async (status = 'pending') => {
    setPhotoFetching(true)
    try {
      const { data, error } = await supabase
        .from('product_photo_submissions').select('*')
        .eq('status', status).order('created_at', { ascending: false })
      if (error) setFetchError(`Photo fetch error: ${error.message}`)
      setPhotoSubs(data || [])
    } catch (e) {
      setFetchError(`Photo exception: ${e.message}`)
    } finally {
      setPhotoFetching(false)
    }
  }

  const handleApprovePhoto = async (sub) => {
    try {
      // Copy each image to product_photos
      const inserts = sub.image_urls.map(url => ({
        product_id: sub.product_id,
        image_url: url,
        added_by: sub.user_id,
        is_admin_added: false,
      }))
      const { error: insertErr } = await supabase.from('product_photos').insert(inserts)
      if (insertErr) throw new Error(insertErr.message)

      // Credit ₹1 per photo to user
      const earned = sub.image_urls.length
      await supabase.rpc('increment_earnings', { uid: sub.user_id, amount: earned })

      // Mark submission approved
      await supabase.from('product_photo_submissions').update({ status: 'approved' }).eq('id', sub.id)
      fetchAll(); fetchPhotoSubs(photoTab)
    } catch (e) {
      setFetchError(`Approve photo error: ${e.message}`)
    }
  }

  const handleRejectPhoto = async (id) => {
    await supabase.from('product_photo_submissions').update({ status: 'rejected' }).eq('id', id)
    fetchAll(); fetchPhotoSubs(photoTab)
  }

  const handleApprove = async (id) => {
    const { error } = await supabase.from('product_submissions').update({ status: 'approved' }).eq('id', id)
    if (error) { setFetchError(`Approve failed: ${error.message} — check Supabase RLS policies`); return }
    fetchAll(); fetchSubs(tab)
  }

  const handleReject = async (id) => {
    const { error } = await supabase.from('product_submissions').update({ status: 'rejected' }).eq('id', id)
    if (error) { setFetchError(`Reject failed: ${error.message}`); return }
    fetchAll(); fetchSubs(tab)
  }

  const setMsg = (id, msg) => setCardMsgs(m => ({ ...m, [id]: msg }))

  const handleSave = async (id, { text, brand, category }) => {
    if (!text?.trim()) return
    setSaving(id)
    setMsg(id, null)
    try {
      const { data: sub, error: subErr } = await supabase
        .from('product_submissions').select('*').eq('id', id).single()
      if (subErr || !sub) throw new Error('Could not load submission: ' + (subErr?.message || 'not found'))

      const images      = sub.images || []
      const productName = sub.product_name_searched || 'Unknown Product'
      const parsed      = parseIngredients(text.trim())
      const score       = calculateScore(parsed)
      const brandName   = (brand || '').trim() || productName.split(' ')[0]

      const { error: insertErr } = await supabase.from('ai_extracted_products').insert({
        name:            productName,
        brand:           brandName.slice(0, 100),
        category:        category || 'Personal Care',
        image_url:       images[0] || null,
        images:          images,
        awareness_score: score,
        summary:         `${productName} contains ${parsed.length} ingredients. ${parsed.filter(i => i.classification === 'commonly_questioned').length} are commonly questioned and ${parsed.filter(i => i.classification === 'worth_knowing').length} are worth knowing. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.`,
        fssai_note:      'Subject to applicable FSSAI regulations.',
        verdict:         verdictFromScore(score),
        recommendation:  recommendationFromScore(score),
        ingredients:     parsed,
        ingredients_raw: text.trim().slice(0, 5000),
        submission_id:   id,
        status:          'active',
      })
      if (insertErr) throw new Error('Save failed: ' + insertErr.message)

      const { error: updateErr } = await supabase
        .from('product_submissions').update({ status: 'extracted' }).eq('id', id)
      if (updateErr) throw new Error('Saved to DB but could not move to extracted: ' + updateErr.message)

      setMsg(id, { type: 'success', text: `✓ "${productName}" saved — score ${score}/100, ${parsed.length} ingredients` })
      fetchAll(); fetchSubs(tab)
    } catch (err) {
      setMsg(id, { type: 'error', text: `✕ ${err.message}` })
    } finally {
      setSaving(null)
    }
  }

  if (authLoading && !user) {
    return (
      <div style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ color: '#9ca3af', fontSize: 15 }}>Checking access…</div>
      </div>
    )
  }

  if (!isAdmin) return null

  const adminPage = tab === 'photos' ? 'photos' : tab === 'reports' ? 'reports' : tab === 'add' ? 'add' : 'products'

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: isMobile ? '20px 14px 48px' : '32px 20px 60px' }}>

      {/* Header */}
      <div style={{ marginBottom: 20 }}>
        <h1 style={{ fontFamily: 'Poppins, sans-serif', fontSize: isMobile ? 20 : 26, fontWeight: 800, color: '#0D1B2A', margin: '0 0 4px' }}>
          🔐 Admin Panel
        </h1>
        <p style={{ color: '#6b7280', fontSize: 13, margin: 0, wordBreak: 'break-all' }}>
          <strong>{user.email}</strong>
        </p>
        {fetchError && (
          <div style={{ marginTop: 8, padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, color: '#dc2626', fontWeight: 600 }}>
            ⚠️ {fetchError}
          </div>
        )}
      </div>

      {/* Top-level page switcher */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 24 }}>
        <button
          onClick={() => setTab('pending')}
          style={{
            flex: 1, padding: isMobile ? '14px 8px' : '16px 12px', borderRadius: 14, border: 'none', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center',
            background: adminPage === 'products' ? '#1B3F8A' : '#f1f5f9',
            color: adminPage === 'products' ? '#fff' : '#475569',
            boxShadow: adminPage === 'products' ? '0 4px 14px rgba(27,63,138,0.25)' : 'none',
            transition: 'all 0.15s',
          }}>
          <div style={{ fontSize: isMobile ? 22 : 26 }}>📋</div>
          <div style={{ fontSize: isMobile ? 12 : 14, fontWeight: 700, marginTop: 4 }}>Product Submissions</div>
          <div style={{ fontSize: 11, marginTop: 2, opacity: 0.8 }}>{counts.pending} pending</div>
        </button>
        <button
          onClick={() => setTab('photos')}
          style={{
            flex: 1, padding: isMobile ? '14px 8px' : '16px 12px', borderRadius: 14, border: 'none', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center',
            background: adminPage === 'photos' ? '#0ea5e9' : '#f1f5f9',
            color: adminPage === 'photos' ? '#fff' : '#475569',
            boxShadow: adminPage === 'photos' ? '0 4px 14px rgba(14,165,233,0.25)' : 'none',
            transition: 'all 0.15s',
          }}>
          <div style={{ fontSize: isMobile ? 22 : 26 }}>📸</div>
          <div style={{ fontSize: isMobile ? 12 : 14, fontWeight: 700, marginTop: 4 }}>Photo Approvals</div>
          <div style={{ fontSize: 11, marginTop: 2, opacity: 0.8 }}>{counts.photos} pending</div>
        </button>
        <button
          onClick={() => setTab('reports')}
          style={{
            flex: 1, padding: isMobile ? '14px 8px' : '16px 12px', borderRadius: 14, border: 'none', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center',
            background: adminPage === 'reports' ? '#3b82f6' : '#f1f5f9',
            color: adminPage === 'reports' ? '#fff' : '#475569',
            boxShadow: adminPage === 'reports' ? '0 4px 14px rgba(59,130,246,0.25)' : 'none',
            transition: 'all 0.15s',
          }}>
          <div style={{ fontSize: isMobile ? 22 : 26 }}>🚩</div>
          <div style={{ fontSize: isMobile ? 12 : 14, fontWeight: 700, marginTop: 4 }}>Ingredient Reports</div>
          <div style={{ fontSize: 11, marginTop: 2, opacity: 0.8 }}>{counts.reports} pending</div>
        </button>
        <button
          onClick={() => setTab('add')}
          style={{
            flex: 1, padding: isMobile ? '14px 8px' : '16px 12px', borderRadius: 14, border: 'none', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center',
            background: adminPage === 'add' ? '#16a34a' : '#f1f5f9',
            color: adminPage === 'add' ? '#fff' : '#475569',
            boxShadow: adminPage === 'add' ? '0 4px 14px rgba(22,163,74,0.25)' : 'none',
            transition: 'all 0.15s',
          }}>
          <div style={{ fontSize: isMobile ? 22 : 26 }}>🗂️</div>
          <div style={{ fontSize: isMobile ? 12 : 14, fontWeight: 700, marginTop: 4 }}>Manage Products</div>
          <div style={{ fontSize: 11, marginTop: 2, opacity: 0.8 }}>add · delete</div>
        </button>
      </div>

      {/* ── PHOTO APPROVALS PAGE ── */}
      {adminPage === 'photos' && (
        <>
          <h2 style={{ fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827', marginBottom: 14 }}>
            📸 Photo Approvals
          </h2>

          {/* Photo status counts */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16 }}>
            {[
              { key: 'pending', label: 'Pending', color: '#f59e0b', bg: '#fef3c7' },
              { key: 'approved', label: 'Approved', color: '#16a34a', bg: '#f0fdf4' },
              { key: 'rejected', label: 'Rejected', color: '#dc2626', bg: '#fef2f2' },
            ].map(({ key, label, color, bg }) => (
              <button key={key} onClick={() => setPhotoTab(key)}
                style={{ flex: 1, borderRadius: 10, border: `1.5px solid ${photoTab === key ? color + '88' : '#e5e7eb'}`, background: photoTab === key ? bg : '#f9fafb', padding: isMobile ? '8px 4px' : '10px 6px', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center' }}>
                <div style={{ fontSize: isMobile ? 17 : 20, fontWeight: 800, color }}>{photoCounts[key]}</div>
                <div style={{ fontSize: isMobile ? 9 : 11, color: '#6b7280', fontWeight: 600, marginTop: 2 }}>{label}</div>
              </button>
            ))}
          </div>

          {/* Photo tab strip */}
          <div style={{ display: 'flex', borderBottom: '1.5px solid #e5e7eb', marginBottom: 18 }}>
            {[
              { key: 'pending', label: 'Pending', color: '#f59e0b' },
              { key: 'approved', label: 'Saved Photos', color: '#16a34a' },
              { key: 'rejected', label: 'Rejected', color: '#dc2626' },
            ].map(({ key, label, color }) => (
              <button key={key} onClick={() => setPhotoTab(key)}
                style={{ flexShrink: 0, background: 'none', border: 'none', borderBottom: photoTab === key ? `2.5px solid ${color}` : '2.5px solid transparent', color: photoTab === key ? color : '#6b7280', fontWeight: photoTab === key ? 700 : 500, fontSize: isMobile ? 13 : 14, padding: isMobile ? '8px 14px' : '8px 20px', cursor: 'pointer', fontFamily: 'inherit', marginBottom: -1.5, whiteSpace: 'nowrap' }}>
                {label}
                <span style={{ background: photoTab === key ? '#f3f4f6' : '#f3f4f6', color: photoTab === key ? color : '#9ca3af', borderRadius: 99, padding: '1px 7px', fontSize: 11, fontWeight: 700, marginLeft: 6 }}>{photoCounts[key]}</span>
              </button>
            ))}
          </div>

          {photoFetching ? (
            <div style={{ textAlign: 'center', padding: '48px 0', color: '#9ca3af', fontSize: 15 }}>Loading…</div>
          ) : photoSubs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px 0' }}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>📸</div>
              <p style={{ color: '#9ca3af', fontSize: 15 }}>No pending photo submissions</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
              {photoSubs.map(sub => (
                <div key={sub.id} style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 14, overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.05)' }}>
                  {/* Images preview */}
                  <div style={{ display: 'flex', gap: 4, padding: 10, background: '#f9fafb', flexWrap: 'wrap' }}>
                    {(sub.image_urls || []).map((url, i) => (
                      <a key={i} href={url} target="_blank" rel="noreferrer" style={{ flexShrink: 0 }}>
                        <img src={url} alt="" style={{ width: 80, height: 80, objectFit: 'cover', borderRadius: 8, border: '1px solid #e5e7eb', display: 'block' }} />
                      </a>
                    ))}
                  </div>
                  <div style={{ padding: '12px 14px' }}>
                    <p style={{ margin: '0 0 3px', fontWeight: 700, fontSize: 14, color: '#111827' }}>
                      {sub.product_name || sub.product_id}
                    </p>
                    <p style={{ margin: '0 0 6px', fontSize: 12, color: '#9ca3af' }}>{formatDate(sub.created_at)}</p>
                    <div style={{ display: 'flex', gap: 6, marginBottom: 10, flexWrap: 'wrap' }}>
                      <span style={{ fontSize: 11, background: '#f0fdf4', color: '#16a34a', border: '1px solid #bbf7d0', borderRadius: 99, padding: '2px 8px', fontWeight: 600 }}>
                        {sub.image_urls?.length || 0} photo(s)
                      </span>
                      {sub.upi_or_mobile && (
                        <span style={{ fontSize: 11, background: '#eff6ff', color: '#1d4ed8', border: '1px solid #bfdbfe', borderRadius: 99, padding: '2px 8px', fontWeight: 600 }}>
                          💳 {sub.upi_or_mobile}
                        </span>
                      )}
                      <span style={{ fontSize: 11, background: '#fefce8', color: '#ca8a04', border: '1px solid #fde68a', borderRadius: 99, padding: '2px 8px', fontWeight: 600 }}>
                        Reward: ₹1
                      </span>
                    </div>
                    {photoTab === 'pending' && (
                      <div style={{ display: 'flex', gap: 8 }}>
                        <button onClick={() => handleApprovePhoto(sub)}
                          style={{ flex: 1, background: '#16a34a', color: '#fff', border: 'none', borderRadius: 10, padding: '10px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                          ✓ Approve + Save
                        </button>
                        <button onClick={() => handleRejectPhoto(sub.id)}
                          style={{ flex: 1, background: '#fff', color: '#dc2626', border: '1.5px solid #dc2626', borderRadius: 10, padding: '10px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                          ✕ Reject
                        </button>
                      </div>
                    )}
                    {photoTab === 'approved' && (
                      <div style={{ padding: '8px 12px', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 8, fontSize: 12, fontWeight: 700, color: '#16a34a' }}>
                        ✓ Approved · Photos saved · ₹1 credited
                      </div>
                    )}
                    {photoTab === 'rejected' && (
                      <div style={{ padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, fontWeight: 700, color: '#dc2626', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8 }}>
                        <span>✕ Rejected</span>
                        <button onClick={() => handleApprovePhoto(sub)}
                          style={{ background: '#16a34a', color: '#fff', border: 'none', borderRadius: 7, padding: '5px 12px', fontSize: 12, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                          Re-approve
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* ── INGREDIENT REPORTS PAGE ── */}
      {adminPage === 'reports' && (
        <>
          <h2 style={{ fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827', marginBottom: 14 }}>
            🚩 Ingredient Reports
          </h2>
          {ingredientReports.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px 0' }}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>🚩</div>
              <p style={{ color: '#9ca3af', fontSize: 15 }}>No ingredient reports yet</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {ingredientReports.map(report => (
                <div key={report.id} style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 12, padding: '14px 16px', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8, marginBottom: 8 }}>
                    <div>
                      <p style={{ margin: 0, fontWeight: 700, fontSize: 14, color: '#111827' }}>{report.product_name}</p>
                      <p style={{ margin: '3px 0 0', fontSize: 11, color: '#9ca3af' }}>{formatDate(report.created_at)}</p>
                    </div>
                    <span style={{
                      flexShrink: 0,
                      background: report.status === 'pending' ? '#fef3c7' : report.status === 'approved' ? '#f0fdf4' : '#fef2f2',
                      color: report.status === 'pending' ? '#d97706' : report.status === 'approved' ? '#16a34a' : '#dc2626',
                      fontSize: 11, fontWeight: 700, padding: '4px 10px', borderRadius: 99, textTransform: 'uppercase', letterSpacing: '0.04em',
                    }}>
                      {report.status}
                    </span>
                  </div>
                  {report.user_email && (
                    <p style={{ margin: '0 0 8px', fontSize: 12, color: '#6b7280' }}>{report.user_email}</p>
                  )}
                  <div style={{ marginBottom: 8 }}>
                    <p style={{ margin: '0 0 4px', fontSize: 12, fontWeight: 600, color: '#374151' }}>Reported ingredients:</p>
                    <div style={{ background: '#f3f4f6', borderRadius: 7, padding: '8px 12px', fontSize: 12, color: '#374151', fontFamily: 'monospace', whiteSpace: 'pre-wrap', wordBreak: 'break-word', border: '1px solid #e5e7eb' }}>
                      {report.reported_ingredients}
                    </div>
                  </div>
                  {report.reason && (
                    <p style={{ margin: '0 0 10px', fontSize: 12, color: '#6b7280' }}>
                      <strong>Reason:</strong> {report.reason}
                    </p>
                  )}
                  {report.status === 'pending' && (
                    <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
                      <button
                        onClick={() => handleApproveReport(report)}
                        style={{ flex: 1, background: '#16a34a', color: '#fff', border: 'none', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                        ✓ Approve
                      </button>
                      <button
                        onClick={() => handleRejectReport(report.id)}
                        style={{ flex: 1, background: '#fff', color: '#dc2626', border: '1.5px solid #dc2626', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
                        ✕ Reject
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {/* ── MANAGE PRODUCTS PAGE ── */}
      {adminPage === 'add' && (
        <>
          <h2 style={{ fontFamily: 'Poppins,sans-serif', fontSize: 16, fontWeight: 700, color: '#111827', marginBottom: 20 }}>
            Manage Products
          </h2>
          <AddProductForm isMobile={isMobile} />
          <div style={{ marginTop: 32, borderTop: '2px dashed #fee2e2', paddingTop: 28 }}>
            <DeleteProductSection isMobile={isMobile} />
          </div>
        </>
      )}

      {/* ── PRODUCT SUBMISSIONS PAGE ── */}
      {adminPage === 'products' && (
        <>
          {/* Stats bar */}
          <div style={{ display: 'flex', gap: 8, marginBottom: 16, overflowX: 'auto' }}>
            {STATUS_TABS.filter(s => s !== 'photos' && s !== 'reports').map(s => (
              <button key={s} onClick={() => setTab(s)}
                style={{ flexShrink: 0, flex: 1, minWidth: 64, background: tab === s ? STATUS_BG[s] : '#f9fafb', border: `1.5px solid ${tab === s ? STATUS_COLOR[s] + '66' : '#e5e7eb'}`, borderRadius: 10, padding: isMobile ? '8px 4px' : '10px 6px', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center' }}>
                <div style={{ fontSize: isMobile ? 17 : 20, fontWeight: 800, color: STATUS_COLOR[s] }}>{counts[s]}</div>
                <div style={{ fontSize: isMobile ? 9 : 11, color: '#6b7280', textTransform: 'capitalize', fontWeight: 600, marginTop: 2 }}>{s}</div>
              </button>
            ))}
          </div>

          {/* Tab strip */}
          <div style={{ display: 'flex', borderBottom: '1.5px solid #e5e7eb', marginBottom: 20, overflowX: 'auto' }}>
            {STATUS_TABS.filter(s => s !== 'photos' && s !== 'reports').map(s => (
              <button key={s} onClick={() => setTab(s)}
                style={{ flexShrink: 0, background: 'none', border: 'none', borderBottom: tab === s ? `2.5px solid ${STATUS_COLOR[s]}` : '2.5px solid transparent', color: tab === s ? STATUS_COLOR[s] : '#6b7280', fontWeight: tab === s ? 700 : 500, fontSize: isMobile ? 13 : 14, padding: isMobile ? '8px 14px' : '8px 20px', cursor: 'pointer', textTransform: 'capitalize', fontFamily: 'inherit', marginBottom: -1.5, whiteSpace: 'nowrap' }}>
                {s}
                <span style={{ background: tab === s ? STATUS_BG[s] : '#f3f4f6', color: tab === s ? STATUS_COLOR[s] : '#9ca3af', borderRadius: 99, padding: '1px 7px', fontSize: 11, fontWeight: 700, marginLeft: 6 }}>{counts[s]}</span>
              </button>
            ))}
          </div>

          {/* Submissions grid */}
          {fetching ? (
            <div style={{ textAlign: 'center', padding: '48px 0', color: '#9ca3af', fontSize: 15 }}>Loading…</div>
          ) : subs.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '48px 0' }}>
              <div style={{ fontSize: 48, marginBottom: 12 }}>📭</div>
              <p style={{ color: '#9ca3af', fontSize: 15 }}>No {tab} submissions</p>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(auto-fill, minmax(300px, 1fr))', gap: 16 }}>
              {subs.map(s => (
                <SubmissionCard key={s.id} sub={s}
                  onApprove={handleApprove}
                  onReject={handleReject}
                  onSave={handleSave}
                  saving={saving}
                  cardMsg={cardMsgs[s.id] || null}
                />
              ))}
            </div>
          )}
        </>
      )}

    </div>
  )
}
