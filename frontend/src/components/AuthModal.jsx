import { useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const QUIZ_QUESTIONS = [
  { id: 'age_group', question: 'What is your age group?', options: ['Under 18', '18–25', '26–35', '36–45', '46+'] },
  { id: 'health_concern', question: 'Which area matters most to you?', options: ['Fitness', 'Nutrition', 'Skincare', 'Haircare', 'Overall wellness'] },
  { id: 'diet_type', question: 'Do you follow a specific diet?', options: ['Vegan', 'Vegetarian', 'Non-vegetarian', 'Keto / Low-carb', 'Jain', 'No specific diet'] },
  { id: 'check_frequency', question: 'How often do you check product ingredients?', options: ['Always – before every purchase', 'Sometimes', 'Rarely', 'This is my first time'] },
  { id: 'product_category', question: 'Which products do you check most?', options: ['Packaged snacks / Food', 'Beverages', 'Cosmetics / Skincare', 'Baby products', 'Health supplements'] },
]

const S = {
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 9999, backgroundColor: 'rgba(0,0,0,0.55)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '16px' },
  card: { backgroundColor: '#fff', borderRadius: '18px', boxShadow: '0 20px 60px rgba(0,0,0,0.3)', width: '100%', maxWidth: '420px', maxHeight: '85vh', overflowY: 'auto', position: 'relative' },
  closeBtn: { position: 'absolute', top: '14px', right: '16px', background: 'none', border: 'none', fontSize: '22px', color: '#9ca3af', cursor: 'pointer', lineHeight: 1, zIndex: 2 },
  logo: { display: 'flex', alignItems: 'center', gap: '8px', padding: '22px 22px 0' },
  body: { padding: '12px 24px 28px' },
  h2: { fontSize: '20px', fontWeight: 700, color: '#111827', margin: '0 0 4px' },
  sub: { fontSize: '13px', color: '#6b7280', margin: '0 0 20px' },
  label: { display: 'block', fontSize: '12px', fontWeight: 600, color: '#374151', marginBottom: '6px' },
  input: { width: '100%', border: '1.5px solid #d1d5db', borderRadius: '10px', padding: '12px 14px', fontSize: '14px', outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit' },
  orRow: { display: 'flex', alignItems: 'center', margin: '14px 0' },
  orLine: { flex: 1, height: '1px', backgroundColor: '#e5e7eb' },
  orText: { margin: '0 12px', fontSize: '11px', color: '#9ca3af', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' },
  phoneWrap: { display: 'flex' },
  phonePrefix: { display: 'inline-flex', alignItems: 'center', padding: '0 12px', border: '1.5px solid #d1d5db', borderRight: 'none', borderRadius: '10px 0 0 10px', backgroundColor: '#f9fafb', fontSize: '14px', color: '#6b7280', whiteSpace: 'nowrap' },
  phoneInput: { flex: 1, border: '1.5px solid #d1d5db', borderLeft: 'none', borderRadius: '0 10px 10px 0', padding: '12px 14px', fontSize: '14px', outline: 'none', fontFamily: 'inherit' },
  primaryBtn: { width: '100%', backgroundColor: '#FF9933', color: '#fff', border: 'none', borderRadius: '10px', padding: '14px', fontSize: '15px', fontWeight: 700, cursor: 'pointer', marginTop: '18px', fontFamily: 'inherit' },
  ghostBtn: { background: 'none', border: 'none', color: '#FF9933', fontSize: '13px', fontWeight: 500, cursor: 'pointer', fontFamily: 'inherit' },
  error: { color: '#ef4444', fontSize: '12px', marginTop: '8px' },
  hint: { textAlign: 'center', fontSize: '12px', color: '#9ca3af', marginTop: '12px' },
}

export default function AuthModal({ onClose, initialStep }) {
  const [step, setStep] = useState(initialStep || 'contact')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [otp, setOtp] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [quizAnswers, setQuizAnswers] = useState({})

  const close = () => onClose()

  const handleContinue = async () => {
    const emailVal = email.trim()
    const phoneVal = phone.trim()
    if (!emailVal && !phoneVal) { setError('Please enter your email or mobile number.'); return }
    setLoading(true); setError('')
    try {
      if (emailVal) {
        const { error: e } = await supabase.auth.signInWithOtp({ email: emailVal, options: { emailRedirectTo: window.location.origin } })
        if (e) throw e
        setStep('check_email')
      } else {
        const ph = phoneVal.startsWith('+') ? phoneVal : `+91${phoneVal}`
        const { error: e } = await supabase.auth.signInWithOtp({ phone: ph })
        if (e) throw e
        setStep('otp')
      }
    } catch (e) {
      setError(e.message || 'Something went wrong. Please try again.')
    }
    setLoading(false)
  }

  const handleVerifyOtp = async () => {
    if (!otp.trim()) { setError('Please enter the OTP.'); return }
    setLoading(true); setError('')
    try {
      const ph = phone.trim().startsWith('+') ? phone.trim() : `+91${phone.trim()}`
      const { data, error: e } = await supabase.auth.verifyOtp({ phone: ph, token: otp.trim(), type: 'sms' })
      if (e) throw e
      const uid = data.user?.id
      if (uid) {
        const { data: prof } = await supabase.from('user_profiles').select('id').eq('id', uid).maybeSingle()
        if (!prof) { await supabase.from('user_profiles').insert({ id: uid }); setStep('quiz'); setLoading(false); return }
      }
      setStep('done'); setTimeout(close, 1800)
    } catch (e) {
      setError(e.message || 'Invalid OTP. Please try again.')
    }
    setLoading(false)
  }

  const handleQuizSubmit = async () => {
    setLoading(true)
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (user && Object.keys(quizAnswers).length > 0)
        await supabase.from('user_profiles').update({ ...quizAnswers, quiz_completed: true }).eq('id', user.id)
    } catch (_) {}
    setLoading(false); setStep('done'); setTimeout(close, 1800)
  }

  return (
    <div style={S.overlay}>
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }} onClick={close} />
      <div style={S.card}>
        <button style={S.closeBtn} onClick={close}>✕</button>

        {/* Logo */}
        <div style={S.logo}>
          <svg width="26" height="26" fill="#FF9933" viewBox="0 0 24 24">
            <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-10v5l4.25 2.52.77-1.28-3.52-2.09V10H11z"/>
          </svg>
          <span style={{ fontWeight: 800, fontSize: '17px' }}>
            <span style={{ color: '#FF9933' }}>Check</span>
            <span style={{ color: '#138808' }}>Karo</span>
          </span>
        </div>

        {/* CONTACT */}
        {step === 'contact' && (
          <div style={S.body}>
            <h2 style={S.h2}>Welcome!</h2>
            <p style={S.sub}>Login or sign up — no account needed to browse.</p>

            <label style={S.label}>Email Address</label>
            <input style={S.input} type="email" placeholder="you@example.com" value={email} onChange={e => { setEmail(e.target.value); setError('') }} />

            <div style={S.orRow}><div style={S.orLine}/><span style={S.orText}>or</span><div style={S.orLine}/></div>

            <label style={S.label}>Mobile Number</label>
            <div style={S.phoneWrap}>
              <span style={S.phonePrefix}>+91</span>
              <input style={S.phoneInput} type="tel" placeholder="9876543210" value={phone} maxLength={10} onChange={e => { setPhone(e.target.value.replace(/\D/g, '')); setError('') }} />
            </div>

            {error && <p style={S.error}>{error}</p>}

            <button style={{ ...S.primaryBtn, opacity: loading ? 0.65 : 1 }} onClick={handleContinue} disabled={loading}>
              {loading ? 'Please wait…' : 'Continue →'}
            </button>

            <p style={S.hint}>You can still use CheckKaro without logging in.</p>
          </div>
        )}

        {/* CHECK EMAIL */}
        {step === 'check_email' && (
          <div style={{ ...S.body, textAlign: 'center' }}>
            <div style={{ width: 64, height: 64, borderRadius: '50%', backgroundColor: '#fff7ed', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '8px auto 16px' }}>
              <svg width="30" height="30" fill="none" stroke="#FF9933" strokeWidth="2" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </div>
            <h2 style={S.h2}>Check your inbox!</h2>
            <p style={{ ...S.sub, marginBottom: 4 }}>We sent a login link to</p>
            <p style={{ fontWeight: 700, color: '#111827', marginBottom: 16 }}>{email}</p>
            <p style={{ fontSize: 13, color: '#9ca3af', marginBottom: 20 }}>Click the link in the email to log in. You can close this popup.</p>
            <button style={S.ghostBtn} onClick={() => { setStep('contact'); setEmail('') }}>← Use a different email</button>
          </div>
        )}

        {/* OTP */}
        {step === 'otp' && (
          <div style={S.body}>
            <h2 style={S.h2}>Enter OTP</h2>
            <p style={S.sub}>Sent via SMS to <strong>+91 {phone}</strong></p>
            <input style={{ ...S.input, textAlign: 'center', letterSpacing: '0.3em', fontSize: 22 }} type="text" inputMode="numeric" maxLength={6} placeholder="——————" value={otp} onChange={e => { setOtp(e.target.value.replace(/\D/g, '')); setError('') }} onKeyDown={e => e.key === 'Enter' && handleVerifyOtp()} />
            {error && <p style={S.error}>{error}</p>}
            <button style={{ ...S.primaryBtn, opacity: loading ? 0.65 : 1 }} onClick={handleVerifyOtp} disabled={loading}>{loading ? 'Verifying…' : 'Verify OTP'}</button>
            <div style={{ textAlign: 'center', marginTop: 12 }}>
              <button style={{ ...S.ghostBtn, color: '#9ca3af' }} onClick={() => { setStep('contact'); setOtp(''); setError('') }}>← Change number</button>
            </div>
          </div>
        )}

        {/* QUIZ */}
        {step === 'quiz' && (
          <div style={S.body}>
            <h2 style={S.h2}>Quick questions</h2>
            <p style={S.sub}>Help us personalise your experience. <span style={{ color: '#FF9933', fontWeight: 600 }}>All optional.</span></p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
              {QUIZ_QUESTIONS.map(q => (
                <div key={q.id}>
                  <p style={{ fontSize: 14, fontWeight: 600, color: '#374151', marginBottom: 8 }}>{q.question}</p>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {q.options.map(opt => {
                      const sel = quizAnswers[q.id] === opt
                      return (
                        <button key={opt} onClick={() => setQuizAnswers(p => ({ ...p, [q.id]: opt }))} style={{ padding: '6px 12px', borderRadius: 999, fontSize: 13, fontWeight: 500, cursor: 'pointer', border: `1.5px solid ${sel ? '#FF9933' : '#d1d5db'}`, backgroundColor: sel ? '#FF9933' : '#fff', color: sel ? '#fff' : '#374151', fontFamily: 'inherit' }}>{opt}</button>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
              <button onClick={() => { setStep('done'); setTimeout(close, 1800) }} style={{ flex: 1, border: '1.5px solid #d1d5db', backgroundColor: '#fff', color: '#374151', borderRadius: 10, padding: 12, fontSize: 14, cursor: 'pointer', fontFamily: 'inherit' }}>Skip</button>
              <button onClick={handleQuizSubmit} disabled={loading} style={{ flex: 1, backgroundColor: '#138808', color: '#fff', border: 'none', borderRadius: 10, padding: 12, fontSize: 14, fontWeight: 700, cursor: 'pointer', opacity: loading ? 0.65 : 1, fontFamily: 'inherit' }}>{loading ? 'Saving…' : 'Submit'}</button>
            </div>
          </div>
        )}

        {/* DONE */}
        {step === 'done' && (
          <div style={{ ...S.body, textAlign: 'center', padding: '20px 24px 40px' }}>
            <div style={{ width: 64, height: 64, borderRadius: '50%', backgroundColor: '#dcfce7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '8px auto 16px' }}>
              <svg width="30" height="30" fill="none" stroke="#16a34a" strokeWidth="2.5" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
            </div>
            <h2 style={S.h2}>You're in!</h2>
            <p style={{ fontSize: 14, color: '#6b7280' }}>Welcome to CheckKaro. Know what's inside.</p>
          </div>
        )}
      </div>
    </div>
  )
}
