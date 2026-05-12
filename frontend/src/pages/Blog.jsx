import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const CATEGORIES = ['All', 'Food', 'Cosmetics', 'Health', 'Lifestyle', 'Product Review']

const CAT_COLORS = {
  'Food':           'bg-orange-100 text-orange-700',
  'Cosmetics':      'bg-pink-100 text-pink-700',
  'Health':         'bg-green-100 text-green-700',
  'Lifestyle':      'bg-blue-100 text-blue-700',
  'Product Review': 'bg-purple-100 text-purple-700',
  'General':        'bg-gray-100 text-gray-700',
}

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  const days = Math.floor(hrs / 24)
  if (days < 30) return `${days}d ago`
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

export default function Blog() {
  const [blogs, setBlogs]       = useState([])
  const [loading, setLoading]   = useState(true)
  const [category, setCategory] = useState('All')
  const { user, openAuthModal } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    fetchBlogs()
  }, [])

  async function fetchBlogs() {
    setLoading(true)
    const { data } = await supabase
      .from('blogs')
      .select('id, title, slug, excerpt, category, author_name, cover_image, created_at')
      .eq('status', 'approved')
      .order('created_at', { ascending: false })
    setBlogs(data || [])
    setLoading(false)
  }

  const filtered = category === 'All' ? blogs : blogs.filter(b => b.category === category)

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Hero */}
      <div style={{ background: 'linear-gradient(135deg, #1B3F8A 0%, #2d5bc7 100%)' }} className="text-white py-16 px-4">
        <div className="max-w-5xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-1.5 text-sm font-medium mb-4">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Community Blogs
          </div>
          <h1 className="font-poppins font-bold text-3xl sm:text-5xl mb-4">Know More. Share More.</h1>
          <p className="text-blue-100 text-base sm:text-lg max-w-2xl mx-auto mb-8">
            Real people sharing real insights about food ingredients, cosmetics, and healthy living in India.
          </p>
          <button
            onClick={() => user ? navigate('/blog/write') : openAuthModal()}
            style={{ background: '#FF9933' }}
            className="text-white font-bold px-8 py-3 rounded-xl text-base hover:opacity-90 transition-opacity shadow-lg"
          >
            ✍️ Write a Blog
          </button>
          {!user && <p className="text-blue-200 text-xs mt-2">Login required to write</p>}
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-10">

        {/* Category filter */}
        <div className="flex gap-2 flex-wrap mb-8">
          {CATEGORIES.map(cat => (
            <button key={cat} onClick={() => setCategory(cat)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all border ${
                category === cat
                  ? 'bg-navy text-white border-navy'
                  : 'bg-white text-gray-600 border-gray-200 hover:border-navy hover:text-navy'
              }`}
              style={category === cat ? { backgroundColor: '#1B3F8A', borderColor: '#1B3F8A' } : {}}>
              {cat}
            </button>
          ))}
        </div>

        {/* Blog grid */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1,2,3,4,5,6].map(i => (
              <div key={i} className="bg-white rounded-2xl overflow-hidden shadow-sm animate-pulse">
                <div className="h-44 bg-gray-200" />
                <div className="p-5 space-y-3">
                  <div className="h-3 bg-gray-200 rounded w-1/3" />
                  <div className="h-5 bg-gray-200 rounded w-3/4" />
                  <div className="h-3 bg-gray-200 rounded w-full" />
                  <div className="h-3 bg-gray-200 rounded w-2/3" />
                </div>
              </div>
            ))}
          </div>
        ) : filtered.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📝</div>
            <h3 className="font-poppins font-semibold text-navy text-xl mb-2">No blogs yet</h3>
            <p className="text-gray-500 mb-6">Be the first to write about {category === 'All' ? 'anything' : category}!</p>
            <button onClick={() => user ? navigate('/blog/write') : openAuthModal()}
              style={{ background: '#FF9933' }}
              className="text-white font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity">
              Write First Blog
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map(blog => (
              <Link key={blog.id} to={`/blog/${blog.slug}`}
                className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group border border-gray-100">
                {/* Cover image */}
                <div className="h-44 bg-gradient-to-br from-blue-50 to-orange-50 overflow-hidden relative">
                  {blog.cover_image ? (
                    <img src={blog.cover_image} alt={blog.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <svg className="w-16 h-16 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                  )}
                  {blog.category && (
                    <span className={`absolute top-3 left-3 text-xs font-semibold px-2.5 py-1 rounded-full ${CAT_COLORS[blog.category] || CAT_COLORS['General']}`}>
                      {blog.category}
                    </span>
                  )}
                </div>
                <div className="p-5">
                  <h2 className="font-poppins font-bold text-navy text-base leading-snug mb-2 group-hover:text-orange-500 transition-colors line-clamp-2"
                    style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {blog.title}
                  </h2>
                  {blog.excerpt && (
                    <p className="text-gray-500 text-sm leading-relaxed mb-4"
                      style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {blog.excerpt}
                    </p>
                  )}
                  <div className="flex items-center justify-between text-xs text-gray-400 pt-3 border-t border-gray-100">
                    <span className="font-medium text-gray-600">✍ {blog.author_name || 'Anonymous'}</span>
                    <span>{timeAgo(blog.created_at)}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
