import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL  = 'shubhampaliwal5@gmail.com'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const STATUS_TABS  = ['pending', 'approved', 'rejected', 'extracted']
const STATUS_COLOR = { pending: '#f59e0b', approved: '#16a34a', rejected: '#dc2626', extracted: '#7c3aed' }
const STATUS_BG    = { pending: '#fef3c7', approved: '#f0fdf4', rejected: '#fef2f2', extracted: '#f5f3ff' }

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

function SubmissionCard({ sub, onApprove, onReject, onExtract, extracting }) {
  const imgs = sub.images || []
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
          <button
            onClick={() => onExtract(sub.id)}
            disabled={extracting === sub.id}
            style={{ width: '100%', background: extracting === sub.id ? '#e9d5ff' : '#7c3aed', color: '#fff', border: 'none', borderRadius: 10, padding: '11px 0', fontSize: 14, fontWeight: 700, cursor: extracting === sub.id ? 'not-allowed' : 'pointer', fontFamily: 'inherit', touchAction: 'manipulation', transition: 'background 0.2s' }}>
            {extracting === sub.id ? '⏳ Extracting…' : '🤖 Extract & Add to DB'}
          </button>
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
  const [fetching,   setFetching]   = useState(false)
  const [extracting, setExtracting] = useState(null)  // submission id being extracted
  const [extractMsg, setExtractMsg] = useState(null)  // { type: 'success'|'error', text }

  const isAdmin = user?.email === ADMIN_EMAIL

  useEffect(() => {
    if (!authLoading && !isAdmin) navigate('/')
  }, [user, authLoading, isAdmin, navigate])

  useEffect(() => {
    if (isAdmin) { fetchAll(); fetchSubs(tab) }
  }, [isAdmin, tab])

  const fetchSubs = async (status) => {
    setFetching(true)
    try {
      const { data, error } = await supabase
        .from('product_submissions').select('*')
        .eq('status', status).order('created_at', { ascending: false })
      if (error) console.error('[Admin] fetchSubs:', error.message, error.code)
      setSubs(data || [])
    } catch (e) {
      console.error('[Admin] fetchSubs exception:', e)
      setSubs([])
    } finally {
      setFetching(false)
    }
  }

  const fetchAll = async () => {
    try {
      const { data, error } = await supabase.from('product_submissions').select('status')
      if (error) { console.error('[Admin] fetchAll:', error.message, error.code); return }
      if (!data) return
      const c = { pending: 0, approved: 0, rejected: 0, extracted: 0 }
      data.forEach(r => { if (c[r.status] !== undefined) c[r.status]++ })
      setCounts(c)
    } catch (e) {
      console.error('[Admin] fetchAll exception:', e)
    }
  }

  const handleApprove = async (id) => {
    const { error } = await supabase.from('product_submissions').update({ status: 'approved' }).eq('id', id)
    if (error) console.error('[Admin] approve:', error.message)
    fetchAll(); fetchSubs(tab)
  }
  const handleReject = async (id) => {
    const { error } = await supabase.from('product_submissions').update({ status: 'rejected' }).eq('id', id)
    if (error) console.error('[Admin] reject:', error.message)
    fetchAll(); fetchSubs(tab)
  }

  const handleExtract = async (id) => {
    setExtracting(id)
    setExtractMsg(null)
    try {
      // Get current Supabase session JWT — proves identity server-side
      const { data: { session } } = await supabase.auth.getSession()
      if (!session?.access_token) throw new Error('Not authenticated — please log in again')

      const res = await fetch(`${API_BASE_URL}/api/admin/extract-product`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
        body: JSON.stringify({ submission_id: id }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Extraction failed')
      setExtractMsg({ type: 'success', text: `✓ "${data.product_name}" added to DB (score: ${data.awareness_score}, ${data.ingredients_count} ingredients)` })
      fetchAll(); fetchSubs(tab)
    } catch (err) {
      setExtractMsg({ type: 'error', text: `✕ ${err.message}` })
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

      {/* Extract result message */}
      {extractMsg && (
        <div style={{ marginBottom: 16, padding: '12px 16px', borderRadius: 10, fontSize: 13, fontWeight: 600,
          background: extractMsg.type === 'success' ? '#f0fdf4' : '#fef2f2',
          color: extractMsg.type === 'success' ? '#16a34a' : '#dc2626',
          border: `1px solid ${extractMsg.type === 'success' ? '#bbf7d0' : '#fecaca'}` }}>
          {extractMsg.text}
        </div>
      )}

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
            <SubmissionCard key={s.id} sub={s} onApprove={handleApprove} onReject={handleReject} onExtract={handleExtract} extracting={extracting} />
          ))}
        </div>
      )}
    </div>
  )
}
