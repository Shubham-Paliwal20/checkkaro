import { Link } from 'react-router-dom'

function Footer() {
  return (
    <footer className="bg-navy text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Left - Logo and Tagline */}
          <div>
            <div className="flex items-center space-x-2 mb-3">
              <svg className="w-8 h-8 text-primary" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5zm0 18c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6zm-1-10v5l4.25 2.52.77-1.28-3.52-2.09V10H11z"/>
              </svg>
              <span className="font-poppins font-bold text-xl">CheckKaro</span>
            </div>
            <p className="text-gray-400 text-sm">Be informed. Be aware.</p>
          </div>

          {/* Center - Navigation */}
          <div>
            <h3 className="font-poppins font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-gray-400 hover:text-primary transition-colors">Home</Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-400 hover:text-primary transition-colors">Products</Link>
              </li>
              <li>
                <Link to="/check-ingredient" className="text-gray-400 hover:text-primary transition-colors">Check Ingredient</Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-primary transition-colors">About</Link>
              </li>
            </ul>
          </div>

          {/* Right - Data Sources */}
          <div>
            <h3 className="font-poppins font-semibold mb-3">Data Sources</h3>
            <p className="text-gray-400 text-sm">
              Data sourced from Open Food Facts and public FSSAI guidelines, WHO, EFSA, and peer-reviewed research.
            </p>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-navy-light mt-8 pt-6 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} CheckKaro. For informational purposes only. Not medical advice.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
