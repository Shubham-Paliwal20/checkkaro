import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabaseClient'
import { useAuth } from '../context/AuthContext'

const CATEGORIES = ['All', 'Food', 'Cosmetics', 'Health', 'Lifestyle', 'Product Review']

const CAT_COLORS = {
  'Food':           { bg: '#fff7ed', text: '#ea580c', dot: '#f97316' },
  'Cosmetics':      { bg: '#fdf2f8', text: '#be185d', dot: '#ec4899' },
  'Health':         { bg: '#f0fdf4', text: '#15803d', dot: '#22c55e' },
  'Lifestyle':      { bg: '#eff6ff', text: '#1d4ed8', dot: '#3b82f6' },
  'Product Review': { bg: '#faf5ff', text: '#7e22ce', dot: '#a855f7' },
}

export const STATIC_BLOGS = [
  {
    id: 'static-1',
    slug: 'static-1',
    title: 'Why You Should Read Food Labels Before Buying Packaged Snacks in India',
    excerpt: 'Most Indians never read the ingredient list on packaged food. Here\'s what you\'re missing — and why it matters for your family\'s health.',
    content: `Most Indians pick up a packet of chips or biscuits without a second glance at the ingredient list. But what if that list told a very different story than the attractive packaging?

India's packaged food industry is booming. With over 40,000 food products on shelves, we're eating more processed food than ever before. And yet, most of us have no idea what's actually inside these products.

**What to look for on a food label**

The first thing to understand is that ingredients are listed in descending order of quantity. So if sugar is the first ingredient in your "health" cereal — it's mostly sugar.

Common red flags to watch out for:
- **Partially hydrogenated oils**: A source of trans fats, linked to heart disease
- **High Fructose Corn Syrup (HFCS)**: Added sugar that's metabolised differently by your body
- **Artificial colours like Tartrazine (E102)**: Linked to hyperactivity in children
- **Sodium nitrite**: Used in processed meats, a known carcinogen at high levels
- **MSG**: While generally safe for most, causes reactions in sensitive individuals

**The "natural flavours" trick**

Brands love to use the phrase "natural flavours" — but this can mean almost anything. Natural strawberry flavour, for example, can legally be derived from wood shavings treated with chemicals. It doesn't have to come from actual strawberries.

**What FSSAI requires**

The Food Safety and Standards Authority of India (FSSAI) mandates that all packaged foods display:
- Complete ingredient list
- Nutritional information per 100g
- Any allergens in bold
- Manufacturing and expiry date
- Vegetarian/non-vegetarian symbol

**Start small**

You don't need to become an expert overnight. Start by checking the first three ingredients on your next grocery run. If you can't pronounce them or don't know what they are — that's a sign to look them up on Parkho before buying.

Knowledge is your best defence against misleading marketing. The next time a brand claims "no added sugar" or "made with real fruits" — check the label. The truth is always there.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800&q=80',
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-2',
    slug: 'static-2',
    title: 'Parabens in Indian Skincare: Should You Really Be Worried?',
    excerpt: 'Parabens are in almost every moisturiser, shampoo, and cream on the market. But are they actually dangerous? Here\'s what the science says.',
    content: `Walk into any pharmacy or beauty store in India and pick up a moisturiser. Flip it over. Chances are high you'll find methylparaben, propylparaben, or butylparaben somewhere in the ingredient list.

Parabens are preservatives. They've been used in cosmetics since the 1950s to prevent bacteria and mould from growing in your lotions and creams. Without them, your moisturiser could become a petri dish within weeks.

**Why people are worried**

The alarm bells started in 2004 when a UK study found traces of parabens in breast tumour tissue. Headlines screamed that parabens cause cancer. Social media ran with it. "Paraben-free" became the hottest marketing claim in beauty.

But here's what that study actually showed: parabens were present in the tissue. It did NOT show that parabens caused the cancer, or that they wouldn't have been present in healthy tissue too. Correlation is not causation.

**What regulators say**

The European Scientific Committee on Consumer Safety (SCCS) reviewed the evidence extensively. Their conclusion:
- Methylparaben and ethylparaben are safe at current use levels
- Propylparaben and butylparaben: safe below 0.19% concentration
- Isopropylparaben and isobutylparaben: insufficient safety data, best avoided

FSSAI in India follows similar guidelines. Most products use parabens at concentrations of 0.01–0.3%, well within safe limits.

**Who should be careful**

If you have sensitive skin or hormone-related conditions, you may want to limit paraben exposure as a precaution — not because the science is conclusive, but because the precautionary principle makes sense.

Pregnant women and parents of young children may also prefer to choose paraben-free options, especially for products applied to large areas of skin regularly.

**The bottom line**

Parabens at typical cosmetic concentrations are not proven to cause harm in healthy adults. The "paraben-free" marketing trend has outpaced the actual scientific concern. However, if you prefer to avoid them — plenty of alternatives like phenoxyethanol exist, each with their own profile worth checking.

Use Parkho to check any ingredient you're unsure about. Knowledge beats both blind trust and unnecessary panic.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800&q=80',
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-3',
    slug: 'static-3',
    title: 'Hidden Sugar in "Healthy" Indian Foods — What Brands Don\'t Tell You',
    excerpt: 'Oats, granola, fruit juice, multigrain bread — they all sound healthy. But the sugar content might shock you.',
    content: `India has one of the highest rates of diabetes in the world — over 100 million diabetics and counting. Yet somehow, we're eating more "health foods" than ever. Something doesn't add up.

The problem isn't just mithai and soft drinks. The hidden sugar problem runs through foods we consider healthy.

**The usual suspects**

*Packaged fruit juices*: A 200ml tetra pack of "100% fruit juice" can contain 20–25 grams of sugar. That's more sugar than a can of cola per 200ml. The fibre that slows sugar absorption in whole fruit is gone. What remains is essentially sugar water with vitamins.

*Flavoured yoghurt*: Plain dahi is one of the healthiest foods you can eat. Flavoured yoghurt brands add 15–25g of sugar per 100g serving. Check the label — sugar is often the second ingredient.

*Multigrain bread*: The word "multigrain" just means multiple grains. It doesn't mean whole grain, low-GI, or low-sugar. Many multigrain breads in India contain added sugar and refined flour as the primary ingredient.

*Breakfast cereals*: Some popular cereals marketed to children contain over 30% sugar by weight. They're cereal-flavoured candy, essentially.

*Granola and muesli*: Brands like to show photos of nuts and oats. But check the label — honey, glucose syrup, and brown sugar can make these calorie and sugar bombs.

**How sugar hides in ingredient lists**

Manufacturers use many names for sugar to make it less obvious:
- Dextrose, fructose, sucrose, maltose
- Corn syrup, glucose syrup, high fructose corn syrup
- Fruit juice concentrate
- Cane juice, coconut sugar, jaggery
- Maltodextrin (acts like sugar in the body)

**What to do**

Look at the nutritional information, not just the ingredients. Check "Total Sugars" per 100g. As a rule of thumb:
- Under 5g per 100g = low sugar
- 5–15g per 100g = moderate
- Over 15g per 100g = high sugar

Real healthy eating in India doesn't need to be complicated. Dal, sabzi, roti, curd, fruits — traditional Indian food is naturally low in added sugar. The health food industry has simply repackaged junk food with better marketing.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=800&q=80',
    created_at: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-4',
    slug: 'static-4',
    title: '5 Harmful Ingredients Hiding in Your Daily Face Cream',
    excerpt: 'Your moisturiser may be doing more harm than good. These five ingredients are worth avoiding — especially in products you use every day.',
    content: `We put moisturiser on our face every single day. Which makes the ingredients in it especially important — because daily exposure to even small amounts of harmful chemicals adds up over time.

Here are five ingredients to watch for in your face cream.

**1. Sodium Lauryl Sulphate (SLS)**

SLS is a detergent that creates foam and lather. It's cheap, effective at cleaning, and harsh. In face creams, it can strip your skin's natural moisture barrier, cause irritation, and worsen conditions like rosacea and eczema. It's more commonly found in face washes than creams, but check anyway.

**2. Synthetic Fragrances (Parfum)**

"Parfum" or "Fragrance" on an ingredient list is a legal black box. A single fragrance ingredient can contain up to 200 individual chemicals — and manufacturers don't have to disclose them. Synthetic fragrances are the number one cause of cosmetic allergic reactions.

If your face cream has a pleasant scent but "fragrance" is the source — consider switching to a fragrance-free option, especially if you have sensitive skin.

**3. Mineral Oil (Paraffinum Liquidum)**

Derived from petroleum, mineral oil is cheap and used as a moisturising agent in many budget face creams. The problem: it forms an occlusive layer on skin that traps moisture but also clogs pores. For oily or acne-prone skin, this can be problematic. For dry, non-acne-prone skin, it's generally harmless.

**4. Oxybenzone (in SPF moisturisers)**

If your daily moisturiser has SPF, check if oxybenzone is listed. This chemical UV filter has been detected in human blood, urine, and breast milk after topical application. The FDA has flagged it as needing more safety data. Mineral sunscreens with zinc oxide or titanium dioxide are safer alternatives.

**5. Formaldehyde-releasing preservatives**

DMDM Hydantoin, Imidazolidinyl Urea, Diazolidinyl Urea, and Quaternium-15 all release small amounts of formaldehyde over time. Formaldehyde is a known carcinogen and allergen. These preservatives are still legal and widely used in India. Check your face cream's ingredient list carefully.

**What to do**

You don't need to throw away everything you own. Start by checking the products you use on your face daily — the ones with the most contact time and largest application area. Use Parkho to check any ingredient you're unsure about.

Switching to cleaner formulations doesn't have to be expensive. Many affordable Indian brands now offer products without these ingredients.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=800&q=80',
    created_at: new Date(Date.now() - 8 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-5',
    slug: 'static-5',
    title: 'E-Numbers in Indian Food: Which Are Safe and Which to Avoid',
    excerpt: 'E-numbers are everywhere in packaged food. But not all of them are harmful. Here\'s a simple guide to understanding what they mean.',
    content: `You've seen them on every packet of processed food: E102, E211, E621. These codes look technical and mysterious. But they're just a standardised numbering system for food additives approved for use in food production.

Not all E-numbers are harmful. Many are derived from natural sources. Here's how to make sense of them.

**How E-numbers are categorised**

- E100–E199: Colours
- E200–E299: Preservatives
- E300–E399: Antioxidants
- E400–E499: Thickeners, stabilisers, emulsifiers
- E500–E599: Acidity regulators
- E600–E699: Flavour enhancers
- E900+: Sweeteners, glazing agents, others

**Commonly used and generally safe**

*E300 (Vitamin C / Ascorbic acid)*: An antioxidant derived from vitamin C. Completely safe. Used to prevent oxidation and preserve colour.

*E322 (Lecithin)*: Usually derived from soy or sunflower. An emulsifier found in chocolate. Generally safe and occurs naturally in eggs.

*E330 (Citric acid)*: Found naturally in citrus fruits. Used as a preservative and flavour enhancer. Very safe.

*E440 (Pectin)*: Derived from fruit peels. Used as a gelling agent in jams. Completely natural and safe.

**Ones to be cautious about**

*E102 (Tartrazine)*: A synthetic yellow dye. Linked to hyperactivity in children in some studies. Banned in Norway and Austria. Used widely in Indian snacks, drinks, and confectionery.

*E110 (Sunset Yellow)*: Another synthetic dye. Associated with allergic reactions, particularly in people sensitive to aspirin.

*E211 (Sodium Benzoate)*: A preservative. When combined with Vitamin C (E300) in acidic drinks, it can form benzene — a known carcinogen. Commonly found in soft drinks and pickles.

*E621 (MSG / Monosodium Glutamate)*: A flavour enhancer. Generally considered safe by regulatory bodies, but some people report sensitivity symptoms. Used heavily in Chinese food and instant noodles.

*E951 (Aspartame)*: An artificial sweetener. Safe for most people but should be avoided by those with phenylketonuria (PKU). There's ongoing debate about long-term effects at high doses.

**The simple rule**

Numbers in the 100s (colours) and 200s (preservatives) deserve the most scrutiny. Numbers in the 300s and 400s are usually harmless or naturally derived.

When in doubt, use Parkho to check any E-number before buying.`,
    category: 'Food',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=800&q=80',
    created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
  {
    id: 'static-6',
    slug: 'static-6',
    title: 'How to Read a Cosmetic Ingredient List Like an Expert',
    excerpt: 'INCI names look intimidating. But once you know the basics, you\'ll never look at a skincare product the same way again.',
    content: `Aqua. Glycerin. Niacinamide. Cetearyl Alcohol. If you've tried reading the back of a moisturiser and given up — you're not alone. Cosmetic ingredient lists (written in INCI format) look like a chemistry textbook.

But here's the secret: you only need to understand a few basics to become a smarter cosmetics consumer.

**What is INCI?**

INCI stands for International Nomenclature of Cosmetic Ingredients. It's a standardised system used globally to name cosmetic ingredients. The same ingredient will have the same INCI name on a product sold in India, Europe, or the US — making it easier to research and compare.

**Rule 1: Order matters**

Ingredients are listed in descending order by concentration. The first ingredient is present in the highest amount. Usually the first 1–5 ingredients make up 80–90% of the product.

If water (Aqua) is first — it's mostly water. If a "vitamin C serum" lists sodium ascorbyl phosphate 10th — there's very little actual vitamin C in it.

**Rule 2: The 1% threshold**

After a certain point in the list (usually around the 10th–15th ingredient), concentrations drop below 1%. Ingredients after this point can be listed in any order. This is where you'll often find preservatives, fragrances, and actives present in tiny amounts.

**Key ingredient categories to know**

*Humectants* (attract moisture): Glycerin, Hyaluronic Acid, Sodium PCA
*Emollients* (soften skin): Squalane, Jojoba Oil, Cetearyl Alcohol
*Occlusives* (seal in moisture): Petrolatum, Dimethicone, Beeswax
*Actives* (target skin concerns): Niacinamide, Retinol, Salicylic Acid, AHA/BHA
*Preservatives*: Phenoxyethanol, Parabens, DMDM Hydantoin
*Emulsifiers* (keep oil and water mixed): Polysorbate 20, Ceteareth-20

**Words that are just water**

"Aqua," "Eau," "Water" — all the same thing. Some fancy brands write it as "Alpine Spring Water" or "Thermal Water" — it's still water. Don't pay a premium for it.

**Red flags in ingredient lists**

- Alcohol Denat high up the list (drying, irritating)
- "Fragrance" or "Parfum" with no further detail
- Many silicones in anti-ageing products (they fill wrinkles temporarily but do nothing long-term)
- "Collagen" in a topical cream (too large to penetrate skin — it just sits on top)

**Your cheat sheet**

Next time you pick up a skincare product:
1. Check the first 5 ingredients — what's the base?
2. Look for your target active — where does it appear in the list?
3. Check for fragrance and known irritants
4. Use Parkho to look up anything unfamiliar

It takes 2 minutes and could save you from spending ₹2,000 on a product that doesn't do what it claims.`,
    category: 'Cosmetics',
    author_name: 'Parkho Editorial',
    cover_image: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800&q=80',
    created_at: new Date(Date.now() - 12 * 24 * 60 * 60 * 1000).toISOString(),
    status: 'approved',
    isStatic: true,
  },
]

function timeAgo(dateStr) {
  const diff = Date.now() - new Date(dateStr).getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return 'Today'
  if (days === 1) return 'Yesterday'
  if (days < 30) return `${days} days ago`
  return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

function CatBadge({ cat }) {
  const c = CAT_COLORS[cat] || { bg: '#f3f4f6', text: '#374151', dot: '#9ca3af' }
  return (
    <span style={{ background: c.bg, color: c.text }} className="text-xs font-bold px-3 py-1 rounded-full">
      {cat}
    </span>
  )
}

export default function Blog() {
  const [dbBlogs, setDbBlogs]   = useState([])
  const [category, setCategory] = useState('All')
  const { user, openAuthModal } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    // Load DB blogs in background — static blogs show immediately
    supabase.from('blogs').select('id,title,slug,excerpt,category,author_name,cover_image,created_at')
      .eq('status', 'approved').order('created_at', { ascending: false })
      .then(({ data }) => { if (data && data.length > 0) setDbBlogs(data) })
      .catch(() => {})
  }, [])

  const allBlogs = [...dbBlogs, ...STATIC_BLOGS]
  const filtered = category === 'All' ? allBlogs : allBlogs.filter(b => b.category === category)
  const featured = filtered[0]
  const sideBlogs = filtered.slice(1, 4)
  const gridBlogs = filtered.slice(4)

  return (
    <div className="min-h-screen bg-gray-50">

      {/* ── HERO BANNER ── */}
      <div className="relative overflow-hidden" style={{ minHeight: 320 }}>
        {/* Background image */}
        <img
          src="https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=1600&q=80"
          alt="blog hero"
          className="absolute inset-0 w-full h-full object-cover"
          onError={e => { e.target.onerror=null; e.target.style.display='none' }}
        />
        {/* Dark overlay */}
        <div className="absolute inset-0" style={{ background: 'linear-gradient(to bottom, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0.7) 100%)' }} />

        <div className="relative max-w-6xl mx-auto px-4 py-16 text-center">
          <div className="inline-flex items-center gap-2 bg-white/20 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 text-white text-xs font-semibold mb-5 tracking-widest uppercase">
            <span style={{ color: '#FF9933' }}>●</span> Community Knowledge Hub
          </div>
          <h1 className="font-poppins font-black text-white mb-2" style={{ fontSize: 'clamp(32px, 6vw, 58px)', letterSpacing: '-1px', textShadow: '0 2px 20px rgba(0,0,0,0.4)' }}>
            Parkho <span style={{ color: '#FF9933' }}>Blog</span>
          </h1>
          <p className="text-white/70 text-sm sm:text-base mb-1 font-semibold tracking-widest uppercase">Food · Cosmetics · Health · Lifestyle</p>
          <p className="text-white/60 text-sm max-w-lg mx-auto mt-3 leading-relaxed">
            Real insights from real people. Know what's in your products, understand ingredients, and make better choices.
          </p>
          <button
            onClick={() => user ? navigate('/blog/write') : openAuthModal()}
            className="mt-7 inline-flex items-center gap-2 text-white font-bold px-8 py-3.5 rounded-xl text-sm hover:opacity-90 transition-all shadow-xl"
            style={{ background: '#FF9933', boxShadow: '0 4px 20px rgba(255,153,51,0.4)' }}>
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
            Write a Blog
          </button>
        </div>

        {/* Wave */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 50" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" style={{ display: 'block', width: '100%', height: 50 }}>
            <path d="M0 50L360 20L720 40L1080 15L1440 30V50H0Z" fill="#f9fafb"/>
          </svg>
        </div>
      </div>

      {/* ── CATEGORY FILTER ── */}
      <div className="max-w-6xl mx-auto px-4 pt-8 pb-2">
        <div className="flex gap-2 flex-wrap">
          {CATEGORIES.map(cat => (
            <button key={cat} onClick={() => setCategory(cat)}
              className="px-4 py-1.5 rounded-full text-sm font-semibold transition-all border"
              style={category === cat
                ? { background: '#1B3F8A', color: '#fff', borderColor: '#1B3F8A' }
                : { background: '#fff', color: '#6b7280', borderColor: '#e5e7eb' }}>
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* ── MAIN CONTENT ── */}
      <div className="max-w-6xl mx-auto px-4 py-8">

        {filtered.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-5xl mb-4">📝</div>
            <h3 className="font-poppins font-bold text-navy text-xl mb-2">No blogs in this category yet</h3>
            <button onClick={() => user ? navigate('/blog/write') : openAuthModal()}
              style={{ background: '#FF9933' }}
              className="mt-4 text-white font-bold px-6 py-2.5 rounded-xl hover:opacity-90 transition-opacity">
              Write First Blog
            </button>
          </div>
        ) : (
          <>
            {/* ── FEATURED + SIDEBAR LAYOUT ── */}
            {featured && (
              <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-10">

                {/* Featured (large left) */}
                <Link to={`/blog/${featured.slug}`}
                  className="lg:col-span-3 relative rounded-2xl overflow-hidden group shadow-md"
                  style={{ minHeight: 420 }}>
                  <img
                    src={featured.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80'}
                    alt={featured.title}
                    className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                    onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&q=80' }}
                  />
                  <div className="absolute inset-0" style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.05) 100%)' }} />
                  <div className="absolute inset-0 flex flex-col justify-end p-6 sm:p-8">
                    <CatBadge cat={featured.category} />
                    <h2 className="font-poppins font-black text-white text-xl sm:text-2xl leading-snug mt-3 mb-3 group-hover:text-orange-300 transition-colors">
                      {featured.title}
                    </h2>
                    <p className="text-gray-300 text-sm leading-relaxed mb-4 line-clamp-2"
                      style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                      {featured.excerpt}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="text-gray-400 text-xs">
                        ✍ <span className="text-white font-medium">{featured.author_name}</span> · {timeAgo(featured.created_at)}
                      </div>
                      <span className="inline-flex items-center gap-1.5 bg-white/20 backdrop-blur text-white text-xs font-bold px-4 py-2 rounded-xl hover:bg-orange-500 transition-colors">
                        READ MORE →
                      </span>
                    </div>
                  </div>
                </Link>

                {/* Sidebar (right) */}
                <div className="lg:col-span-2 flex flex-col gap-4">
                  {sideBlogs.map(blog => (
                    <Link key={blog.id} to={`/blog/${blog.slug}`}
                      className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group border border-gray-100 flex gap-0">
                      <div className="w-32 sm:w-36 flex-shrink-0 overflow-hidden">
                        <img
                          src={blog.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80'}
                          alt={blog.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          style={{ minHeight: 110 }}
                          onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&q=80' }}
                        />
                      </div>
                      <div className="p-3 sm:p-4 flex flex-col justify-between flex-1">
                        <div>
                          <CatBadge cat={blog.category} />
                          <h3 className="font-poppins font-bold text-navy text-sm leading-snug mt-2 group-hover:text-orange-500 transition-colors"
                            style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                            {blog.title}
                          </h3>
                        </div>
                        <div className="text-xs text-gray-400 mt-2">
                          {blog.author_name} · {timeAgo(blog.created_at)}
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>
            )}

            {/* ── GRID: remaining blogs ── */}
            {gridBlogs.length > 0 && (
              <>
                <div className="flex items-center gap-3 mb-6">
                  <div className="h-px flex-1 bg-gray-200" />
                  <span className="text-xs font-bold text-gray-400 tracking-widest uppercase">More Articles</span>
                  <div className="h-px flex-1 bg-gray-200" />
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {gridBlogs.map(blog => (
                    <Link key={blog.id} to={`/blog/${blog.slug}`}
                      className="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow group border border-gray-100">
                      <div className="h-44 overflow-hidden relative">
                        <img
                          src={blog.cover_image || 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80'}
                          alt={blog.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                          onError={e => { e.target.onerror=null; e.target.src='https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=600&q=80' }}
                        />
                        <div className="absolute top-3 left-3">
                          <CatBadge cat={blog.category} />
                        </div>
                      </div>
                      <div className="p-5">
                        <h3 className="font-poppins font-bold text-navy text-base leading-snug mb-2 group-hover:text-orange-500 transition-colors"
                          style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {blog.title}
                        </h3>
                        <p className="text-gray-500 text-sm leading-relaxed"
                          style={{ display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                          {blog.excerpt}
                        </p>
                        <div className="flex items-center justify-between text-xs text-gray-400 mt-4 pt-3 border-t border-gray-100">
                          <span className="font-medium text-gray-600">✍ {blog.author_name}</span>
                          <span>{timeAgo(blog.created_at)}</span>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              </>
            )}
          </>
        )}

        {/* ── WRITE CTA BANNER ── */}
        <div className="mt-14 rounded-2xl overflow-hidden border border-gray-100 shadow-sm bg-white">
          <div className="flex flex-col sm:flex-row items-center gap-0">
            {/* Left image strip */}
            <div className="w-full sm:w-48 h-32 sm:h-auto flex-shrink-0 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1455390582262-044cdead277a?w=400&q=80"
                alt="write" className="w-full h-full object-cover" style={{ minHeight: 140 }}
                onError={e => { e.target.onerror=null; e.target.style.display='none' }} />
            </div>
            {/* Content */}
            <div className="flex-1 flex flex-col sm:flex-row items-center justify-between gap-6 p-7 sm:p-8">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-7 h-0.5 rounded" style={{ background: '#FF9933' }} />
                  <span className="text-xs font-bold tracking-widest uppercase" style={{ color: '#FF9933' }}>Share Your Knowledge</span>
                </div>
                <h3 className="font-poppins font-black text-2xl mb-1" style={{ color: '#1B3F8A' }}>Have something to share?</h3>
                <p className="text-gray-500 text-sm">Write about ingredients, products, or your health journey. Help others make better choices.</p>
              </div>
              <button onClick={() => user ? navigate('/blog/write') : openAuthModal()}
                style={{ background: '#1B3F8A', whiteSpace: 'nowrap' }}
                className="text-white font-bold px-8 py-3.5 rounded-xl hover:opacity-90 transition-opacity shadow-md text-sm flex-shrink-0">
                ✍️ Write a Blog
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
