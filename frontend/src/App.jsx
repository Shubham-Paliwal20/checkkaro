import { useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return null
}
import { AnimatePresence } from 'framer-motion'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import AuthModal from './components/AuthModal'
import Home from './pages/Home'
import Result from './pages/Result'
import CheckIngredient from './pages/CheckIngredient'
import Products from './pages/Products'
import About from './pages/About'
import Admin from './pages/Admin'
import Blog from './pages/Blog'
import BlogPost from './pages/BlogPost'
import WriteBlog from './pages/WriteBlog'
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://checkkaro.onrender.com'

// Keep Render backend awake — ping on load, every 4 min, and immediately when
// the user returns to the tab (setInterval is throttled in background tabs, so
// Render can sleep during a long away period; the visibility ping wakes it fast).
function usePrewarm() {
  useEffect(() => {
    const ping = () => axios.get(`${API_BASE_URL}/health`, { timeout: 30000 }).catch(() => {})
    ping()
    const id = setInterval(ping, 4 * 60 * 1000)
    const onVisible = () => { if (!document.hidden) ping() }
    document.addEventListener('visibilitychange', onVisible)
    return () => {
      clearInterval(id)
      document.removeEventListener('visibilitychange', onVisible)
    }
  }, [])
}

function AnimatedRoutes() {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <ScrollToTop />
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Home />} />
        <Route path="/result/:productName" element={<Result />} />
        <Route path="/check-ingredient" element={<CheckIngredient />} />
        <Route path="/products" element={<Products />} />
        <Route path="/about" element={<About />} />
        <Route path="/blog" element={<Blog />} />
        <Route path="/blog/write" element={<WriteBlog />} />
        <Route path="/blog/:slug" element={<BlogPost />} />
        <Route path="/admin" element={<Admin />} />
      </Routes>
    </AnimatePresence>
  )
}

function AppShell() {
  const { showAuthModal, authModalStep, closeAuthModal } = useAuth()
  usePrewarm()

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <AnimatedRoutes />
      </main>
      <Footer />
      {showAuthModal && <AuthModal onClose={closeAuthModal} initialStep={authModalStep} />}
    </div>
  )
}

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppShell />
      </AuthProvider>
    </Router>
  )
}

export default App
