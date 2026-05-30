import { useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const ORANGE = '#FF9933'
const BLUE   = '#1B3F8A'
const GREEN  = '#138808'

const QUIZ_QUESTIONS = [
  { id: 'age_group',       question: 'What is your age group?',                  options: ['Under 18', '18–25', '26–35', '36–45', '46+'] },
  { id: 'health_concern',  question: 'Which area matters most to you?',           options: ['Fitness', 'Nutrition', 'Skincare', 'Haircare', 'Overall wellness'] },
  { id: 'diet_type',       question: 'Do you follow a specific diet?',            options: ['Vegan', 'Vegetarian', 'Non-vegetarian', 'Keto / Low-carb', 'Jain', 'No specific diet'] },
  { id: 'check_frequency', question: 'How often do you check product ingredients?', options: ['Always – before every purchase', 'Sometimes', 'Rarely', 'This is my first time'] },
  { id: 'product_category',question: 'Which products do you check most?',        options: ['Packaged snacks / Food', 'Beverages', 'Cosmetics / Skincare', 'Baby products', 'Health supplements'] },
]

function GoogleIcon() {
  return (
    <svg width="20" height="20" viewBox="0 0 48 48" style={{ flexShrink: 0 }}>
      <path fill="#EA4335" d="M24 9.5c3.14 0 5.95 1.08 8.17 2.86l6.1-6.1C34.47 3.08 29.53 1 24 1 14.82 1 7.02 6.48 3.44 14.22l7.12 5.53C12.28 13.59 17.67 9.5 24 9.5z"/>
      <path fill="#4285F4" d="M46.56 24.5c0-1.64-.15-3.22-.41-4.75H24v9h12.73c-.55 2.97-2.2 5.48-4.68 7.16l7.19 5.59C43.27 37.52 46.56 31.5 46.56 24.5z"/>
      <path fill="#FBBC05" d="M10.56 28.25A14.6 14.6 0 019.5 24c0-1.48.26-2.91.71-4.25l-7.12-5.53A23.94 23.94 0 001 24c0 3.86.93 7.5 2.56 10.72l7-5.47z"/>
      <path fill="#34A853" d="M24 47c5.53 0 10.18-1.83 13.57-4.97l-7.19-5.59C28.6 38.13 26.42 39 24 39c-6.33 0-11.72-4.09-13.44-9.75l-7 5.47C7.02 42.52 14.82 47 24 47z"/>
    </svg>
  )
}

function EyeIcon({ show }) {
  return show ? (
    <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
    </svg>
  ) : (
    <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.477 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
    </svg>
  )
}

function Divider({ label = 'or' }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', margin: '14px 0' }}>
      <div style={{ flex: 1, height: 1, background: '#e5e7eb' }} />
      <span style={{ margin: '0 12px', fontSize: 11, color: '#9ca3af', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em' }}>{label}</span>
      <div style={{ flex: 1, height: 1, background: '#e5e7eb' }} />
    </div>
  )
}

function Input({ type = 'text', value, onChange, placeholder, suffix, onKeyDown }) {
  return (
    <div style={{ position: 'relative', marginBottom: 12 }}>
      <input
        type={type}
        value={value}
        onChange={onChange}
        onKeyDown={onKeyDown}
        placeholder={placeholder}
        style={{ width: '100%', border: '1.5px solid #d1d5db', borderRadius: 10, padding: suffix ? '11px 40px 11px 14px' : '11px 14px', fontSize: 14, outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit', color: '#111827' }}
        onFocus={e => { e.target.style.borderColor = ORANGE; e.target.style.boxShadow = `0 0 0 2px ${ORANGE}22` }}
        onBlur={e => { e.target.style.borderColor = '#d1d5db'; e.target.style.boxShadow = '' }}
      />
      {suffix && (
        <button type="button" onClick={suffix.onClick} tabIndex={-1}
          style={{ position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#9ca3af', padding: 0, display: 'flex' }}>
          {suffix.icon}
        </button>
      )}
    </div>
  )
}

function PrimaryBtn({ children, onClick, disabled, loading }) {
  return (
    <button onClick={onClick} disabled={disabled || loading}
      style={{ width: '100%', background: ORANGE, color: '#fff', border: 'none', borderRadius: 10, padding: '13px 14px', fontSize: 15, fontWeight: 700, cursor: (disabled || loading) ? 'not-allowed' : 'pointer', opacity: (disabled || loading) ? 0.65 : 1, fontFamily: 'inherit', marginTop: 4 }}>
      {children}
    </button>
  )
}

function GhostBtn({ children, onClick }) {
  return (
    <button onClick={onClick} style={{ background: 'none', border: 'none', color: ORANGE, fontSize: 13, fontWeight: 500, cursor: 'pointer', fontFamily: 'inherit', padding: 0 }}>
      {children}
    </button>
  )
}

export default function AuthModal({ onClose, initialStep }) {
  const [step,        setStep]        = useState(initialStep || 'main')
  const [isSignUp,    setIsSignUp]    = useState(false)

  const [email,       setEmail]       = useState('')
  const [password,    setPassword]    = useState('')
  const [showPass,    setShowPass]    = useState(false)
  const [resetEmail,  setResetEmail]  = useState('')

  const [loading,      setLoading]      = useState(false)
  const [error,        setError]        = useState('')
  const [quizAnswers,  setQuizAnswers]  = useState({})
  const [newPassword,  setNewPassword]  = useState('')
  const [confirmPass,  setConfirmPass]  = useState('')
  const [showNewPass,  setShowNewPass]  = useState(false)
  const [showConfPass, setShowConfPass] = useState(false)

  const clearError = () => setError('')

  // ── After successful login: show quiz until user completes it once ──
  const handlePostLogin = async (userId) => {
    if (!userId) { setStep('done'); setTimeout(onClose, 1600); return }
    const { data: prof } = await supabase
      .from('user_profiles')
      .select('id, quiz_completed')
      .eq('id', userId)
      .maybeSingle()
    if (!prof) {
      await supabase.from('user_profiles').upsert({ id: userId })
    }
    if (!prof?.quiz_completed) {
      setStep('quiz')
    } else {
      setStep('done')
      setTimeout(onClose, 1600)
    }
  }

  // ── Google OAuth ──
  const handleGoogle = async () => {
    setLoading(true); clearError()
    const { error: e } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: { redirectTo: 'https://www.parkho.in' },
    })
    if (e) { setError(e.message); setLoading(false) }
  }

  // ── Email sign-in ──
  const handleEmailSignIn = async () => {
    if (!email.trim()) { setError('Please enter your email.'); return }
    if (!password)     { setError('Please enter your password.'); return }
    setLoading(true); clearError()
    const { data, error: e } = await supabase.auth.signInWithPassword({ email: email.trim(), password })
    setLoading(false)
    if (e) {
      const msg = e.message?.toLowerCase() || ''
      if (msg.includes('not confirmed') || msg.includes('email not confirmed')) {
        setError('Please confirm your email first — check your inbox for the link we sent.')
        return
      }
      if (msg.includes('invalid login') || msg.includes('invalid credentials') || msg.includes('wrong password')) {
        setError('Incorrect email or password. Please try again.')
        return
      }
      setError(e.message)
      return
    }
    await handlePostLogin(data.user?.id)
  }

  // ── Email sign-up ──
  const handleEmailSignUp = async () => {
    if (!email.trim()) { setError('Please enter your email.'); return }
    if (password.length < 6) { setError('Password must be at least 6 characters.'); return }
    setLoading(true); clearError()
    const { data, error: e } = await supabase.auth.signUp({ email: email.trim(), password })

    if (e) {
      const msg = e.message?.toLowerCase() || ''
      if (msg.includes('already registered') || msg.includes('already exists') || msg.includes('already been registered')) {
        const { data: d2, error: e2 } = await supabase.auth.signInWithPassword({ email: email.trim(), password })
        setLoading(false)
        if (e2) { setError('This email is already registered. Switch to "Sign In".'); return }
        await handlePostLogin(d2.user?.id)
        return
      }
      if (msg.includes('email') || msg.includes('sending') || msg.includes('rate') || msg.includes('smtp')) {
        setLoading(false)
        setStep('check_email')
        return
      }
      setLoading(false)
      setError(e.message)
      return
    }

    setLoading(false)
    if (data.session) {
      await handlePostLogin(data.user?.id)
    } else {
      setStep('check_email')
    }
  }

  // ── Set new password (after clicking email reset link) ──
  const handleSetNewPassword = async () => {
    if (newPassword.length < 6) { setError('Password must be at least 6 characters.'); return }
    if (newPassword !== confirmPass) { setError('Passwords do not match.'); return }
    setLoading(true); clearError()
    const { error: e } = await supabase.auth.updateUser({ password: newPassword })
    setLoading(false)
    if (e) { setError(e.message); return }
    setStep('reset_done')
    setTimeout(onClose, 2200)
  }

  // ── Forgot password ──
  const handleForgotPassword = async () => {
    if (!resetEmail.trim()) { setError('Please enter your email address.'); return }
    setLoading(true); clearError()
    const { error: e } = await supabase.auth.resetPasswordForEmail(resetEmail.trim(), {
      redirectTo: 'https://www.parkho.in',
    })
    setLoading(false)
    if (e) { setError(e.message); return }
    setStep('forgot_sent')
  }

  // ── Quiz submit ──
  const handleQuizSubmit = async () => {
    setLoading(true)
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (user && Object.keys(quizAnswers).length > 0)
        await supabase.from('user_profiles').update({ ...quizAnswers, quiz_completed: true }).eq('id', user.id)
    } catch (_) {}
    setLoading(false)
    setStep('done')
    setTimeout(onClose, 1600)
  }

  // ─────────────────── RENDER ───────────────────
  return (
    <div className="auth-modal-overlay">
      <div style={{ position: 'absolute', inset: 0 }} onClick={onClose} />

      <div className="auth-modal-card">

        {/* Top accent bar */}
        <div style={{ height: 4, background: `linear-gradient(90deg, ${ORANGE}, ${BLUE})`, borderRadius: '20px 20px 0 0' }} />

        {/* Close */}
        <button onClick={onClose} style={{ position: 'absolute', top: 14, right: 16, background: 'none', border: 'none', fontSize: 22, color: '#9ca3af', cursor: 'pointer', lineHeight: 1, zIndex: 2 }}>✕</button>

        {/* Logo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '20px 24px 0' }}>
          <svg width="32" height="32" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="22" cy="22" r="17.5" fill="white" fillOpacity="0.08" stroke={ORANGE} strokeWidth="4"/>
            <rect x="9" y="14" width="11" height="14" rx="2" fill="#4A87B8"/>
            <ellipse cx="14.5" cy="20" rx="3" ry="4" fill="white" opacity="0.85"/>
            <line x1="14.5" y1="15.5" x2="14.5" y2="24.5" stroke="#4A87B8" strokeWidth="1.2"/>
            <rect x="10" y="12" width="9" height="3" rx="1" fill="#4A87B8"/>
            <rect x="21" y="12" width="8" height="16" rx="2.5" fill="#4A87B8"/>
            <rect x="22.5" y="9" width="5" height="4" rx="1.5" fill="#4A87B8"/>
            <rect x="24" y="6.5" width="2" height="3.5" rx="1" fill="#4A87B8"/>
            <rect x="30" y="21" width="7.5" height="7" rx="2" fill="#4A87B8"/>
            <rect x="30.5" y="19" width="6.5" height="2.5" rx="1" fill="#4A87B8"/>
            <line x1="36" y1="36" x2="48" y2="48" stroke={ORANGE} strokeWidth="5.5" strokeLinecap="round"/>
          </svg>
          <div style={{ display: 'flex', flexDirection: 'column', lineHeight: 1.2 }}>
            <span style={{ fontWeight: 800, fontSize: 20, color: BLUE, fontFamily: 'Poppins, sans-serif' }}>Parkho</span>
            <span style={{ fontSize: 11, color: '#9ca3af' }}>Know what's inside</span>
          </div>
        </div>

        <div style={{ padding: '14px 24px 28px' }}>

          {/* ══════════════ MAIN SCREEN ══════════════ */}
          {step === 'main' && (
            <>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 2px' }}>Welcome!</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 18px' }}>Login or sign up to rate products & more.</p>

              {/* Google Button */}
              <button
                onClick={handleGoogle}
                disabled={loading}
                style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10, background: '#fff', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '12px 16px', fontSize: 15, fontWeight: 600, color: '#374151', cursor: 'pointer', boxShadow: '0 1px 4px rgba(0,0,0,0.07)', fontFamily: 'inherit', transition: 'box-shadow 0.15s' }}
                onMouseEnter={e => e.currentTarget.style.boxShadow = '0 3px 12px rgba(0,0,0,0.12)'}
                onMouseLeave={e => e.currentTarget.style.boxShadow = '0 1px 4px rgba(0,0,0,0.07)'}
              >
                <GoogleIcon />
                Continue with Google
              </button>

              <Divider />

              {/* Sign In / Sign Up toggle */}
              <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
                {[false, true].map(su => (
                  <button key={String(su)} onClick={() => { setIsSignUp(su); clearError() }}
                    style={{ flex: 1, padding: '7px 0', borderRadius: 8, border: `1.5px solid ${isSignUp === su ? ORANGE : '#e5e7eb'}`, fontFamily: 'inherit', fontSize: 13, fontWeight: 600, cursor: 'pointer',
                      background: isSignUp === su ? '#fff7ed' : '#fff',
                      color: isSignUp === su ? ORANGE : '#6b7280',
                    }}>
                    {su ? 'New Account' : 'Sign In'}
                  </button>
                ))}
              </div>

              <Input type="email" value={email} onChange={e => { setEmail(e.target.value); clearError() }} placeholder="you@example.com"
                onKeyDown={e => e.key === 'Enter' && (isSignUp ? handleEmailSignUp() : handleEmailSignIn())} />
              <Input
                type={showPass ? 'text' : 'password'}
                value={password}
                onChange={e => { setPassword(e.target.value); clearError() }}
                placeholder={isSignUp ? 'Create a password (min 6 chars)' : 'Your password'}
                suffix={{ icon: <EyeIcon show={showPass} />, onClick: () => setShowPass(p => !p) }}
                onKeyDown={e => e.key === 'Enter' && (isSignUp ? handleEmailSignUp() : handleEmailSignIn())}
              />

              {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '-6px 0 8px' }}>{error}</p>}

              <PrimaryBtn onClick={isSignUp ? handleEmailSignUp : handleEmailSignIn} loading={loading}>
                {loading ? (isSignUp ? 'Creating account…' : 'Signing in…') : (isSignUp ? 'Create Account →' : 'Sign In →')}
              </PrimaryBtn>

              {!isSignUp && (
                <div style={{ textAlign: 'center', marginTop: 10 }}>
                  <GhostBtn onClick={() => { setResetEmail(email); setStep('forgot'); clearError() }}>
                    Forgot password?
                  </GhostBtn>
                </div>
              )}

              <p style={{ textAlign: 'center', fontSize: 11, color: '#9ca3af', marginTop: 14, marginBottom: 0 }}>
                You can browse Parkho without logging in.
              </p>
            </>
          )}

          {/* ══════════════ CHECK EMAIL (signup confirmation) ══════════════ */}
          {step === 'check_email' && (
            <div style={{ textAlign: 'center', paddingTop: 8 }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#fff7ed', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <svg width="30" height="30" fill="none" stroke={ORANGE} strokeWidth="2" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 6px' }}>Confirm your email</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 4px' }}>We sent a confirmation link to</p>
              <p style={{ fontWeight: 700, color: '#111827', marginBottom: 16 }}>{email}</p>
              <p style={{ fontSize: 13, color: '#9ca3af', marginBottom: 20 }}>Click the link to activate your account, then come back and sign in.</p>
              <GhostBtn onClick={() => { setStep('main'); clearError() }}>← Back to login</GhostBtn>
            </div>
          )}

          {/* ══════════════ FORGOT PASSWORD ══════════════ */}
          {step === 'forgot' && (
            <>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 4px' }}>Reset Password</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 18px' }}>Enter your email and we'll send a reset link.</p>
              <Input type="email" value={resetEmail} onChange={e => { setResetEmail(e.target.value); clearError() }} placeholder="you@example.com"
                onKeyDown={e => e.key === 'Enter' && handleForgotPassword()} />
              {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '-6px 0 8px' }}>{error}</p>}
              <PrimaryBtn onClick={handleForgotPassword} loading={loading}>{loading ? 'Sending…' : 'Send Reset Link'}</PrimaryBtn>
              <div style={{ textAlign: 'center', marginTop: 12 }}>
                <GhostBtn onClick={() => { setStep('main'); clearError() }}>← Back to login</GhostBtn>
              </div>
            </>
          )}

          {/* ══════════════ FORGOT SENT ══════════════ */}
          {step === 'forgot_sent' && (
            <div style={{ textAlign: 'center', paddingTop: 8 }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#eff6ff', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <svg width="30" height="30" fill="none" stroke={BLUE} strokeWidth="2" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 6px' }}>Check your inbox</h2>
              <p style={{ fontSize: 13, color: '#6b7280', marginBottom: 4 }}>Reset link sent to</p>
              <p style={{ fontWeight: 700, color: '#111827', marginBottom: 16 }}>{resetEmail}</p>
              <p style={{ fontSize: 12, color: '#9ca3af', marginBottom: 20 }}>Click the link in the email to set a new password.</p>
              <GhostBtn onClick={() => { setStep('main'); clearError() }}>← Back to login</GhostBtn>
            </div>
          )}

          {/* ══════════════ QUIZ ══════════════ */}
          {step === 'quiz' && (
            <>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 4px' }}>Quick questions</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 18px' }}>Help us personalise your experience. <span style={{ color: ORANGE, fontWeight: 600 }}>All optional.</span></p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
                {QUIZ_QUESTIONS.map(q => {
                  const isSingle = q.id === 'age_group'
                  const getSelected = () => {
                    const v = quizAnswers[q.id]
                    if (!v) return []
                    return Array.isArray(v) ? v : [v]
                  }
                  const toggleOpt = (opt) => {
                    if (isSingle) {
                      setQuizAnswers(p => ({ ...p, [q.id]: opt }))
                    } else {
                      setQuizAnswers(p => {
                        const cur = Array.isArray(p[q.id]) ? p[q.id] : (p[q.id] ? [p[q.id]] : [])
                        const next = cur.includes(opt) ? cur.filter(o => o !== opt) : [...cur, opt]
                        return { ...p, [q.id]: next }
                      })
                    }
                  }
                  const selected = getSelected()
                  return (
                    <div key={q.id}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                        <p style={{ fontSize: 14, fontWeight: 600, color: '#374151', margin: 0 }}>{q.question}</p>
                        <span style={{ fontSize: 10, fontWeight: 700, color: isSingle ? '#6b7280' : ORANGE, background: isSingle ? '#f3f4f6' : '#fff7ed', borderRadius: 99, padding: '2px 8px', whiteSpace: 'nowrap' }}>
                          {isSingle ? 'Choose one' : 'Choose multiple'}
                        </span>
                      </div>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {q.options.map(opt => {
                          const sel = selected.includes(opt)
                          return (
                            <button key={opt} onClick={() => toggleOpt(opt)}
                              style={{ padding: '6px 12px', borderRadius: 999, fontSize: 13, fontWeight: 500, cursor: 'pointer', fontFamily: 'inherit', border: `1.5px solid ${sel ? ORANGE : '#d1d5db'}`, background: sel ? ORANGE : '#fff', color: sel ? '#fff' : '#374151', transition: 'all 0.15s' }}>
                              {!isSingle && sel && '✓ '}{opt}
                            </button>
                          )
                        })}
                      </div>
                    </div>
                  )
                })}
              </div>
              <div style={{ display: 'flex', gap: 12, marginTop: 24 }}>
                <button onClick={() => { setStep('done'); setTimeout(onClose, 1600) }}
                  style={{ flex: 1, border: '1.5px solid #d1d5db', background: '#fff', color: '#374151', borderRadius: 10, padding: 12, fontSize: 14, cursor: 'pointer', fontFamily: 'inherit' }}>
                  Skip
                </button>
                <button onClick={handleQuizSubmit} disabled={loading}
                  style={{ flex: 1, background: GREEN, color: '#fff', border: 'none', borderRadius: 10, padding: 12, fontSize: 14, fontWeight: 700, cursor: 'pointer', opacity: loading ? 0.65 : 1, fontFamily: 'inherit' }}>
                  {loading ? 'Saving…' : 'Submit'}
                </button>
              </div>
            </>
          )}

          {/* ══════════════ SET NEW PASSWORD ══════════════ */}
          {step === 'reset_password' && (
            <>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 4px' }}>Set New Password</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 18px' }}>Choose a strong password for your account.</p>
              <Input
                type={showNewPass ? 'text' : 'password'}
                value={newPassword}
                onChange={e => { setNewPassword(e.target.value); clearError() }}
                placeholder="New password (min 6 characters)"
                suffix={{ icon: <EyeIcon show={showNewPass} />, onClick: () => setShowNewPass(p => !p) }}
              />
              <Input
                type={showConfPass ? 'text' : 'password'}
                value={confirmPass}
                onChange={e => { setConfirmPass(e.target.value); clearError() }}
                placeholder="Confirm new password"
                suffix={{ icon: <EyeIcon show={showConfPass} />, onClick: () => setShowConfPass(p => !p) }}
              />
              {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '-6px 0 8px' }}>{error}</p>}
              <PrimaryBtn onClick={handleSetNewPassword} loading={loading}>
                {loading ? 'Saving…' : 'Set New Password →'}
              </PrimaryBtn>
            </>
          )}

          {/* ══════════════ RESET DONE ══════════════ */}
          {step === 'reset_done' && (
            <div style={{ textAlign: 'center', padding: '12px 0 16px' }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#dcfce7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <svg width="30" height="30" fill="none" stroke="#16a34a" strokeWidth="2.5" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 6px' }}>Password Updated!</h2>
              <p style={{ fontSize: 14, color: '#6b7280' }}>Your new password has been saved. You're now logged in.</p>
            </div>
          )}

          {/* ══════════════ DONE ══════════════ */}
          {step === 'done' && (
            <div style={{ textAlign: 'center', padding: '12px 0 16px' }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#dcfce7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <svg width="30" height="30" fill="none" stroke="#16a34a" strokeWidth="2.5" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 6px' }}>You're in!</h2>
              <p style={{ fontSize: 14, color: '#6b7280' }}>Welcome to Parkho. Know what's inside.</p>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}
