import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL  = 'shubhampaliwal5@gmail.com'
const STATUS_TABS  = ['pending', 'approved', 'rejected', 'extracted']
const STATUS_COLOR = { pending: '#f59e0b', approved: '#16a34a', rejected: '#dc2626', extracted: '#7c3aed' }
const STATUS_BG    = { pending: '#fef3c7', approved: '#f0fdf4', rejected: '#fef2f2', extracted: '#f5f3ff' }

// ── Client-side Claude (Anthropic) helpers — no backend needed ───────────────
const CLAUDE_KEY   = import.meta.env.VITE_ANTHROPIC_API_KEY || ''
const CLAUDE_URL   = 'https://api.anthropic.com/v1/messages'
const CLAUDE_MODEL = 'claude-3-5-haiku-20241022'
const CLAUDE_HDR   = {
  'x-api-key': CLAUDE_KEY,
  'anthropic-version': '2023-06-01',
  'anthropic-dangerous-direct-browser-access': 'true',
  'content-type': 'application/json',
}

const CLASSIFICATION_SYSTEM = `You are an ingredient classification specialist for CheckKaro, an Indian consumer awareness platform.
Classification: generally_recognised | worth_knowing | commonly_questioned
Score from 100: worth_knowing -8pts each, commonly_questioned -20pts each, banned in EU/Canada -15pts each.
Language rules: never use safe/unsafe/dangerous/toxic/cancer. Use: generally recognised / worth knowing / commonly questioned.
End summary with: "This information is for general awareness based on publicly available regulatory data. It is not a health assessment or medical advice."`

async function claudeVision(imageUrl, productName) {
  if (!CLAUDE_KEY) return 'NOT_VISIBLE'
  try {
    const resp = await fetch(CLAUDE_URL, {
      method: 'POST',
      headers: { ...CLAUDE_HDR, 'x-api-key': CLAUDE_KEY },
      body: JSON.stringify({
        model: CLAUDE_MODEL,
        max_tokens: 1024,
        messages: [{
          role: 'user',
          content: [
            { type: 'image', source: { type: 'url', url: imageUrl } },
            { type: 'text', text: `This is a "${productName}" product label. Extract ONLY the ingredients list text exactly as printed on the label. Return ONLY the raw text. If the ingredients section is not visible, return: NOT_VISIBLE` },
          ],
        }],
      }),
    })
    const data = await resp.json()
    if (!resp.ok) return 'NOT_VISIBLE'
    return data.content?.[0]?.text?.trim() || 'NOT_VISIBLE'
  } catch { return 'NOT_VISIBLE' }
}

async function claudeAnalyze(productName, ingredientsText) {
  if (!CLAUDE_KEY) throw new Error('VITE_ANTHROPIC_API_KEY not set — add it in Vercel Dashboard → Settings → Environment Variables')
  const resp = await fetch(CLAUDE_URL, {
    method: 'POST',
    headers: { ...CLAUDE_HDR, 'x-api-key': CLAUDE_KEY },
    body: JSON.stringify({
      model: CLAUDE_MODEL,
      max_tokens: 8000,
      system: CLASSIFICATION_SYSTEM,
      messages: [{
        role: 'user',
        content: `Product: ${productName}\nIngredients from label: ${ingredientsText}\n\nClassify each ingredient. Return ONLY valid JSON, no markdown:\n{"brand":"string","category":"string","awareness_score":75,"summary":"string","fssai_note":"string","verdict":"string","recommendation":"string","ingredients":[{"name":"string","aliases":"string","classification":"generally_recognised","one_line_note":"string","regulatory_note":"string"}]}`,
      }],
    }),
  })
  const data = await resp.json()
  if (!resp.ok) throw new Error(`Claude: ${data.error?.message || resp.status}`)
  let text = data.content?.[0]?.text || ''
  text = text.trim()
  if (text.startsWith('```json')) text = text.slice(7)
  if (text.startsWith('```')) text = text.slice(3)
  if (text.endsWith('```')) text = text.slice(0, -3)
  return JSON.parse(text.trim())
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
  const [idx, setIdx]     = useState(0)
  const touchStartX       = useRef(null)

  const prev = () => setIdx(i => (i - 1 + imgs.length) % imgs.length)
  const next = () => setIdx(i => (i + 1) % imgs.length)

  const onTouchStart = e => { touchStartX.current = e.touches[0].clientX }
  const onTouchEnd   = e => {
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

      {/* Prev / Next arrows */}
      {imgs.length > 1 && (
        <>
          <button onClick={prev} style={{ position: 'absolute', left: 6, top: '50%', transform: 'translateY(-50%)', background: 'rgba(0,0,0,0.45)', border: 'none', color: '#fff', borderRadius: '50%', width: 32, height: 32, fontSize: 16, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', touchAction: 'manipulation' }}>‹</button>
          <button onClick={next} style={{ position: 'absolute', right: 6, top: '50%', transform: 'translateY(-50%)', background: 'rgba(0,0,0,0.45)', border: 'none', color: '#fff', borderRadius: '50%', width: 32, height: 32, fontSize: 16, cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', touchAction: 'manipulation' }}>›</button>
        </>
      )}

      {/* Dots */}
      {imgs.length > 1 && (
        <div style={{ position: 'absolute', bottom: 8, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 5 }}>
          {imgs.map((_, i) => (
            <button key={i} onClick={() => setIdx(i)}
              style={{ width: i === idx ? 20 : 7, height: 7, borderRadius: 99, border: 'none', cursor: 'pointer', background: i === idx ? '#FF9933' : 'rgba(255,255,255,0.5)', padding: 0, transition: 'all 0.2s' }} />
          ))}
        </div>
      )}

      {/* Full size link */}
      <a href={imgs[idx]} target="_blank" rel="noreferrer"
        style={{ position: 'absolute', top: 8, right: 8, background: 'rgba(0,0,0,0.5)', color: '#fff', borderRadius: 6, padding: '4px 10px', fontSize: 11, textDecoration: 'none', fontWeight: 600 }}>
        Full ↗
      </a>

      {/* Counter */}
      <span style={{ position: 'absolute', top: 8, left: 8, background: 'rgba(0,0,0,0.5)', color: '#fff', borderRadius: 6, padding: '3px 8px', fontSize: 11, fontWeight: 600 }}>
        {idx + 1}/{imgs.length}
      </span>
    </div>
  )
}

function SubmissionCard({ sub, onApprove, onReject, onExtract, extracting, cardMsg, forceManualOpen }) {
  const imgs = sub.images || []
  const [showManual, setShowManual] = useState(false)
  const [manualText, setManualText] = useState('')
  const textareaRef = useRef(null)

  useEffect(() => {
    if (forceManualOpen) {
      setShowManual(true)
      setTimeout(() => textareaRef.current?.focus(), 100)
    }
  }, [forceManualOpen])

  return (
    <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 14, overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.05)' }}>
      <ImageViewer imgs={imgs} />

      <div style={{ padding: '14px 16px' }}>
        {/* Header row */}
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: 7, marginBottom: (sub.status === 'pending' || sub.status === 'approved') ? 14 : 4 }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
            <span style={{ fontSize: 15, flexShrink: 0, marginTop: 1 }}>📧</span>
            <span style={{ fontSize: 13, color: '#374151', wordBreak: 'break-all', lineHeight: 1.4 }}>{sub.email || '—'}</span>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
            <span style={{ fontSize: 15, flexShrink: 0, marginTop: 1 }}>💳</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: '#1d4ed8', wordBreak: 'break-all', lineHeight: 1.4 }}>{sub.contact}</span>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 15, flexShrink: 0 }}>🖼️</span>
            <span style={{ fontSize: 13, color: '#6b7280' }}>{imgs.length} image{imgs.length !== 1 ? 's' : ''}</span>
          </div>
        </div>

        {sub.status === 'pending' && (
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => onApprove(sub.id)}
              style={{ flex: 1, background: '#16a34a', color: '#fff', border: 'none', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit', touchAction: 'manipulation' }}>
              ✓ Approve
            </button>
            <button onClick={() => onReject(sub.id)}
              style={{ flex: 1, background: '#fff', color: '#dc2626', border: '1.5px solid #dc2626', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit', touchAction: 'manipulation' }}>
              ✕ Reject
            </button>
          </div>
        )}

        {sub.status === 'approved' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {/* AI extract from image */}
            <button
              onClick={() => onExtract(sub.id, null)}
              disabled={extracting != null}
              style={{ width: '100%', background: extracting === sub.id ? '#e9d5ff' : extracting != null ? '#f3f4f6' : '#7c3aed', color: extracting != null ? '#9ca3af' : '#fff', border: 'none', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: extracting != null ? 'not-allowed' : 'pointer', fontFamily: 'inherit', touchAction: 'manipulation', transition: 'background 0.2s' }}>
              {extracting === sub.id && !showManual ? '⏳ Working…' : '🤖 Extract from Image (AI)'}
            </button>

            {/* Manual toggle */}
            <button
              onClick={() => setShowManual(v => !v)}
              style={{ width: '100%', background: 'none', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '8px 0', fontSize: 13, fontWeight: 600, color: '#6b7280', cursor: 'pointer', fontFamily: 'inherit', touchAction: 'manipulation' }}>
              {showManual ? '▲ Hide manual entry' : '✏️ Enter ingredients manually'}
            </button>

            {showManual && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                <p style={{ margin: 0, fontSize: 12, color: '#6b7280', lineHeight: 1.4 }}>
                  Paste the ingredients list exactly as printed on the label:
                </p>
                <textarea
                  ref={textareaRef}
                  value={manualText}
                  onChange={e => setManualText(e.target.value)}
                  placeholder="e.g. Water, Glycerin, Sodium Laureth Sulfate, Cocamidopropyl Betaine..."
                  rows={5}
                  style={{ width: '100%', boxSizing: 'border-box', border: '1.5px solid #d1d5db', borderRadius: 8, padding: '10px 12px', fontSize: 13, fontFamily: 'inherit', resize: 'vertical', outline: 'none', color: '#111827' }}
                />
                <button
                  onClick={() => onExtract(sub.id, manualText)}
                  disabled={extracting != null || !manualText.trim()}
                  style={{ width: '100%', background: extracting != null || !manualText.trim() ? '#f3f4f6' : '#059669', color: extracting != null || !manualText.trim() ? '#9ca3af' : '#fff', border: 'none', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: extracting != null || !manualText.trim() ? 'not-allowed' : 'pointer', fontFamily: 'inherit', touchAction: 'manipulation', transition: 'background 0.2s' }}>
                  {extracting === sub.id ? '⏳ Working…' : '✓ Analyse & Add to DB'}
                </button>
              </div>
            )}

            {/* Inline status message — visible right here in the card */}
            {cardMsg && (
              <div style={{ marginTop: 4, padding: '10px 14px', borderRadius: 8, fontSize: 13, fontWeight: 600, lineHeight: 1.5,
                background: cardMsg.type === 'success' ? '#f0fdf4' : cardMsg.type === 'info' ? '#fefce8' : '#fef2f2',
                color: cardMsg.type === 'success' ? '#16a34a' : cardMsg.type === 'info' ? '#92400e' : '#dc2626',
                border: `1px solid ${cardMsg.type === 'success' ? '#bbf7d0' : cardMsg.type === 'info' ? '#fde68a' : '#fecaca'}` }}>
                {cardMsg.text}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function Admin() {
  const { user, loading: authLoading } = useAuth()
  const navigate  = useNavigate()
  const isMobile  = useIsMobile()
  const [tab,        setTab]        = useState('pending')
  const [subs,       setSubs]       = useState([])
  const [counts,     setCounts]     = useState({ pending: 0, approved: 0, rejected: 0, extracted: 0 })
  const [fetching,      setFetching]      = useState(false)
  const [extracting,    setExtracting]    = useState(null)
  const [cardMsgs,      setCardMsgs]      = useState({})
  const [openManualIds, setOpenManualIds] = useState(new Set())
  const [fetchError,    setFetchError]    = useState(null)

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

  const handleExtract = async (id, manualText = null) => {
    setExtracting(id)
    setMsg(id, null)
    try {
      // Get submission directly from Supabase — no backend needed
      const { data: sub, error: subErr } = await supabase
        .from('product_submissions').select('*').eq('id', id).single()
      if (subErr || !sub) throw new Error('Could not load submission: ' + (subErr?.message || 'not found'))

      const images = sub.images || []
      const productName = sub.product_name_searched || 'Unknown Product'
      let ingredientsText = manualText?.trim() || ''

      // ── Vision: read ingredients from image ──────────────────────────────
      if (!ingredientsText) {
        if (!images.length) throw new Error('No images in submission. Use "Enter manually" option.')
        if (!CLAUDE_KEY) throw new Error('VITE_ANTHROPIC_API_KEY not configured in Vercel environment variables.')
        const ordered = images.length > 1 ? [images[1], images[0], ...images.slice(2)] : images
        setMsg(id, { type: 'info', text: '⏳ Reading label with Claude Vision…' })
        for (const url of ordered) {
          const t = await claudeVision(url, productName)
          if (t && t !== 'NOT_VISIBLE') { ingredientsText = t; break }
        }
        if (!ingredientsText) {
          // Auto-open manual entry form and show a helpful prompt
          setOpenManualIds(s => new Set([...s, id]))
          throw new Error('AI couldn\'t read ingredients from the photos (likely front-label shot). The text box below is now open — paste the ingredients from the back label.')
        }
      }

      // ── Analysis: classify ingredients with Claude ────────────────────────
      setMsg(id, { type: 'info', text: '⏳ Classifying ingredients with Claude AI…' })
      const analysis = await claudeAnalyze(productName, ingredientsText)

      // ── Save directly to Supabase ─────────────────────────────────────────
      setMsg(id, { type: 'info', text: '⏳ Saving to database…' })
      const productData = {
        name: productName,
        brand: (analysis.brand || 'Unknown').slice(0, 100),
        category: (analysis.category || 'General').slice(0, 100),
        image_url: images[0] || null,
        awareness_score: Math.max(0, Math.min(100, parseInt(analysis.awareness_score) || 50)),
        summary: (analysis.summary || '').slice(0, 2000),
        fssai_note: (analysis.fssai_note || '').slice(0, 500),
        verdict: (analysis.verdict || '').slice(0, 200),
        recommendation: (analysis.recommendation || '').slice(0, 500),
        ingredients: analysis.ingredients || [],
        ingredients_raw: ingredientsText.slice(0, 5000),
        submission_id: id,
      }

      const { error: insertErr } = await supabase.from('ai_extracted_products').insert(productData)
      if (insertErr) throw new Error('Save failed: ' + insertErr.message)

      await supabase.from('product_submissions').update({ status: 'extracted' }).eq('id', id)

      setMsg(id, { type: 'success', text: `✓ Added "${productName}" — score ${analysis.awareness_score}, ${(analysis.ingredients || []).length} ingredients` })
      fetchAll(); fetchSubs(tab)

    } catch (err) {
      setMsg(id, { type: 'error', text: `✕ ${err.message || 'Unknown error'}` })
      console.error('[Extract error]', err)
    } finally {
      setExtracting(null)
    }
  }

  // Only block render while auth is genuinely unknown (no user resolved yet).
  // If user is already in context the isAdmin check is instant — no spinner needed.
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

      {/* Header */}
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
            style={{ flex: 1, background: tab === s ? STATUS_BG[s] : '#f9fafb', border: `1.5px solid ${tab === s ? STATUS_COLOR[s] + '66' : '#e5e7eb'}`, borderRadius: 12, padding: isMobile ? '10px 4px' : '12px 8px', cursor: 'pointer', fontFamily: 'inherit', transition: 'all 0.15s', textAlign: 'center' }}>
            <div style={{ fontSize: isMobile ? 20 : 22, fontWeight: 800, color: STATUS_COLOR[s] }}>{counts[s]}</div>
            <div style={{ fontSize: isMobile ? 10 : 12, color: '#6b7280', textTransform: 'capitalize', fontWeight: 600, marginTop: 2 }}>{s}</div>
          </button>
        ))}
      </div>

      {/* Tab strip */}
      <div style={{ display: 'flex', borderBottom: '1.5px solid #e5e7eb', marginBottom: 20, overflowX: 'auto', WebkitOverflowScrolling: 'touch' }}>
        {STATUS_TABS.map(s => (
          <button key={s} onClick={() => setTab(s)}
            style={{ flexShrink: 0, background: 'none', border: 'none', borderBottom: tab === s ? `2.5px solid ${STATUS_COLOR[s]}` : '2.5px solid transparent', color: tab === s ? STATUS_COLOR[s] : '#6b7280', fontWeight: tab === s ? 700 : 500, fontSize: isMobile ? 13 : 14, padding: isMobile ? '8px 14px' : '8px 20px', cursor: 'pointer', textTransform: 'capitalize', fontFamily: 'inherit', transition: 'all 0.15s', marginBottom: -1.5, whiteSpace: 'nowrap' }}>
            {s}
            <span style={{ background: tab === s ? STATUS_BG[s] : '#f3f4f6', color: tab === s ? STATUS_COLOR[s] : '#9ca3af', borderRadius: 99, padding: '1px 7px', fontSize: 11, fontWeight: 700, marginLeft: 6 }}>{counts[s]}</span>
          </button>
        ))}
      </div>

      {/* Grid / empty / loading */}
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
            <SubmissionCard key={s.id} sub={s} onApprove={handleApprove} onReject={handleReject} onExtract={handleExtract} extracting={extracting} cardMsg={cardMsgs[s.id] || null} forceManualOpen={openManualIds.has(s.id)} />
          ))}
        </div>
      )}
    </div>
  )
}
