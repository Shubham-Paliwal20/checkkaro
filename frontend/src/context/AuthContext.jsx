import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authModalStep, setAuthModalStep] = useState('main')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      setUser(session?.user ?? null)

      // On every sign-in: show quiz until completed (handles Google OAuth redirect & magic link)
      if (event === 'SIGNED_IN' && session?.user) {
        const userId = session.user.id
        const { data: profile } = await supabase
          .from('user_profiles')
          .select('id, quiz_completed')
          .eq('id', userId)
          .maybeSingle()

        if (!profile) {
          await supabase.from('user_profiles').upsert({ id: userId })
        }
        if (!profile?.quiz_completed) {
          setAuthModalStep('quiz')
          setShowAuthModal(true)
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const signOut = async () => {
    setShowAuthModal(false)
    await supabase.auth.signOut()
    setUser(null)
  }

  const openAuthModal = (step) => {
    // Guard: if called as onClick handler, step will be a SyntheticEvent — ignore it
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
