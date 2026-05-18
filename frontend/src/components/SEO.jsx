import { Helmet } from 'react-helmet-async'

const SITE_NAME = 'Parkho'
const SITE_URL = 'https://parkho.in'
const DEFAULT_OG_IMAGE = `${SITE_URL}/og-image.png`
const DEFAULT_TITLE = 'Parkho — Check Ingredients in Indian Food & Cosmetic Products'
const DEFAULT_DESC = 'Check ingredients in any Indian food or cosmetic product. Get a simple breakdown of what\'s safe, questionable, or harmful — based on FSSAI, WHO & peer-reviewed research.'

export default function SEO({
  title,
  description = DEFAULT_DESC,
  keywords = '',
  canonical,
  ogImage = DEFAULT_OG_IMAGE,
  ogType = 'website',
  noIndex = false,
  structuredData = null,
}) {
  const fullTitle = title ? `${title} | ${SITE_NAME}` : DEFAULT_TITLE
  const canonicalUrl = canonical ? `${SITE_URL}${canonical}` : SITE_URL
  const schemas = structuredData ? (Array.isArray(structuredData) ? structuredData : [structuredData]) : []

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      {keywords && <meta name="keywords" content={keywords} />}
      <link rel="canonical" href={canonicalUrl} />
      {noIndex && <meta name="robots" content="noindex,nofollow" />}

      {/* Open Graph */}
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:url" content={canonicalUrl} />
      <meta property="og:type" content={ogType} />
      <meta property="og:site_name" content={SITE_NAME} />
      <meta property="og:locale" content="en_IN" />

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />

      {/* Structured Data — supports single object or array of schemas */}
      {schemas.map((sd, i) => (
        <script key={i} type="application/ld+json">{JSON.stringify(sd)}</script>
      ))}
    </Helmet>
  )
}
