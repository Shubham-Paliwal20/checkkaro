import { Link } from 'react-router-dom'

function Footer() {
  return (
    <footer className="bg-navy text-white">

      {/* Social Banner */}
      <div className="border-b border-white/10 py-12 sm:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="font-poppins text-2xl sm:text-4xl font-bold text-white mb-6">
            Get Connected with us on social network
          </p>
          <a
            href="https://instagram.com/parkho.in"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 bg-white/10 hover:bg-orange transition-colors rounded-full px-6 py-3 group"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-white">
              <rect x="2" y="2" width="20" height="20" rx="5.5" stroke="currentColor" strokeWidth="1.8"/>
              <circle cx="12" cy="12" r="4.5" stroke="currentColor" strokeWidth="1.8"/>
              <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
            </svg>
            <span className="text-white font-semibold text-base">@parkho.in</span>
          </a>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Left - Logo and Tagline */}
          <div>
            <div className="flex items-center gap-2.5 mb-3">
              <svg width="40" height="40" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Magnifying glass — orange ring */}
                <circle cx="22" cy="22" r="17.5" fill="white" fillOpacity="0.08" stroke="#FF9933" strokeWidth="4"/>
                {/* Jar with leaf */}
                <rect x="9" y="14" width="11" height="14" rx="2" fill="#4A87B8"/>
                <ellipse cx="14.5" cy="20" rx="3" ry="4" fill="white" opacity="0.85"/>
                <line x1="14.5" y1="15.5" x2="14.5" y2="24.5" stroke="#4A87B8" strokeWidth="1.2"/>
                <rect x="10" y="12" width="9" height="3" rx="1" fill="#4A87B8"/>
                {/* Pump bottle */}
                <rect x="21" y="12" width="8" height="16" rx="2.5" fill="#4A87B8"/>
                <rect x="22.5" y="9" width="5" height="4" rx="1.5" fill="#4A87B8"/>
                <rect x="24" y="6.5" width="2" height="3.5" rx="1" fill="#4A87B8"/>
                {/* Small container */}
                <rect x="30" y="21" width="7.5" height="7" rx="2" fill="#4A87B8"/>
                <rect x="30.5" y="19" width="6.5" height="2.5" rx="1" fill="#4A87B8"/>
                {/* Handle */}
                <line x1="36" y1="36" x2="48" y2="48" stroke="#FF9933" strokeWidth="5.5" strokeLinecap="round"/>
              </svg>
              <div className="flex flex-col leading-tight">
                <div className="font-poppins font-bold text-xl text-white">
                  Parkho
                </div>
                <span className="text-xs text-gray-400" style={{ marginTop: '-1px' }}>Know what's inside</span>
              </div>
            </div>
            <p className="text-gray-400 text-sm">Be informed. Be aware.</p>
          </div>

          {/* Center - Navigation */}
          <div>
            <h3 className="font-poppins font-semibold mb-3">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-gray-400 hover:text-orange transition-colors">Home</Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-400 hover:text-orange transition-colors">Products</Link>
              </li>
              <li>
                <Link to="/check-ingredient" className="text-gray-400 hover:text-orange transition-colors">Check Ingredient</Link>
              </li>
              <li>
                <Link to="/blog" className="text-gray-400 hover:text-orange transition-colors">Blog</Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-orange transition-colors">About</Link>
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
          <p>&copy; {new Date().getFullYear()} Parkho. For informational purposes only. Not medical advice.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
