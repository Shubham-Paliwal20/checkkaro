import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const location = useLocation()
  const { user, signOut, openAuthModal } = useAuth()

  const isHome  = location.pathname === '/'
  const isAdmin = user?.email === 'shubhampaliwal5@gmail.com'

  useEffect(() => {
    const fn = () => setIsScrolled(window.scrollY > 10)
    window.addEventListener('scroll', fn)
    return () => window.removeEventListener('scroll', fn)
  }, [])

  const isActive = (path) => location.pathname === path

  const navLinks = [
    ...(!isHome ? [{ to: '/', label: 'Home' }] : []),
    { to: '/products',          label: 'Products' },
    { to: '/check-ingredient',  label: 'Check Ingredient' },
    { to: '/about',             label: 'About' },
    ...(isAdmin ? [{ to: '/admin', label: '🔐 Admin' }] : []),
  ]

  return (
    <nav className={`sticky top-0 z-50 bg-white transition-shadow duration-200 ${isScrolled ? 'shadow-md' : 'shadow-sm'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        {/* ── Main header row ── */}
        <div className="flex justify-between items-center h-[62px]">

          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <svg width="40" height="40" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="22" cy="22" r="17.5" fill="white" stroke="#FF9933" strokeWidth="4"/>
              <rect x="9" y="14" width="11" height="14" rx="2" fill="#4A87B8"/>
              <ellipse cx="14.5" cy="20" rx="3" ry="4" fill="white" opacity="0.85"/>
              <line x1="14.5" y1="15.5" x2="14.5" y2="24.5" stroke="#4A87B8" strokeWidth="1.2"/>
              <rect x="10" y="12" width="9" height="3" rx="1" fill="#4A87B8"/>
              <rect x="21" y="12" width="8" height="16" rx="2.5" fill="#4A87B8"/>
              <rect x="22.5" y="9" width="5" height="4" rx="1.5" fill="#4A87B8"/>
              <rect x="24" y="6.5" width="2" height="3.5" rx="1" fill="#4A87B8"/>
              <rect x="30" y="21" width="7.5" height="7" rx="2" fill="#4A87B8"/>
              <rect x="30.5" y="19" width="6.5" height="2.5" rx="1" fill="#4A87B8"/>
              <line x1="36" y1="36" x2="48" y2="48" stroke="#FF9933" strokeWidth="5.5" strokeLinecap="round"/>
            </svg>
            <div className="flex flex-col leading-tight">
              <div className="font-poppins font-bold text-lg md:text-xl">
                <span style={{ color: '#1B3F8A' }}>Parkho</span>
              </div>
              <span className="text-xs text-gray-400" style={{ marginTop: '-1px' }}>Know what's inside</span>
            </div>
          </Link>

          {/* Desktop nav links */}
          <div className="hidden md:flex items-center space-x-8">
            {navLinks.map(({ to, label }) => (
              <Link key={to} to={to}
                className={`text-sm font-medium transition-colors ${isActive(to) ? 'text-orange border-b-2 border-orange' : 'text-gray-700 hover:text-orange'}`}
                style={isActive(to) ? { color: '#FF9933' } : {}}>
                {label}
              </Link>
            ))}

            {/* Desktop login / user */}
            {user ? (
              <div className="flex items-center space-x-3">
                <span className="text-xs text-gray-500 truncate max-w-[120px]">{user.email || user.phone}</span>
                <button onClick={signOut}
                  className="text-sm font-medium text-gray-600 border border-gray-300 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors">
                  Logout
                </button>
              </div>
            ) : (
              <button onClick={() => openAuthModal()}
                className="text-sm font-semibold text-white px-4 py-1.5 rounded-lg transition-colors"
                style={{ backgroundColor: '#FF9933' }}>
                Login
              </button>
            )}
          </div>

          {/* Mobile: Login / Logout always visible in header */}
          <div className="md:hidden flex items-center gap-2">
            {user ? (
              <button onClick={signOut}
                className="text-xs font-semibold text-gray-600 border border-gray-300 px-3 py-1.5 rounded-lg">
                Logout
              </button>
            ) : (
              <button onClick={() => openAuthModal()}
                className="text-xs font-semibold text-white px-3 py-1.5 rounded-lg"
                style={{ backgroundColor: '#FF9933' }}>
                Login
              </button>
            )}
          </div>
        </div>

        {/* ── Mobile: scrollable nav strip (always visible, no hamburger) ── */}
        <div className="md:hidden flex items-center gap-1.5 overflow-x-auto pb-2 pt-0.5"
          style={{ scrollbarWidth: 'none', WebkitOverflowScrolling: 'touch', msOverflowStyle: 'none' }}>
          {navLinks.map(({ to, label }) => (
            <Link key={to} to={to}
              className="flex-shrink-0 text-xs font-semibold px-3 py-1.5 rounded-full transition-colors whitespace-nowrap"
              style={{
                backgroundColor: isActive(to) ? '#FF9933' : '#f3f4f6',
                color: isActive(to) ? '#fff' : '#374151',
              }}>
              {label}
            </Link>
          ))}
        </div>

      </div>

      {/* Hide scrollbar in webkit */}
      <style>{`.md\\:hidden::-webkit-scrollbar{display:none}`}</style>
    </nav>
  )
}

export default Navbar
