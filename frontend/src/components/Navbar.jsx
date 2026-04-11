import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'

function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const isActive = (path) => location.pathname === path

  return (
    <nav className={`sticky top-0 z-50 bg-white transition-shadow duration-200 ${isScrolled ? 'shadow-md' : 'shadow-sm'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-[68px]">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <svg className="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-10v5l4.25 2.52.77-1.28-3.52-2.09V10H11z"/>
            </svg>
            <div className="flex flex-col">
              <span className="font-poppins font-bold text-primary text-xl">CheckKaro</span>
              <span className="text-xs text-gray-500 -mt-1">Know what's inside</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link 
              to="/products" 
              className={`text-sm font-medium transition-colors ${isActive('/products') ? 'text-primary border-b-2 border-primary' : 'text-gray-700 hover:text-primary'}`}
            >
              Products
            </Link>
            <Link 
              to="/check-ingredient" 
              className={`text-sm font-medium transition-colors ${isActive('/check-ingredient') ? 'text-primary border-b-2 border-primary' : 'text-gray-700 hover:text-primary'}`}
            >
              Check Ingredient
            </Link>
            <Link 
              to="/about" 
              className={`text-sm font-medium transition-colors ${isActive('/about') ? 'text-primary border-b-2 border-primary' : 'text-gray-700 hover:text-primary'}`}
            >
              About
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button 
            className="md:hidden p-2"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <svg className="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {isMobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-100">
            <Link 
              to="/products" 
              className="block py-2 text-sm font-medium text-gray-700 hover:text-primary"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Products
            </Link>
            <Link 
              to="/check-ingredient" 
              className="block py-2 text-sm font-medium text-gray-700 hover:text-primary"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Check Ingredient
            </Link>
            <Link 
              to="/about" 
              className="block py-2 text-sm font-medium text-gray-700 hover:text-primary"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              About
            </Link>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar
