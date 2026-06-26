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

// Keep Render backend awake. Render free tier spins down after 15 min of inactivity.
// Ping every 2 min — if the ping times out (backend is waking up), retry after 35s
// so the backend is warm before the user's next real request.
function usePrewarm() {
  useEffect(() => {
    const ping = () =>
      axios.get(`${API_BASE_URL}/health`, { timeout: 60000 }).catch(() => {
        // Backend was sleeping — it's waking up now. Retry once after 35s.
        setTimeout(() => axios.get(`${API_BASE_URL}/health`, { timeout: 60000 }).catch(() => {}), 35000)
      })
    ping()
    const id = setInterval(ping, 2 * 60 * 1000)
    // When user returns to tab after being away, ping immediately
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
