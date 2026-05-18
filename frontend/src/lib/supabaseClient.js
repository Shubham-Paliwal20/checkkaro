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

// Force session refresh when the user returns to the tab after being away.
// Browsers throttle background tabs — the auto-refresh timer may not fire,
// leaving the JWT expired and all Supabase queries silently failing.
let _hiddenAt = 0
document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    _hiddenAt = Date.now()
  } else {
    const awayMs = Date.now() - _hiddenAt
    // If away for more than 4 minutes, the JWT may need refreshing
    if (_hiddenAt > 0 && awayMs > 4 * 60 * 1000) {
      supabase.auth.refreshSession().catch(() => {})
    }
  }
})
