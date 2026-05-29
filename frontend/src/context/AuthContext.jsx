import { createContext, useContext, useEffect, useRef, useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const AuthContext = createContext(null)

const INACTIVITY_MS = 30 * 60 * 1000

function tokenAge(accessToken) {
  try {
    const payload = JSON.parse(atob(accessToken.split('.')[1]))
    return Math.floor(Date.now() / 1000) - (payload.iat || 0)
  } catch { return Infinity }
}

// Wipe every Supabase auth key from localStorage and sessionStorage directly.
// This runs before calling supabase.auth.signOut() so that even if the SDK
// throws (e.g. storage lock conflict), the session is already gone from disk.
function clearSupabaseStorage() {
  for (const storage of [localStorage, sessionStorage]) {
    try {
      Object.keys(storage)
        .filter(k => k.startsWith('sb-'))
        .forEach(k => storage.removeItem(k))
    } catch (_) {}
  }
}

export function AuthProvider({ children }) {
  const [user, setUser]               = useState(null)
  const [loading, setLoading]         = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authModalStep, setAuthModalStep] = useState('main')

  // Guards the onAuthStateChange listener from restoring the user
  // while a sign-out is in progress (prevents race with auto-refresh)
  const signingOut = useRef(false)
  const signOutFn  = useRef(null)  // keeps inactivity timer pointing at latest signOut

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      // Always handle sign-out cleanly regardless of the guard
      if (event === 'SIGNED_OUT') {
        setUser(null)
        setLoading(false)
        signingOut.current = false
        return
      }

      // Block any SIGNED_IN / TOKEN_REFRESHED events that arrive while we're
      // in the middle of signing out — these are stale callbacks from the
      // auto-refresh timer firing concurrently with the logout call.
      if (signingOut.current) return

      if (event === 'PASSWORD_RECOVERY') {
        window.history.replaceState(null, '', window.location.pathname)
        setAuthModalStep('reset_password')
        setShowAuthModal(true)
        return
      }

      setUser(session?.user ?? null)
      setLoading(false)

      // Remove auth tokens from the URL immediately so the link isn't reusable.
      if (event === 'SIGNED_IN' && (window.location.hash || window.location.search.includes('code='))) {
        window.history.replaceState(null, '', window.location.pathname)
      }

      // Only show the quiz on a genuinely fresh sign-in, not on page-load token restores.
      if (event === 'SIGNED_IN' && session?.user && session.access_token) {
        if (tokenAge(session.access_token) > 90) return

        const userId = session.user.id
        const { data: profile } = await supabase
          .from('user_profiles')
          .select('id, quiz_completed')
          .eq('id', userId)
          .maybeSingle()

        if (!profile) await supabase.from('user_profiles').upsert({ id: userId })
        if (!profile?.quiz_completed) {
          setAuthModalStep('quiz')
          setShowAuthModal(true)
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const signOut = async () => {
    signingOut.current = true   // block stray auth events immediately

    // Clear UI before any async work
    setUser(null)
    setShowAuthModal(false)

    // Force-wipe storage directly so the session is gone even if the SDK call fails
    clearSupabaseStorage()

    // Tell Supabase server to invalidate the refresh token (best-effort; we don't
    // depend on this succeeding — local storage is already clear)
    try {
      await supabase.auth.signOut({ scope: 'global' })
    } catch (e) {
      console.warn('signOut server call failed (session cleared locally):', e)
    }

    // Release the guard after a short window to handle any last stray events
    setTimeout(() => { signingOut.current = false }, 1500)
  }

  signOutFn.current = signOut

  // Auto-logout after 30 minutes of inactivity — only runs while logged in
  useEffect(() => {
    if (!user) return

    let timer
    const reset = () => {
      clearTimeout(timer)
      timer = setTimeout(() => signOutFn.current(), INACTIVITY_MS)
    }

    const EVENTS = ['mousemove', 'mousedown', 'keydown', 'scroll', 'touchstart', 'click']
    EVENTS.forEach(e => window.addEventListener(e, reset, { passive: true }))
    reset()

    return () => {
      clearTimeout(timer)
      EVENTS.forEach(e => window.removeEventListener(e, reset))
    }
  }, [user])

  const openAuthModal = (step) => {
    const s = typeof step === 'string' ? step : 'main'
    setAuthModalStep(s)
    setShowAuthModal(true)
  }

  const closeAuthModal = () => {
    setShowAuthModal(false)
    setAuthModalStep('main')
  }

  return (
    <AuthContext.Provider value={{ user, loading, signOut, showAuthModal, authModalStep, openAuthModal, closeAuthModal }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
