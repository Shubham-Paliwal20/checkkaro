import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'
const STATUS_TABS  = ['pending', 'approved', 'rejected', 'extracted']
const STATUS_COLOR = { pending: '#f59e0b', approved: '#16a34a', rejected: '#dc2626', extracted: '#7c3aed' }
const STATUS_BG    = { pending: '#fef3c7', approved: '#f0fdf4', rejected: '#fef2f2', extracted: '#f5f3ff' }

const CATEGORIES = ['Personal Care', 'Skincare', 'Haircare', 'Food & Beverages', 'Supplements', 'Baby Care', 'Other']

// Parse "Water, Glycerin, Sodium Laureth Sulfate..." into ingredient objects
function parseIngredients(text) {
  return text
    .split(/[,;]/)
    .map(s => s.trim())
    .filter(s => s.length > 0)
    .map(name => ({
      name: name.slice(0, 100),
      aliases: '',
      classification: 'generally_recognised',
      one_line_note: '',
      regulatory_note: '',
    }))
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
  const [score,       setScore]       = useState(70)

  const isSaving = saving === sub.id
  const parsed = ingredients.trim() ? parseIngredients(ingredients) : []

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

        {/* Info rows */}
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

        {/* Approved — manual form, saves directly to Supabase */}
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

            {/* Score */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
              <label style={{ fontSize: 12, color: '#6b7280', fontWeight: 600, whiteSpace: 'nowrap' }}>Score (0–100):</label>
              <input
                type="number" min={0} max={100}
                value={score}
                onChange={e => setScore(e.target.value)}
                style={{ ...field, width: 72 }}
                disabled={isSaving}
              />
              <span style={{ fontSize: 12, color: '#6b7280' }}>
                {score >= 80 ? '🟢 Clean' : score >= 60 ? '🟡 Average' : score >= 40 ? '🟠 Review' : '🔴 Caution'}
              </span>
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
              {parsed.length > 0 && (
                <p style={{ margin: '3px 0 0', fontSize: 11, color: '#9ca3af' }}>
                  {parsed.length} ingredients detected
                </p>
              )}
            </div>

            {/* Save button */}
            <button
              onClick={() => onSave(sub.id, { text: ingredients, brand, category, score })}
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

        {sub.status === 'extracted' && (
          <div style={{ fontSize: 13, color: '#7c3aed', fontWeight: 600, paddingTop: 4 }}>
            ✓ Added to database
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
  const [counts,     setCounts]     = useState({ pending: 0, approved: 0, rejected: 0, extracted: 0 })
  const [fetching,   setFetching]   = useState(false)
  const [saving,     setSaving]     = useState(null)
  const [cardMsgs,   setCardMsgs]   = useState({})
  const [fetchError, setFetchError] = useState(null)

  const isAdmin = user?.email === ADMIN_EMAIL

  useEffect(() => {
    if (!authLoading && !isAdmin) navigate('/')
  }, [user, authLoading, isAdmin, navigate])

  useEffect(() => {
    if (isAdmin) { fetchAll(); fetchSubs(tab) }
  }, [isAdmin, tab])

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

  const fetchAll = async () => {
    try {
      const { data, error } = await supabase.from('product_submissions').select('status')
      if (error) { setFetchError(`Count error: ${error.message}`); return }
      if (!data) return
      const c = { pending: 0, approved: 0, rejected: 0, extracted: 0 }
      data.forEach(r => { if (c[r.status] !== undefined) c[r.status]++ })
      setCounts(c)
    } catch (e) {
      setFetchError(`Count exception: ${e.message}`)
    }
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

  // Save directly to Supabase — no backend, no AI, no external API calls
  const handleSave = async (id, { text, brand, category, score }) => {
    if (!text?.trim()) return
    setSaving(id)
    setMsg(id, null)
    try {
      const { data: sub, error: subErr } = await supabase
        .from('product_submissions').select('*').eq('id', id).single()
      if (subErr || !sub) throw new Error('Could not load submission: ' + (subErr?.message || 'not found'))

      const images     = sub.images || []
      const productName = sub.product_name_searched || 'Unknown Product'
      const parsed     = parseIngredients(text.trim())
      const numScore   = Math.max(0, Math.min(100, parseInt(score) || 70))
      const brandName  = (brand || '').trim() || productName.split(' ')[0]

      const { error: insertErr } = await supabase.from('ai_extracted_products').insert({
        name:            productName,
        brand:           brandName.slice(0, 100),
        category:        category || 'Personal Care',
        image_url:       images[0] || null,
        images:          images,
        awareness_score: numScore,
        summary:         `${productName} contains ${parsed.length} ingredients. This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice.`,
        fssai_note:      'Subject to applicable FSSAI regulations.',
        verdict:         verdictFromScore(numScore),
        recommendation:  recommendationFromScore(numScore),
        ingredients:     parsed,
        ingredients_raw: text.trim().slice(0, 5000),
        submission_id:   id,
        status:          'active',
      })
      if (insertErr) throw new Error('Save failed: ' + insertErr.message)

      await supabase.from('product_submissions').update({ status: 'extracted' }).eq('id', id)

      setMsg(id, { type: 'success', text: `✓ "${productName}" saved — ${parsed.length} ingredients, score ${numScore}/100` })
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

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: isMobile ? '20px 14px 48px' : '32px 20px 60px' }}>

      <div style={{ marginBottom: isMobile ? 16 : 28 }}>
        <h1 style={{ fontFamily: 'Poppins, sans-serif', fontSize: isMobile ? 20 : 26, fontWeight: 800, color: '#0D1B2A', margin: '0 0 4px' }}>
          🔐 Admin Panel
        </h1>
        <p style={{ color: '#6b7280', fontSize: 13, margin: 0, wordBreak: 'break-all' }}>
          Review submissions · <strong>{user.email}</strong>
        </p>
        {fetchError && (
          <div style={{ marginTop: 8, padding: '8px 12px', background: '#fef2f2', border: '1px solid #fecaca', borderRadius: 8, fontSize: 12, color: '#dc2626', fontWeight: 600 }}>
            ⚠️ {fetchError}
          </div>
        )}
      </div>

      {/* Stats */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 20 }}>
        {STATUS_TABS.map(s => (
          <button key={s} onClick={() => setTab(s)}
            style={{ flex: 1, background: tab === s ? STATUS_BG[s] : '#f9fafb', border: `1.5px solid ${tab === s ? STATUS_COLOR[s] + '66' : '#e5e7eb'}`, borderRadius: 12, padding: isMobile ? '10px 4px' : '12px 8px', cursor: 'pointer', fontFamily: 'inherit', textAlign: 'center' }}>
            <div style={{ fontSize: isMobile ? 20 : 22, fontWeight: 800, color: STATUS_COLOR[s] }}>{counts[s]}</div>
            <div style={{ fontSize: isMobile ? 10 : 12, color: '#6b7280', textTransform: 'capitalize', fontWeight: 600, marginTop: 2 }}>{s}</div>
          </button>
        ))}
      </div>

      {/* Tab strip */}
      <div style={{ display: 'flex', borderBottom: '1.5px solid #e5e7eb', marginBottom: 20, overflowX: 'auto' }}>
        {STATUS_TABS.map(s => (
          <button key={s} onClick={() => setTab(s)}
            style={{ flexShrink: 0, background: 'none', border: 'none', borderBottom: tab === s ? `2.5px solid ${STATUS_COLOR[s]}` : '2.5px solid transparent', color: tab === s ? STATUS_COLOR[s] : '#6b7280', fontWeight: tab === s ? 700 : 500, fontSize: isMobile ? 13 : 14, padding: isMobile ? '8px 14px' : '8px 20px', cursor: 'pointer', textTransform: 'capitalize', fontFamily: 'inherit', marginBottom: -1.5, whiteSpace: 'nowrap' }}>
            {s}
            <span style={{ background: tab === s ? STATUS_BG[s] : '#f3f4f6', color: tab === s ? STATUS_COLOR[s] : '#9ca3af', borderRadius: 99, padding: '1px 7px', fontSize: 11, fontWeight: 700, marginLeft: 6 }}>{counts[s]}</span>
          </button>
        ))}
      </div>

      {/* Grid */}
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
    </div>
  )
}
