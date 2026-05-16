import { motion } from 'framer-motion'
import DisclaimerBox from '../components/DisclaimerBox'
import SEO from '../components/SEO'

function About() {
  return (
    <>
      <SEO
        title="About Parkho — Empowering Indian Consumers"
        description="Parkho helps Indian consumers understand food and cosmetic product ingredients with FSSAI regulatory data — explained simply, no jargon, no confusion."
        keywords="about Parkho, ingredient awareness India, FSSAI information, food transparency India, consumer awareness app India"
        canonical="/about"
      />
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft"
    >
      {/* Hero */}
      <section className="text-white py-14 sm:py-20 px-4 text-center"
        style={{ background: 'linear-gradient(135deg, #1B3F8A 0%, #2d5bc7 100%)' }}>
        <div className="max-w-3xl mx-auto">
          <h1 className="font-poppins font-bold text-3xl sm:text-4xl md:text-5xl mb-4">
            About Us
          </h1>
          <p className="text-gray-300 text-base sm:text-lg max-w-xl mx-auto">
            Empowering Indian consumers with ingredient awareness
          </p>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        {/* Mission */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Our Mission</h2>
          <p className="text-gray-700 leading-relaxed mb-4">
            Parkho is an Indian consumer awareness platform designed to help you understand the ingredients in food and cosmetic products sold in India. We believe that every consumer has the right to know what's in the products they use daily.
          </p>
          <p className="text-gray-700 leading-relaxed">
            Our goal is to provide clear, factual, and neutral information about product ingredients based on publicly available regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research — without jargon, without bias, and without making health claims.
          </p>
        </section>

        {/* How It Works */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">How Parkho Works</h2>
          
          <div className="space-y-6">
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">1. Search</h3>
              <p className="text-gray-700">
                Type any Indian product name or ingredient. Our system searches our database and external sources like Open Food Facts.
              </p>
            </div>
            
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">2. AI Analysis</h3>
              <p className="text-gray-700">
                We use advanced AI to analyze ingredients and cross-reference them with regulatory databases from multiple countries.
              </p>
            </div>
            
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">3. Classification</h3>
              <p className="text-gray-700">
                Each ingredient is classified into one of three categories based on regulatory status and research discussion.
              </p>
            </div>
            
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">4. Ingredient Grade</h3>
              <p className="text-gray-700">
                We assign an Ingredient Grade (A/B/C/D) based on the percentage of clean ingredients, weighing different ingredient categories.
              </p>
            </div>
          </div>
        </section>

        {/* Data Sources */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Data Sources</h2>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>FSSAI:</strong> Food Safety and Standards Authority of India public guidelines and regulations</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Open Food Facts:</strong> Collaborative database of food products from around the world</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>WHO & EFSA:</strong> World Health Organization and European Food Safety Authority guidelines</span>
            </li>
            <li className="flex items-start gap-3">
              <svg className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span><strong>Peer-reviewed research:</strong> Published scientific studies on ingredient safety and regulation</span>
            </li>
          </ul>
        </section>

        {/* Classification System */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Classification System</h2>
          
          <div className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
              <h3 className="font-poppins font-semibold text-green-700 mb-2">Generally Recognised</h3>
              <p className="text-sm text-gray-700">
                Ingredients with no notable regulatory flags in major jurisdictions. These are widely accepted and used globally.
              </p>
            </div>
            
            <div className="p-4 bg-amber-50 rounded-lg border-l-4 border-amber-500">
              <h3 className="font-poppins font-semibold text-amber-700 mb-2">Worth Knowing</h3>
              <p className="text-sm text-gray-700">
                Ingredients that are permitted but discussed in research or have regulatory limits in some contexts. Worth being aware of.
              </p>
            </div>
            
            <div className="p-4 bg-red-50 rounded-lg border-l-4 border-red-500">
              <h3 className="font-poppins font-semibold text-red-700 mb-2">Commonly Questioned</h3>
              <p className="text-sm text-gray-700">
                Ingredients that are restricted or banned in one or more countries, or subject to significant scientific debate.
              </p>
            </div>
          </div>
        </section>

        {/* Ingredient Grade */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Understanding the Ingredient Grade</h2>

          <p className="text-gray-700 mb-6">
            We assign an Ingredient Grade (A/B/C/D) based on simple, strict rules — not weighted averages. The grade tells you at a glance how clean a product's ingredient list is.
          </p>

          <div className="mb-6">
            <h3 className="font-poppins font-semibold text-lg text-navy mb-3">Grade Rules:</h3>
            <div className="space-y-3">
              <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
                <p className="font-semibold text-green-700">Grade A — All ingredients are Generally Recognised</p>
                <p className="text-sm text-gray-700">Every ingredient is widely accepted with no notable regulatory flags anywhere in the world.</p>
              </div>
              <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                <p className="font-semibold text-blue-700">Grade B — No questioned ingredients, up to 30% Worth Knowing</p>
                <p className="text-sm text-gray-700">Mostly clean. A few permitted additives that are worth being aware of, but nothing flagged or banned.</p>
              </div>
              <div className="p-3 bg-amber-50 rounded-lg border-l-4 border-amber-500">
                <p className="font-semibold text-amber-700">Grade C — No questioned ingredients, more than 30% Worth Knowing</p>
                <p className="text-sm text-gray-700">A significant portion of the ingredient list has some concerns. Still no banned or restricted ingredients.</p>
              </div>
              <div className="p-3 bg-red-50 rounded-lg border-l-4 border-red-500">
                <p className="font-semibold text-red-700">Grade D — Contains any Commonly Questioned or Banned ingredient</p>
                <p className="text-sm text-gray-700">At least one ingredient is banned in one or more countries, or has documented health concerns from regulatory bodies. Even one such ingredient gives Grade D.</p>
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h3 className="font-poppins font-semibold text-lg text-navy mb-3">The Three Ingredient Categories:</h3>
            <ul className="space-y-3 text-gray-700">
              <li className="flex items-start gap-3">
                <span className="mt-1 w-3 h-3 rounded-full bg-green-500 flex-shrink-0"></span>
                <div>
                  <strong>Generally Recognised</strong> — No notable regulatory flags in any major jurisdiction. Widely accepted globally.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-1 w-3 h-3 rounded-full bg-amber-400 flex-shrink-0"></span>
                <div>
                  <strong>Worth Knowing</strong> — Permitted but with some discussion in research, dietary concerns, or usage limits. Fine for most people in regulated amounts.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="mt-1 w-3 h-3 rounded-full bg-red-600 flex-shrink-0"></span>
                <div>
                  <strong>Commonly Questioned</strong> — Restricted or banned in one or more countries, or associated with significant health evidence. Any product containing these gets Grade D.
                </div>
              </li>
            </ul>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Important:</strong> The Ingredient Grade is based on published international regulatory data from FSSAI, WHO, EFSA and EU regulations. It is not a safety rating or health claim. Individual responses to ingredients vary. Always consult a qualified professional for personal health decisions.
            </p>
          </div>
        </section>

        {/* Legal Disclaimer */}
        <section className="mb-8">
          <DisclaimerBox variant="legal">
            <h3 className="font-poppins font-bold text-lg mb-3">Legal Disclaimer</h3>
            <div className="space-y-3 text-sm">
              <p>
                Parkho provides ingredient information for general awareness only. Our classifications are based on publicly available international regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research.
              </p>
              <p>
                <strong>This is not medical advice.</strong> Parkho does not certify any product as safe or unsafe. We do not make health claims. Individual responses to ingredients vary.
              </p>
              <p>
                The Ingredient Grade is not a safety rating, health claim, or medical assessment. Grade D means one or more commonly questioned or banned ingredients are present. Grade A means all ingredients are generally recognised as safe. Grades B and C reflect the proportion of worth-knowing additives among otherwise clean ingredients.
              </p>
              <p>
                Always read the actual product label and consult a qualified healthcare professional for personal health decisions.
              </p>
              <p>
                Parkho is an educational tool and should not be used as the sole basis for product selection or health decisions.
              </p>
            </div>
          </DisclaimerBox>
        </section>

        {/* Contact/Feedback */}
        <section className="card p-8 text-center">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Questions or Feedback?</h2>
          <p className="text-gray-700 mb-6">
            Parkho is continuously improving. If you have suggestions or find any issues, we'd love to hear from you.
          </p>
          <p className="text-sm text-gray-500">
            This is an open-source educational project built to empower Indian consumers.
          </p>
        </section>
      </div>
    </motion.div>
    </>
  )
}

export default About
