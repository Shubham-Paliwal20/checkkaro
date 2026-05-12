import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'

const CAT_COLORS = {
  'Food':           'bg-orange-100 text-orange-700',
  'Cosmetics':      'bg-pink-100 text-pink-700',
  'Health':         'bg-green-100 text-green-700',
  'Lifestyle':      'bg-blue-100 text-blue-700',
  'Product Review': 'bg-purple-100 text-purple-700',
}

export default function BlogPost() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [blog, setBlog]       = useState(null)
  const [related, setRelated] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchBlog()
  }, [slug])

  async function fetchBlog() {
    setLoading(true)
    const { data } = await supabase
      .from('blogs')
      .select('*')
      .eq('slug', slug)
      .eq('status', 'approved')
      .maybeSingle()
    setBlog(data)
    if (data?.category) {
      const { data: rel } = await supabase
        .from('blogs')
        .select('id, title, slug, author_name, created_at, cover_image')
        .eq('status', 'approved')
        .eq('category', data.category)
        .neq('slug', slug)
        .limit(3)
      setRelated(rel || [])
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
        <h2 className="font-poppins font-bold text-navy text-2xl mb-2">Blog not found</h2>
        <p className="text-gray-500 mb-6">This blog may have been removed or is pending approval.</p>
        <Link to="/blog" style={{ background: '#FF9933' }} className="text-white font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity">
          Back to Blogs
        </Link>
      </div>
    </div>
  )

  const paragraphs = blog.content.split('\n').filter(p => p.trim())
  const readTime = Math.max(1, Math.ceil(blog.content.split(/\s+/).length / 200))

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Cover */}
      {blog.cover_image && (
        <div className="w-full h-64 sm:h-80 overflow-hidden">
          <img src={blog.cover_image} alt={blog.title} className="w-full h-full object-cover" />
        </div>
      )}

      {/* Header */}
      <div style={{ background: blog.cover_image ? 'transparent' : 'linear-gradient(135deg, #1B3F8A 0%, #2d5bc7 100%)' }}
        className={blog.cover_image ? 'px-4 pt-8' : 'py-12 px-4 text-white'}>
        <div className="max-w-3xl mx-auto">
          <button onClick={() => navigate('/blog')}
            className={`flex items-center gap-2 text-sm mb-4 transition-colors ${blog.cover_image ? 'text-gray-500 hover:text-navy' : 'text-blue-200 hover:text-white'}`}>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            All Blogs
          </button>
          {blog.category && (
            <span className={`inline-block text-xs font-semibold px-3 py-1 rounded-full mb-3 ${CAT_COLORS[blog.category] || 'bg-gray-100 text-gray-600'}`}>
              {blog.category}
            </span>
          )}
          <h1 className={`font-poppins font-bold text-2xl sm:text-4xl leading-snug mb-4 ${blog.cover_image ? 'text-navy' : 'text-white'}`}>
            {blog.title}
          </h1>
          <div className={`flex items-center gap-4 text-sm ${blog.cover_image ? 'text-gray-500' : 'text-blue-200'}`}>
            <span className="font-medium">✍ {blog.author_name || 'Anonymous'}</span>
            <span>·</span>
            <span>{new Date(blog.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' })}</span>
            <span>·</span>
            <span>{readTime} min read</span>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-3xl mx-auto px-4 py-10">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 sm:p-10">
          <div className="prose prose-gray max-w-none">
            {paragraphs.map((para, i) => (
              <p key={i} className="text-gray-700 leading-relaxed text-base mb-5">{para}</p>
            ))}
          </div>
        </div>

        {/* Related blogs */}
        {related.length > 0 && (
          <div className="mt-12">
            <h3 className="font-poppins font-bold text-navy text-xl mb-6">More in {blog.category}</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {related.map(r => (
                <Link key={r.id} to={`/blog/${r.slug}`}
                  className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow p-4 group">
                  {r.cover_image && (
                    <img src={r.cover_image} alt={r.title} className="w-full h-28 object-cover rounded-lg mb-3" />
                  )}
                  <h4 className="font-semibold text-navy text-sm leading-snug group-hover:text-orange-500 transition-colors line-clamp-2"
                    style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                    {r.title}
                  </h4>
                  <p className="text-xs text-gray-400 mt-2">by {r.author_name || 'Anonymous'}</p>
                </Link>
              ))}
            </div>
          </div>
        )}

        {/* Write CTA */}
        <div className="mt-12 rounded-2xl p-8 text-center" style={{ background: 'linear-gradient(135deg, #1B3F8A 0%, #2d5bc7 100%)' }}>
          <h3 className="font-poppins font-bold text-white text-xl mb-2">Have something to share?</h3>
          <p className="text-blue-200 text-sm mb-5">Write your own blog and help people make informed choices.</p>
          <Link to="/blog/write" style={{ background: '#FF9933' }}
            className="inline-block text-white font-bold px-8 py-3 rounded-xl hover:opacity-90 transition-opacity">
            ✍️ Write a Blog
          </Link>
        </div>
      </div>
    </div>
  )
}
