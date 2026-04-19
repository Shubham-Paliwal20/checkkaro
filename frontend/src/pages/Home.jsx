import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import SearchBar from '../components/SearchBar'
import ReviewsSection from '../components/ReviewsSection'

function Home() {
  const navigate = useNavigate()

  const quickSearchItems = [
    { label: '🍜 Maggi Masala', query: 'Maggi 2-Minute Masala Noodles', cat: 'Instant Noodles' },
    { label: '🍪 Parle-G', query: 'Parle-G', cat: 'Biscuit' },
    { label: '🥤 Thums Up', query: 'Thums Up', cat: 'Soft Drink' },
    { label: '🧴 Dove Soap', query: 'Dove Soap', cat: 'Soap' },
    { label: '🌿 Parachute Oil', query: 'Parachute Coconut Oil', cat: 'Hair Care' },
    { label: '✨ Lakme Sunscreen', query: 'Lakme Sun Expert SPF 50', cat: 'Skincare' },
    { label: '🧈 Amul Butter', query: 'Amul Butter', cat: 'Dairy' },
    { label: '🌶 Kurkure', query: 'Kurkure Masala Munch', cat: 'Snack' },
  ]

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      {/* Hero Section */}
      <section className="min-h-screen flex flex-col justify-center items-center px-4 bg-white pt-16 sm:pt-0">
        <div className="max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-block mb-4 sm:mb-6">
            <span className="inline-flex items-center gap-2 px-4 sm:px-5 py-2 rounded-full text-xs sm:text-sm font-semibold border-2"
              style={{ background: 'linear-gradient(90deg, #fff7ed 0%, #f0fdf4 100%)', borderColor: '#e5e7eb', color: '#374151' }}>
              <span className="flex items-center gap-1">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#FF9933' }}></span>
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#ffffff', border: '1.5px solid #d1d5db' }}></span>
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#138808' }}></span>
              </span>
              <span>
                <span style={{ color: '#FF9933', fontWeight: 700 }}>Loved</span>
                {' by users across '}
                <span style={{ color: '#138808', fontWeight: 700 }}>India</span>
              </span>
            </span>
          </div>

          {/* Main Heading */}
          <h1 className="font-poppins mb-6">
            <div className="text-3xl sm:text-4xl md:text-6xl font-normal text-navy">Know Your</div>
            <div className="text-3xl sm:text-4xl md:text-6xl font-black flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-3">
              <span className="text-orange">FOOD</span>
              <span className="text-gray-400 text-2xl sm:text-4xl md:text-6xl">AND</span>
              <span className="text-primary">COSMETIC</span>
            </div>
            <div className="text-3xl sm:text-4xl md:text-6xl font-normal text-navy">Products</div>
          </h1>

          {/* Subtitle */}
          <p className="text-base sm:text-lg text-gray-500 max-w-xl mx-auto mb-8 sm:mb-10 px-4">
            Search any Indian product and understand every ingredient — explained simply, no jargon, no confusion.
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto mb-4">
            <SearchBar placeholder="Search any product... e.g., Maggi, Dove Soap, Parle-G" />
          </div>

          {/* Quick Search Chips */}
          <div className="flex flex-wrap gap-2 justify-center items-center px-4 mt-2">
            <span className="text-sm text-gray-400 w-full text-center mb-1">Popular searches across categories</span>
            {quickSearchItems.map((item, idx) => (
              <button
                key={idx}
                onClick={() => navigate(`/result/${encodeURIComponent(item.query)}`)}
                className="flex flex-col items-center bg-white border border-gray-200 rounded-2xl px-3 sm:px-4 py-2 text-xs sm:text-sm hover:shadow-md hover:border-orange transition-all group"
              >
                <span className="font-medium text-gray-800 group-hover:text-orange transition-colors">{item.label}</span>
                <span className="text-[10px] text-gray-400 mt-0.5">{item.cat}</span>
              </button>
            ))}
          </div>

          {/* Scroll Indicator */}
          <motion.div
            className="mt-12 sm:mt-16 hidden sm:block"
            animate={{ y: [0, 10, 0] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
          >
            <svg className="w-6 h-6 mx-auto text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 sm:py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-8 sm:mb-12">
            <p className="text-sm text-orange font-semibold uppercase tracking-wide mb-2">What CheckKaro Does</p>
            <h2 className="section-heading text-2xl sm:text-3xl">Everything you need to know</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 max-w-5xl mx-auto">
            {/* Food Analysis */}
            <div className="card p-6 sm:p-8 hover:shadow-md transition-shadow border-l-4 border-orange">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-orange-light rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-orange" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3zM16 16.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zM6.5 18a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
                </svg>
              </div>
              <h3 className="font-poppins font-semibold text-lg sm:text-xl text-orange mb-3">Food Analysis</h3>
              <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                CheckKaro breaks down every ingredient in your favourite Indian packaged foods — from Maggi to biscuits. Understand what each ingredient is and how it is viewed by regulators worldwide.
              </p>
              <a href="/products" className="text-orange text-sm font-medium hover:underline">
                Search a food product →
              </a>
            </div>

            {/* Cosmetic Analysis */}
            <div className="card p-6 sm:p-8 hover:shadow-md transition-shadow border-l-4 border-primary">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-primary-light rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732l-3.354 1.935-1.18 4.455a1 1 0 01-1.933 0L9.854 12.8 6.5 10.866a1 1 0 010-1.732l3.354-1.935 1.18-4.455A1 1 0 0112 2z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="font-poppins font-semibold text-lg sm:text-xl text-primary mb-3">Cosmetic Analysis</h3>
              <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                From fairness creams to shampoos, CheckKaro analyses ingredients in Indian personal care and cosmetic products and highlights chemicals commonly avoided in other countries.
              </p>
              <a href="/products" className="text-primary text-sm font-medium hover:underline">
                Search a cosmetic →
              </a>
            </div>

            {/* Check Ingredient */}
            <div className="card p-6 sm:p-8 hover:shadow-md transition-shadow border-l-4 border-orange">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-orange-light rounded-full flex items-center justify-center mb-4">
                <svg className="w-6 h-6 sm:w-8 sm:h-8 text-orange" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 9a2 2 0 114 0 2 2 0 01-4 0z" />
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a4 4 0 00-3.446 6.032l-2.261 2.26a1 1 0 101.414 1.415l2.261-2.261A4 4 0 1011 5z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="font-poppins font-semibold text-lg sm:text-xl text-orange mb-3">Check Any Ingredient</h3>
              <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                Spotted an unfamiliar ingredient on a label? Type it directly and get a clear plain-English explanation of what it is, where it is found, and its regulatory status globally.
              </p>
              <a href="/check-ingredient" className="text-orange text-sm font-medium hover:underline">
                Check an ingredient →
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16 sm:py-24 bg-gray-soft">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="section-heading text-center mb-8 sm:mb-12 text-2xl sm:text-3xl">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-orange text-white rounded-full flex items-center justify-center text-xl sm:text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-poppins font-semibold text-base sm:text-lg mb-2">Search</h3>
              <p className="text-gray-600 text-sm">Type any Indian product or ingredient name</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-white border-2 border-orange text-orange rounded-full flex items-center justify-center text-xl sm:text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-poppins font-semibold text-base sm:text-lg mb-2">Analyse</h3>
              <p className="text-gray-600 text-sm">We check every ingredient against regulatory databases</p>
            </div>
            
            <div className="text-center">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-primary text-black rounded-full flex items-center justify-center text-xl sm:text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-poppins font-semibold text-base sm:text-lg mb-2">Understand</h3>
              <p className="text-gray-600 text-sm">Get a clear breakdown without confusing jargon</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Bar */}
      <section className="py-12 sm:py-16 bg-gradient-to-r from-orange-light via-white to-primary-light">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 sm:gap-8 text-center">
            <div>
              <div className="text-3xl sm:text-4xl font-poppins font-bold text-orange mb-2">500+</div>
              <p className="text-gray-600 text-sm sm:text-base">Ingredients classified in our database</p>
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-poppins font-bold text-navy mb-2">360+</div>
              <p className="text-gray-600 text-sm sm:text-base">Indian products analysed across categories</p>
            </div>
            <div>
              <div className="text-3xl sm:text-4xl font-poppins font-bold text-primary mb-2">100%</div>
              <p className="text-gray-600 text-sm sm:text-base">Free — No login, no subscription needed</p>
            </div>
          </div>
        </div>
      </section>

      {/* Reviews Carousel Section */}
      <ReviewsSection />

      {/* Check Ingredient Promo */}
      <section className="py-12 sm:py-16 bg-navy text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8 items-center text-center md:text-left">
            <div>
              <h2 className="font-poppins text-2xl sm:text-3xl font-bold mb-4">
                Not sure about an ingredient?
              </h2>
              <p className="text-gray-300 mb-6 text-sm sm:text-base leading-relaxed">
                Type any ingredient name or E-number from a product label and get instant information about what it is, where it's used, and its regulatory status.
              </p>
            </div>
            <div className="flex justify-center md:justify-end">
              <button
                onClick={() => navigate('/check-ingredient')}
                className="bg-orange text-white px-6 sm:px-8 py-3 sm:py-4 rounded-full font-semibold hover:bg-orange-dark transition-colors shadow-lg text-sm sm:text-base"
              >
                Check an Ingredient
              </button>
            </div>
          </div>
        </div>
      </section>
    </motion.div>
  )
}

export default Home
