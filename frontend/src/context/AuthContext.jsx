import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const AuthContext = createContext(null)

// Decode JWT iat claim to tell fresh logins from page-load token restores
function tokenAge(accessToken) {
  try {
    const payload = JSON.parse(atob(accessToken.split('.')[1]))
    return Math.floor(Date.now() / 1000) - (payload.iat || 0)
  } catch { return Infinity }
}

export function AuthProvider({ children }) {
  const [user, setUser]               = useState(null)
  const [loading, setLoading]         = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authModalStep, setAuthModalStep] = useState('main')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      // Password recovery link clicked — show set-new-password form, don't silently log in
      if (event === 'PASSWORD_RECOVERY') {
        window.history.replaceState(null, '', window.location.pathname)
        setAuthModalStep('reset_password')
        setShowAuthModal(true)
        return
      }

      setUser(session?.user ?? null)
      setLoading(false)   // auth state is now known — stop spinning regardless of source

      // Wipe auth tokens from the URL the moment Supabase reads them.
      // Without this, sharing the post-login URL hands over your session to anyone who opens it.
      if (event === 'SIGNED_IN' && (window.location.hash || window.location.search.includes('code='))) {
        window.history.replaceState(null, '', window.location.pathname)
      }

      // Only show quiz on a genuinely fresh sign-in (token issued < 90s ago).
      // This prevents the quiz modal from firing on every page reload.
      if (event === 'SIGNED_IN' && session?.user && session.access_token) {
        if (tokenAge(session.access_token) > 90) return   // page-load token restore

        const userId = session.user.id
        const userEmail = session.user.email || null
        const { data: profile } = await supabase
          .from('user_profiles')
          .select('id, quiz_completed, email')
          .eq('id', userId)
          .maybeSingle()

        if (!profile) {
          await supabase.from('user_profiles').upsert({ id: userId, email: userEmail })
        } else if (userEmail && profile.email !== userEmail) {
          // Keep email in sync if user changes it
          await supabase.from('user_profiles').update({ email: userEmail }).eq('id', userId)
        }
        if (!profile?.quiz_completed) {
          setAuthModalStep('quiz')
          setShowAuthModal(true)
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  // Clear UI instantly — don't wait for network so mobile never feels stuck
  const signOut = async () => {
    setUser(null)
    setShowAuthModal(false)
    try { await supabase.auth.signOut() } catch (e) { console.warn('signOut:', e) }
  }

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
