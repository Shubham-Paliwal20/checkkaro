import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'
import { STATIC_BLOGS } from './Blog'

const CAT_COLORS = {
  'Food':           { bg: '#fff7ed', text: '#ea580c' },
  'Cosmetics':      { bg: '#fdf2f8', text: '#be185d' },
  'Health':         { bg: '#f0fdf4', text: '#15803d' },
  'Lifestyle':      { bg: '#eff6ff', text: '#1d4ed8' },
  'Product Review': { bg: '#faf5ff', text: '#7e22ce' },
}

const AUTHOR_BIO = {
  'Parkho Editorial': {
    bio: 'The Parkho Editorial team researches and writes about food ingredients, cosmetics, and consumer health in India. Our mission is to help people make informed choices about what they eat and apply to their skin.',
    avatar: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&q=80',
  },
}

function renderContent(content) {
  return content.split('\n').filter(p => p.trim()).map((para, i) => {
    if (para.startsWith('**') && para.endsWith('**')) {
      return <h3 key={i} className="font-poppins font-bold text-lg mt-8 mb-3" style={{ color: '#1B3F8A' }}>{para.replace(/\*\*/g, '')}</h3>
    }
    if (para.startsWith('- **')) {
      const parts = para.replace('- **', '').split('**:')
      return <li key={i} className="mb-2 ml-4 list-disc"><strong style={{ color: '#1B3F8A' }}>{parts[0]}</strong>{parts[1] ? `: ${parts[1]}` : ''}</li>
    }
    if (para.startsWith('- ')) {
      return <li key={i} className="mb-2 ml-4 list-disc text-gray-700">{para.replace('- ', '')}</li>
    }
    if (/^\d+\./.test(para)) {
      return <li key={i} className="mb-2 ml-4 list-decimal text-gray-700">{para.replace(/^\d+\.\s/, '')}</li>
    }
    const rendered = para
      .replace(/\*\*(.+?)\*\*/g, '<strong style="color:#1B3F8A">$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
    return <p key={i} className="text-gray-700 leading-relaxed text-base mb-5" dangerouslySetInnerHTML={{ __html: rendered }} />
  })
}

export default function BlogPost() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [blog, setBlog]       = useState(null)
  const [related, setRelated] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => { fetchBlog() }, [slug])

  async function fetchBlog() {
    setLoading(true)
    const staticMatch = STATIC_BLOGS.find(b => b.slug === slug)
    if (staticMatch) {
      setBlog(staticMatch)
      setRelated(STATIC_BLOGS.filter(b => b.slug !== slug && b.category === staticMatch.category).slice(0, 3))
      setLoading(false)
      return
    }
    const { data } = await supabase.from('blogs').select('*').eq('slug', slug).eq('status', 'approved').maybeSingle()
    setBlog(data)
    if (data?.category) {
      const { data: rel } = await supabase
        .from('blogs').select('id,title,slug,author_name,created_at,cover_image,category')
        .eq('status', 'approved').eq('category', data.category).neq('slug', slug).limit(3)
      setRelated([...(rel || []), ...STATIC_BLOGS.filter(b => b.category === data.category && b.slug !== slug)].slice(0, 3))
    }
    setLoading(false)
  }

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="animate-spin w-8 h-8 border-4 border-orange-400 border-t-transparent rounded-full" />
    </div>
  )

  if (!blog) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="text-center">
        <div className="text-5xl mb-4">📭</div>
        <h2 className="font-poppins font-bold text-2xl mb-2" style={{ color: '#1B3F8A' }}>Blog not found</h2>
        <p className="text-gray-500 mb-6">This blog may have been removed or is pending approval.</p>
        <Link to="/blog" style={{ background: '#FF9933' }} className="text-white font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity">
          Back to Blogs
        </Link>
      </div>
    </div>
  )

  const catColor = CAT_COLORS[blog.category] || { bg: '#f3f4f6', text: '#374151' }
  const readTime = Math.max(1, Math.ceil(blog.content.split(/\s+/).length / 200))
  const authorInfo = AUTHOR_BIO[blog.author_name] || null

  return (
    <div className="min-h-screen bg-gray-50">

      {/* ── HERO / COVER ── */}
      <div className="relative w-full overflow-hidden" style={{ minHeight: 320 }}>
        <img
          src={blog.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200&q=80'}
          alt={blog.title}
          style={{ display: 'block', width: '100%', height: 'auto', maxHeight: 480, objectFit: 'cover', objectPosition: 'center top' }}
          onError={e => { e.target.onerror = null; e.target.src = 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=1200&q=80' }}
        />
        <div className="absolute inset-0" style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.0) 40%, rgba(0,0,0,0.75) 100%)' }} />
        <div className="absolute inset-0 flex flex-col justify-between" style={{ minHeight: 320 }}>
          {/* Back button top */}
          <div className="max-w-6xl mx-auto px-4 pt-6 w-full">
            <button onClick={() => navigate('/blog')}
              className="flex items-center gap-2 text-white/80 hover:text-white text-sm transition-colors bg-black/20 backdrop-blur-sm px-3 py-1.5 rounded-lg w-fit">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              All Blogs
            </button>
          </div>
          {/* Title bottom */}
          <div className="max-w-6xl mx-auto px-4 pb-10 w-full">
            {blog.category && (
              <span style={{ background: catColor.bg, color: catColor.text }}
                className="inline-block text-xs font-bold px-3 py-1 rounded-full mb-4">
                {blog.category}
              </span>
            )}
            <h1 className="font-poppins font-black text-white leading-tight max-w-3xl"
              style={{ fontSize: 'clamp(20px, 4vw, 36px)', textShadow: '0 2px 12px rgba(0,0,0,0.5)' }}>
              {blog.title}
            </h1>
          </div>
        </div>
      </div>

      {/* ── AUTHOR META BAR ── */}
      <div className="bg-white border-b border-gray-100 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-wrap items-center gap-4 justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-orange-200 flex-shrink-0">
              {authorInfo?.avatar
                ? <img src={authorInfo.avatar} alt={blog.author_name} className="w-full h-full object-cover" onError={e => { e.target.style.display='none'; e.target.nextSibling && (e.target.nextSibling.style.display='flex') }} />
                : <div className="w-full h-full flex items-center justify-center text-white font-bold text-sm" style={{ background: '#1B3F8A' }}>{(blog.author_name || 'A')[0].toUpperCase()}</div>
              }
            </div>
            <div>
              <p className="font-semibold text-sm" style={{ color: '#1B3F8A' }}>{blog.author_name || 'Anonymous'}</p>
              <p className="text-xs text-gray-400">{new Date(blog.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</p>
            </div>
          </div>
          <div className="flex items-center gap-4 text-xs text-gray-400">
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {readTime} min read
            </span>
            <span style={{ background: catColor.bg, color: catColor.text }} className="font-bold px-3 py-1 rounded-full text-xs">
              {blog.category}
            </span>
          </div>
        </div>
      </div>

      {/* ── CONTENT + SIDEBAR ── */}
      <div className="max-w-6xl mx-auto px-4 py-10">
        <div className="flex flex-col lg:flex-row gap-10">

          {/* ── MAIN CONTENT ── */}
          <article className="flex-1 min-w-0">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-10">
              {blog.excerpt && (
                <div className="border-l-4 bg-gray-50 rounded-r-xl px-5 py-4 mb-8 italic text-gray-600 text-base leading-relaxed"
                  style={{ borderColor: '#FF9933' }}>
                  {blog.excerpt}
                </div>
              )}
              <div className="prose max-w-none">
                {renderContent(blog.content)}
              </div>
            </div>

            {/* Tags */}
            <div className="mt-6 flex flex-wrap gap-2">
              {['Ingredients', blog.category, 'Parkho', 'India', 'Consumer Awareness'].map(tag => (
                <span key={tag} className="bg-white border border-gray-200 text-gray-500 text-xs font-medium px-3 py-1.5 rounded-full">
                  #{tag.replace(' ', '')}
                </span>
              ))}
            </div>
          </article>

          {/* ── SIDEBAR ── */}
          <aside className="lg:w-80 flex-shrink-0 space-y-6">

            {/* About the Author */}
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
              {/* Decorative heading */}
              <div className="px-6 pt-6 pb-2 flex items-center gap-2">
                <span style={{ fontFamily: 'Georgia, serif', fontSize: 26, color: '#9ca3af', fontStyle: 'italic', lineHeight: 1 }}>about</span>
                <span className="font-poppins font-black text-white text-sm px-3 py-1 rounded" style={{ background: '#FF9933', letterSpacing: 2 }}>ME</span>
              </div>

              {/* Large circular photo */}
              <div className="flex justify-center pt-2 pb-4">
                <div className="relative">
                  <div className="w-36 h-36 rounded-full overflow-hidden border-4 border-white shadow-lg" style={{ outline: '2px solid #e5e7eb' }}>
                    {(blog.author_avatar || authorInfo?.avatar)
                      ? <img src={blog.author_avatar || authorInfo.avatar} alt={blog.author_name} className="w-full h-full object-cover"
                          onError={e => { e.target.style.display='none'; e.target.parentNode.innerHTML = `<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#1B3F8A,#2563eb);color:white;font-size:3rem;font-weight:900">${(blog.author_name||'A')[0].toUpperCase()}</div>` }} />
                      : <div className="w-full h-full flex items-center justify-center text-white font-black text-5xl" style={{ background: 'linear-gradient(135deg, #1B3F8A, #2563eb)' }}>
                          {(blog.author_name || 'A')[0].toUpperCase()}
                        </div>
                    }
                  </div>
                  {/* Decorative ring */}
                  <div className="absolute inset-0 rounded-full" style={{ border: '1.5px dashed #d1d5db', transform: 'scale(1.08)' }} />
                </div>
              </div>

              <div className="px-6 pb-6 text-center">
                <h4 className="font-poppins font-bold text-base mb-2" style={{ color: '#111827' }}>
                  Hey there! I am <span style={{ color: '#1B3F8A' }}>{blog.author_name || 'Anonymous'}.</span>
                </h4>
                <p className="text-gray-500 text-sm leading-relaxed">
                  {blog.author_bio || authorInfo?.bio || `Passionate about consumer awareness and ingredient transparency in India. Writing to help people make informed choices about food and cosmetics.`}
                </p>
                <div className="mt-4 pt-4 border-t border-gray-100">
                  <p className="text-xs text-gray-400 mb-2 font-semibold">My mission?</p>
                  <p className="text-xs text-gray-500 leading-relaxed mb-3">To help every Indian understand what they're eating and applying on their skin.</p>
                  <Link to="/blog/write"
                    className="inline-block text-xs font-bold py-2 px-5 rounded-xl text-white hover:opacity-90 transition-opacity"
                    style={{ background: '#FF9933' }}>
                    ✍️ Write your own blog
                  </Link>
                </div>
              </div>
            </div>

            {/* Related Posts */}
            {related.length > 0 && (
              <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-5">
                <div className="flex items-center gap-2 mb-4">
                  <div className="w-1 h-5 rounded" style={{ background: '#FF9933' }} />
                  <h4 className="font-poppins font-bold text-sm" style={{ color: '#1B3F8A' }}>Related Articles</h4>
                </div>
                <div className="space-y-4">
                  {related.map(r => (
                    <Link key={r.id} to={`/blog/${r.slug}`} className="flex gap-3 group">
                      <div className="w-16 h-16 rounded-xl overflow-hidden flex-shrink-0">
                        <img src={r.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&q=80'}
                          alt={r.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                          onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&q=80' }} />
                      </div>
                      <div className="flex-1">
                        <p className="text-xs font-bold leading-snug group-hover:text-orange-500 transition-colors line-clamp-2"
                          style={{ color: '#1B3F8A', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {r.title}
                        </p>
                        <p className="text-xs text-gray-400 mt-1">{r.author_name}</p>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* Check ingredient CTA */}
            <div className="rounded-2xl p-5 text-white text-center" style={{ background: 'linear-gradient(135deg, #1B3F8A, #2563eb)' }}>
              <div className="text-3xl mb-2">🔍</div>
              <h4 className="font-poppins font-bold text-base mb-2">Check Any Ingredient</h4>
              <p className="text-blue-200 text-xs mb-4 leading-relaxed">Find out if an ingredient in your product is safe, questionable, or banned.</p>
              <Link to="/check-ingredient"
                className="block text-sm font-bold py-2.5 px-5 rounded-xl hover:opacity-90 transition-opacity"
                style={{ background: '#FF9933' }}>
                Check Ingredient →
              </Link>
            </div>

          </aside>
        </div>
      </div>
    </div>
  )
}
