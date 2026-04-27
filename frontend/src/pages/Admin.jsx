import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { supabase } from '../lib/supabaseClient'

const ADMIN_EMAIL = 'shubhampaliwal5@gmail.com'

const STATUS_TABS = ['pending', 'approved', 'rejected']
const STATUS_COLOR = { pending: '#f59e0b', approved: '#16a34a', rejected: '#dc2626' }
const STATUS_BG    = { pending: '#fef3c7', approved: '#f0fdf4', rejected: '#fef2f2' }

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return d.toLocaleString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function SubmissionCard({ sub, onApprove, onReject }) {
  const [imgIdx, setImgIdx] = useState(0)
  const imgs = sub.images || []

  return (
    <div style={{ background: '#fff', border: '1px solid #e5e7eb', borderRadius: 14, overflow: 'hidden', boxShadow: '0 2px 12px rgba(0,0,0,0.05)' }}>

      {/* Image viewer */}
      <div style={{ position: 'relative', height: 180, background: '#f3f4f6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        {imgs.length > 0 ? (
          <>
            <img src={imgs[imgIdx]} alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
            {imgs.length > 1 && (
              <div style={{ position: 'absolute', bottom: 8, left: 0, right: 0, display: 'flex', justifyContent: 'center', gap: 6 }}>
                {imgs.map((_, i) => (
                  <button key={i} onClick={() => setImgIdx(i)}
                    style={{ width: i === imgIdx ? 20 : 8, height: 8, borderRadius: 99, border: 'none', cursor: 'pointer', background: i === imgIdx ? '#FF9933' : '#d1d5db', padding: 0, transition: 'all 0.2s' }} />
                ))}
              </div>
            )}
            <a href={imgs[imgIdx]} target="_blank" rel="noreferrer"
              style={{ position: 'absolute', top: 8, right: 8, background: 'rgba(0,0,0,0.5)', color: '#fff', borderRadius: 6, padding: '4px 8px', fontSize: 11, textDecoration: 'none', fontWeight: 600 }}>
              Full ↗
            </a>
          </>
        ) : (
          <span style={{ color: '#9ca3af', fontSize: 13 }}>No images</span>
        )}
      </div>

      {/* Info */}
      <div style={{ padding: '14px 16px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
          <div>
            <p style={{ margin: 0, fontWeight: 700, fontSize: 14, color: '#111827' }}>
              {sub.product_name || sub.product_name_searched}
            </p>
            {sub.product_name && sub.product_name !== sub.product_name_searched && (
              <p style={{ margin: '1px 0 0', fontSize: 11, color: '#b45309' }}>Searched: "{sub.product_name_searched}"</p>
            )}
            <p style={{ margin: '2px 0 0', fontSize: 12, color: '#9ca3af' }}>{formatDate(sub.created_at)}</p>
          </div>
          <span style={{ background: STATUS_BG[sub.status], color: STATUS_COLOR[sub.status], fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 99, textTransform: 'uppercase', letterSpacing: '0.05em', whiteSpace: 'nowrap' }}>
            {sub.status}
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 14 }}>📧</span>
            <span style={{ fontSize: 13, color: '#374151', wordBreak: 'break-all' }}>{sub.email || '—'}</span>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 14 }}>💳</span>
            <span style={{ fontSize: 14, fontWeight: 700, color: '#1d4ed8', wordBreak: 'break-all' }}>{sub.contact}</span>
          </div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <span style={{ fontSize: 14 }}>🖼️</span>
            <span style={{ fontSize: 13, color: '#6b7280' }}>{imgs.length} image{imgs.length !== 1 ? 's' : ''}</span>
          </div>
        </div>

        {sub.status === 'pending' && (
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => onApprove(sub.id)}
              style={{ flex: 1, background: '#16a34a', color: '#fff', border: 'none', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
              ✓ Approve
            </button>
            <button onClick={() => onReject(sub.id)}
              style={{ flex: 1, background: '#fff', color: '#dc2626', border: '1.5px solid #dc2626', borderRadius: 8, padding: '9px 0', fontSize: 13, fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit' }}>
              ✕ Reject
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default function Admin() {
  const { user, loading: authLoading } = useAuth()
  const navigate = useNavigate()
  const [tab,       setTab]       = useState('pending')
  const [subs,      setSubs]      = useState([])
  const [counts,    setCounts]    = useState({ pending: 0, approved: 0, rejected: 0 })
  const [fetching,  setFetching]  = useState(true)

  const isAdmin = user?.email === ADMIN_EMAIL

  useEffect(() => {
    if (!authLoading && !isAdmin) navigate('/')
  }, [user, authLoading, isAdmin, navigate])

  useEffect(() => {
    if (isAdmin) {
      fetchAll()
      fetchSubs(tab)
    }
  }, [isAdmin, tab])

  const fetchSubs = async (status) => {
    setFetching(true)
    const { data } = await supabase
      .from('product_submissions')
      .select('*')
      .eq('status', status)
      .order('created_at', { ascending: false })
    setSubs(data || [])
    setFetching(false)
  }

  const fetchAll = async () => {
    const { data } = await supabase
      .from('product_submissions')
      .select('status')
    if (!data) return
    const c = { pending: 0, approved: 0, rejected: 0 }
    data.forEach(r => { if (c[r.status] !== undefined) c[r.status]++ })
    setCounts(c)
  }

  const handleApprove = async (id) => {
    await supabase.from('product_submissions').update({ status: 'approved' }).eq('id', id)
    fetchAll()
    fetchSubs(tab)
  }

  const handleReject = async (id) => {
    await supabase.from('product_submissions').update({ status: 'rejected' }).eq('id', id)
    fetchAll()
    fetchSubs(tab)
  }

  if (authLoading) {
    return (
      <div style={{ minHeight: '60vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ color: '#9ca3af', fontSize: 15 }}>Checking access…</div>
      </div>
    )
  }

  if (!isAdmin) return null

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto', padding: '32px 16px 60px' }}>

      {/* Header */}
      <div style={{ marginBottom: 28 }}>
        <h1 style={{ fontFamily: 'Poppins, sans-serif', fontSize: 26, fontWeight: 800, color: '#0D1B2A', margin: '0 0 4px' }}>
          🔐 Admin Panel
        </h1>
        <p style={{ color: '#6b7280', fontSize: 14, margin: 0 }}>
          Review product submissions · Logged in as <strong>{user.email}</strong>
        </p>
      </div>

      {/* Stats */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 24, flexWrap: 'wrap' }}>
        {STATUS_TABS.map(s => (
          <div key={s} style={{ background: STATUS_BG[s], border: `1px solid ${STATUS_COLOR[s]}33`, borderRadius: 12, padding: '12px 20px', minWidth: 100 }}>
            <div style={{ fontSize: 22, fontWeight: 800, color: STATUS_COLOR[s] }}>{counts[s]}</div>
            <div style={{ fontSize: 12, color: '#6b7280', textTransform: 'capitalize', fontWeight: 600 }}>{s}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, borderBottom: '1px solid #e5e7eb', paddingBottom: 1 }}>
        {STATUS_TABS.map(s => (
          <button key={s} onClick={() => setTab(s)}
            style={{ background: 'none', border: 'none', borderBottom: tab === s ? `2px solid ${STATUS_COLOR[s]}` : '2px solid transparent', color: tab === s ? STATUS_COLOR[s] : '#6b7280', fontWeight: tab === s ? 700 : 500, fontSize: 14, padding: '8px 16px', cursor: 'pointer', textTransform: 'capitalize', fontFamily: 'inherit', transition: 'all 0.15s', marginBottom: -1 }}>
            {s} <span style={{ background: tab === s ? STATUS_BG[s] : '#f3f4f6', color: tab === s ? STATUS_COLOR[s] : '#9ca3af', borderRadius: 99, padding: '1px 8px', fontSize: 12, fontWeight: 700, marginLeft: 4 }}>{counts[s]}</span>
          </button>
        ))}
      </div>

      {/* Grid */}
      {fetching ? (
        <div style={{ textAlign: 'center', padding: '48px 0', color: '#9ca3af' }}>Loading…</div>
      ) : subs.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '48px 0' }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>📭</div>
          <p style={{ color: '#9ca3af', fontSize: 15 }}>No {tab} submissions</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 }}>
          {subs.map(s => (
            <SubmissionCard key={s.id} sub={s} onApprove={handleApprove} onReject={handleReject} />
          ))}
        </div>
      )}
    </div>
  )
}
