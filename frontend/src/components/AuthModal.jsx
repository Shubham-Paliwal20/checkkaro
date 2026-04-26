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

function Input({ type = 'text', value, onChange, placeholder, suffix }) {
  return (
    <div style={{ position: 'relative', marginBottom: 12 }}>
      <input
        type={type}
        value={value}
        onChange={onChange}
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
  const [step,         setStep]         = useState(initialStep || 'main')
  const [authTab,      setAuthTab]      = useState('email')   // 'email' | 'phone'
  const [isSignUp,     setIsSignUp]     = useState(false)

  // Email + password
  const [email,        setEmail]        = useState('')
  const [password,     setPassword]     = useState('')
  const [showPass,     setShowPass]     = useState(false)

  // Phone OTP
  const [phone,        setPhone]        = useState('')
  const [otp,          setOtp]          = useState('')

  // Forgot password
  const [resetEmail,   setResetEmail]   = useState('')

  const [loading,      setLoading]      = useState(false)
  const [error,        setError]        = useState('')
  const [quizAnswers,  setQuizAnswers]  = useState({})

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
      options: { redirectTo: window.location.origin },
    })
    if (e) { setError(e.message); setLoading(false) }
    // On success the page redirects — no further action needed here
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
      // Already registered — try signing in with the same password
      if (msg.includes('already registered') || msg.includes('already exists') || msg.includes('already been registered')) {
        const { data: d2, error: e2 } = await supabase.auth.signInWithPassword({ email: email.trim(), password })
        setLoading(false)
        if (e2) { setError('This email is already registered. Switch to "Sign In" tab.'); return }
        await handlePostLogin(d2.user?.id)
        return
      }
      // Email sending failed (rate limit / SMTP) — account may have been created; show check-email screen
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
    // Email confirmation disabled in Supabase → session returned immediately
    if (data.session) {
      await handlePostLogin(data.user?.id)
    } else {
      setStep('check_email')
    }
  }

  // ── Phone OTP send ──
  const handleSendOtp = async () => {
    if (!phone.trim()) { setError('Please enter your mobile number.'); return }
    setLoading(true); clearError()
    const ph = phone.startsWith('+') ? phone : `+91${phone}`
    const { error: e } = await supabase.auth.signInWithOtp({ phone: ph })
    setLoading(false)
    if (e) { setError(e.message); return }
    setStep('otp')
  }

  // ── OTP verify ──
  const handleVerifyOtp = async () => {
    if (!otp.trim()) { setError('Please enter the OTP.'); return }
    setLoading(true); clearError()
    const ph = phone.startsWith('+') ? phone : `+91${phone}`
    const { data, error: e } = await supabase.auth.verifyOtp({ phone: ph, token: otp.trim(), type: 'sms' })
    setLoading(false)
    if (e) { setError(e.message); return }
    await handlePostLogin(data.user?.id)
  }

  // ── Forgot password ──
  const handleForgotPassword = async () => {
    if (!resetEmail.trim()) { setError('Please enter your email address.'); return }
    setLoading(true); clearError()
    const { error: e } = await supabase.auth.resetPasswordForEmail(resetEmail.trim(), {
      redirectTo: window.location.origin,
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
          <svg width="26" height="26" fill={ORANGE} viewBox="0 0 24 24">
            <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-10v5l4.25 2.52.77-1.28-3.52-2.09V10H11z"/>
          </svg>
          <span style={{ fontWeight: 800, fontSize: 17 }}>
            <span style={{ color: ORANGE }}>Check</span><span style={{ color: GREEN }}>Karo</span>
          </span>
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

              {/* Tab toggle — Email | Phone */}
              <div style={{ display: 'flex', background: '#f3f4f6', borderRadius: 10, padding: 3, marginBottom: 16 }}>
                {['email', 'phone'].map(t => (
                  <button key={t} onClick={() => { setAuthTab(t); clearError() }}
                    style={{ flex: 1, padding: '8px 0', borderRadius: 8, border: 'none', fontFamily: 'inherit', fontSize: 13, fontWeight: 600, cursor: 'pointer', transition: 'all 0.15s',
                      background: authTab === t ? '#fff' : 'transparent',
                      color: authTab === t ? '#111827' : '#6b7280',
                      boxShadow: authTab === t ? '0 1px 4px rgba(0,0,0,0.10)' : 'none',
                    }}>
                    {t === 'email' ? '✉ Email' : '📱 Phone OTP'}
                  </button>
                ))}
              </div>

              {/* ── Email tab ── */}
              {authTab === 'email' && (
                <>
                  {/* Sign In / Sign Up pill toggle */}
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

                  <Input type="email" value={email} onChange={e => { setEmail(e.target.value); clearError() }} placeholder="you@example.com" />
                  <Input
                    type={showPass ? 'text' : 'password'}
                    value={password}
                    onChange={e => { setPassword(e.target.value); clearError() }}
                    placeholder={isSignUp ? 'Create a password (min 6 chars)' : 'Your password'}
                    suffix={{ icon: <EyeIcon show={showPass} />, onClick: () => setShowPass(p => !p) }}
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
                </>
              )}

              {/* ── Phone OTP tab ── */}
              {authTab === 'phone' && (
                <>
                  <div style={{ display: 'flex', marginBottom: 12 }}>
                    <span style={{ display: 'inline-flex', alignItems: 'center', padding: '0 12px', border: '1.5px solid #d1d5db', borderRight: 'none', borderRadius: '10px 0 0 10px', background: '#f9fafb', fontSize: 14, color: '#6b7280', whiteSpace: 'nowrap' }}>
                      🇮🇳 +91
                    </span>
                    <input
                      type="tel" inputMode="numeric" maxLength={10}
                      value={phone}
                      onChange={e => { setPhone(e.target.value.replace(/\D/g, '')); clearError() }}
                      placeholder="9876543210"
                      style={{ flex: 1, border: '1.5px solid #d1d5db', borderLeft: 'none', borderRadius: '0 10px 10px 0', padding: '11px 14px', fontSize: 14, outline: 'none', fontFamily: 'inherit' }}
                      onFocus={e => { e.target.style.borderColor = ORANGE }}
                      onBlur={e => { e.target.style.borderColor = '#d1d5db' }}
                    />
                  </div>

                  {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '-6px 0 8px' }}>{error}</p>}

                  <PrimaryBtn onClick={handleSendOtp} loading={loading}>
                    {loading ? 'Sending OTP…' : 'Send OTP →'}
                  </PrimaryBtn>
                </>
              )}

              <p style={{ textAlign: 'center', fontSize: 11, color: '#9ca3af', marginTop: 14, marginBottom: 0 }}>
                You can browse CheckKaro without logging in.
              </p>
            </>
          )}

          {/* ══════════════ OTP VERIFY ══════════════ */}
          {step === 'otp' && (
            <>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 4px' }}>Enter OTP</h2>
              <p style={{ fontSize: 13, color: '#6b7280', margin: '0 0 18px' }}>Sent via SMS to <strong>+91 {phone}</strong></p>
              <input
                type="text" inputMode="numeric" maxLength={6}
                value={otp}
                onChange={e => { setOtp(e.target.value.replace(/\D/g, '')); clearError() }}
                onKeyDown={e => e.key === 'Enter' && handleVerifyOtp()}
                placeholder="——————"
                style={{ width: '100%', border: '1.5px solid #d1d5db', borderRadius: 10, padding: '14px', fontSize: 26, textAlign: 'center', letterSpacing: '0.3em', outline: 'none', boxSizing: 'border-box', fontFamily: 'inherit', marginBottom: 4 }}
                onFocus={e => { e.target.style.borderColor = ORANGE }}
                onBlur={e => { e.target.style.borderColor = '#d1d5db' }}
              />
              {error && <p style={{ color: '#ef4444', fontSize: 12, margin: '4px 0 8px' }}>{error}</p>}
              <PrimaryBtn onClick={handleVerifyOtp} loading={loading}>{loading ? 'Verifying…' : 'Verify OTP'}</PrimaryBtn>
              <div style={{ textAlign: 'center', marginTop: 12 }}>
                <GhostBtn onClick={() => { setStep('main'); setOtp(''); clearError() }}>← Change number</GhostBtn>
              </div>
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
              <Input type="email" value={resetEmail} onChange={e => { setResetEmail(e.target.value); clearError() }} placeholder="you@example.com" />
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
                {QUIZ_QUESTIONS.map(q => (
                  <div key={q.id}>
                    <p style={{ fontSize: 14, fontWeight: 600, color: '#374151', marginBottom: 8 }}>{q.question}</p>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                      {q.options.map(opt => {
                        const sel = quizAnswers[q.id] === opt
                        return (
                          <button key={opt} onClick={() => setQuizAnswers(p => ({ ...p, [q.id]: opt }))}
                            style={{ padding: '6px 12px', borderRadius: 999, fontSize: 13, fontWeight: 500, cursor: 'pointer', fontFamily: 'inherit', border: `1.5px solid ${sel ? ORANGE : '#d1d5db'}`, background: sel ? ORANGE : '#fff', color: sel ? '#fff' : '#374151' }}>
                            {opt}
                          </button>
                        )
                      })}
                    </div>
                  </div>
                ))}
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

          {/* ══════════════ DONE ══════════════ */}
          {step === 'done' && (
            <div style={{ textAlign: 'center', padding: '12px 0 16px' }}>
              <div style={{ width: 64, height: 64, borderRadius: '50%', background: '#dcfce7', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <svg width="30" height="30" fill="none" stroke="#16a34a" strokeWidth="2.5" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <h2 style={{ fontSize: 20, fontWeight: 700, color: '#111827', margin: '0 0 6px' }}>You're in!</h2>
              <p style={{ fontSize: 14, color: '#6b7280' }}>Welcome to CheckKaro. Know what's inside.</p>
            </div>
          )}

        </div>
      </div>
    </div>
  )
}
