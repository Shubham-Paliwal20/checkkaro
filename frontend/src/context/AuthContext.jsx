import { createContext, useContext, useEffect, useState } from 'react'
import { supabase } from '../lib/supabaseClient'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showAuthModal, setShowAuthModal] = useState(false)
  const [authModalStep, setAuthModalStep] = useState('contact')

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
      setLoading(false)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange(async (event, session) => {
      setUser(session?.user ?? null)

      // When user comes back after clicking the magic link email
      if (event === 'SIGNED_IN' && session?.user) {
        const userId = session.user.id
        const { data: profile } = await supabase
          .from('user_profiles')
          .select('id')
          .eq('id', userId)
          .maybeSingle()

        if (!profile) {
          // New user — create profile row and open quiz
          await supabase.from('user_profiles').insert({ id: userId })
          setAuthModalStep('quiz')
          setShowAuthModal(true)
        }
      }
    })

    return () => subscription.unsubscribe()
  }, [])

  const signOut = async () => {
    await supabase.auth.signOut()
    setUser(null)
  }

  const openAuthModal = (step = 'contact') => {
    setAuthModalStep(step)
    setShowAuthModal(true)
  }
  const closeAuthModal = () => {
    setShowAuthModal(false)
    setAuthModalStep('contact')
  }

  return (
    <AuthContext.Provider value={{ user, loading, signOut, showAuthModal, authModalStep, openAuthModal, closeAuthModal }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
