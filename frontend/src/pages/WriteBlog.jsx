import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const CATEGORIES = ['Food', 'Cosmetics', 'Health', 'Lifestyle', 'Product Review']

function slugify(text) {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '') + '-' + Date.now()
}

export default function WriteBlog() {
  const { user, openAuthModal } = useAuth()
  const navigate = useNavigate()

  const [title,       setTitle]       = useState('')
  const [category,   setCategory]   = useState('Food')
  const [content,    setContent]    = useState('')
  const [coverUrl,   setCoverUrl]   = useState('')
  const [authorName, setAuthorName] = useState('')
  const [authorBio,  setAuthorBio]  = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error,      setError]      = useState('')
  const [submitted,  setSubmitted]  = useState(false)

  useEffect(() => {
    if (!user) { openAuthModal(); navigate('/blog') }
    if (user?.email) setAuthorName(user.email.split('@')[0])
  }, [user])

  const wordCount = content.trim().split(/\s+/).filter(Boolean).length

  async function handleSubmit() {
    if (!title.trim())   { setError('Please add a title.'); return }
    if (title.trim().length > 120) { setError('Title too long (max 120 characters).'); return }
    if (content.trim().split(/\s+/).length < 50) { setError('Blog must be at least 50 words.'); return }
    if (content.trim().length > 50000) { setError('Blog too long (max 50,000 characters).'); return }
    setSubmitting(true); setError('')
    const excerpt = content.trim().slice(0, 200).replace(/\n/g, ' ') + '...'
    const { error: e } = await supabase.from('blogs').insert({
      title:       title.trim(),
      slug:        slugify(title.trim()),
      content:     content.trim(),
      excerpt,
      category,
      cover_image: coverUrl.trim() || null,
      author_id:   user.id,
      author_name: authorName.trim() || user.email.split('@')[0],
      author_bio:  authorBio.trim() || null,
      status:      'pending',
    })
    setSubmitting(false)
    if (e) { setError(e.message); return }
    setSubmitted(true)
  }

  if (submitted) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl shadow-sm p-10 max-w-md w-full text-center">
        <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg className="w-10 h-10 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="font-poppins font-bold text-2xl text-navy mb-3">Blog Submitted!</h2>
        <p className="text-gray-500 mb-6">Your blog is under review. Once approved by the admin it will be published on Parkho.</p>
        <button onClick={() => navigate('/blog')}
          style={{ background: '#FF9933' }}
          className="text-white font-bold px-8 py-3 rounded-xl w-full hover:opacity-90 transition-opacity">
          Back to Blogs
        </button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50">

      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, #1B3F8A 0%, #2d5bc7 100%)' }} className="py-10 px-4 text-white">
        <div className="max-w-3xl mx-auto">
          <button onClick={() => navigate('/blog')} className="flex items-center gap-2 text-blue-200 hover:text-white text-sm mb-4 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Blogs
          </button>
          <h1 className="font-poppins font-bold text-3xl mb-1">Write a Blog</h1>
          <p className="text-blue-200 text-sm">Share your knowledge about food, cosmetics, and healthy living.</p>
        </div>
      </div>

      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">

          {/* Guidelines */}
          <div className="bg-orange-50 border-b border-orange-100 px-6 py-4">
            <p className="text-sm text-orange-700 font-medium">📋 Guidelines: Write original content (min 50 words). No promotions or spam. Blogs are reviewed by admin before publishing.</p>
          </div>

          <div className="p-6 space-y-6">

            {/* Title */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Blog Title *</label>
              <input
                value={title} onChange={e => setTitle(e.target.value)}
                placeholder="E.g. Why I stopped using products with Sodium Lauryl Sulfate"
                maxLength={120}
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all"
              />
              <p className="text-xs text-gray-400 mt-1 text-right">{title.length}/120</p>
            </div>

            {/* Category + Author row */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Category *</label>
                <select value={category} onChange={e => setCategory(e.target.value)}
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all bg-white">
                  {CATEGORIES.map(c => <option key={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Your Name</label>
                <input value={authorName} onChange={e => setAuthorName(e.target.value)}
                  placeholder="Display name"
                  className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all"
                />
              </div>
            </div>

            {/* Author bio + avatar */}
            <div className="bg-orange-50 rounded-xl p-4 border border-orange-100">
              <p className="text-xs font-bold text-orange-700 mb-3 uppercase tracking-wide">👤 Your Profile (shown on blog sidebar)</p>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">Your Photo URL <span className="text-gray-400 font-normal">(optional)</span></label>
                  <input value={authorAvatar} onChange={e => setAuthorAvatar(e.target.value)}
                    placeholder="https://example.com/your-photo.jpg"
                    className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all bg-white"
                  />
                  {authorAvatar && (
                    <div className="mt-2 flex items-center gap-3">
                      <img src={authorAvatar} alt="preview" onError={e => e.target.style.display='none'}
                        className="w-14 h-14 rounded-full object-cover border-2 border-orange-200" />
                      <span className="text-xs text-gray-400">This will appear on your blog's sidebar</span>
                    </div>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1.5">About You <span className="text-gray-400 font-normal">(optional)</span></label>
                  <textarea value={authorBio} onChange={e => setAuthorBio(e.target.value)}
                    placeholder="E.g. Nutritionist based in Delhi. Passionate about helping people understand what they eat."
                    rows={2} maxLength={250}
                    className="w-full border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all resize-none bg-white"
                  />
                  <p className="text-xs text-gray-400 text-right mt-1">{authorBio.length}/250</p>
                </div>
              </div>
            </div>

            {/* Cover image */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Cover Image URL <span className="text-gray-400 font-normal">(optional)</span></label>
              <input value={coverUrl} onChange={e => setCoverUrl(e.target.value)}
                placeholder="https://example.com/image.jpg"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all"
              />
              {coverUrl && (
                <img src={coverUrl} alt="preview" onError={e => e.target.style.display='none'}
                  className="mt-2 rounded-xl h-32 w-full object-cover border border-gray-200" />
              )}
            </div>

            {/* Content */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Blog Content *</label>
              <textarea
                value={content} onChange={e => setContent(e.target.value)}
                placeholder="Start writing your blog here... Share what you know about ingredients, products, or healthy habits. Be honest, be helpful."
                rows={16}
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-orange-400 focus:ring-2 focus:ring-orange-100 transition-all resize-none leading-relaxed"
              />
              <div className="flex justify-between text-xs mt-1">
                <span className={wordCount < 50 ? 'text-red-400' : 'text-green-500'}>
                  {wordCount} words {wordCount < 50 ? `(${50 - wordCount} more needed)` : '✓'}
                </span>
                <span className="text-gray-400">{content.length} characters</span>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3 text-sm text-red-600">
                {error}
              </div>
            )}

            {/* Submit */}
            <button onClick={handleSubmit} disabled={submitting}
              style={{ background: submitting ? '#ccc' : '#FF9933' }}
              className="w-full text-white font-bold py-4 rounded-xl text-base hover:opacity-90 transition-opacity disabled:cursor-not-allowed">
              {submitting ? 'Submitting...' : '🚀 Submit for Review'}
            </button>

            <p className="text-center text-xs text-gray-400">
              Your blog will be reviewed by our team. We'll publish it if it meets our community guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
