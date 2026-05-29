import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.warn('Supabase env vars missing. Auth features will be disabled.')
}

export const supabase = createClient(
  supabaseUrl || 'https://placeholder.supabase.co',
  supabaseAnonKey || 'placeholder',
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true,
    },
  }
)

// When the user returns to the tab after browsers throttled timers in the background,
// refresh the JWT if it may have expired — but only if there's an active session.
let _hiddenAt = 0
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    _hiddenAt = Date.now()
  } else {
    const awayMs = Date.now() - _hiddenAt
    if (_hiddenAt > 0 && awayMs > 4 * 60 * 1000) {
      supabase.auth.getSession().then(({ data: { session } }) => {
        if (session) supabase.auth.refreshSession().catch(() => {})
      })
    }
  }
})
