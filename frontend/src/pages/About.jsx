import { motion } from 'framer-motion'
import DisclaimerBox from '../components/DisclaimerBox'

function About() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="min-h-screen bg-gray-soft py-12"
    >
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="section-heading mb-4">About CheckKaro</h1>
          <p className="text-lg text-gray-600">
            Empowering Indian consumers with ingredient awareness
          </p>
        </div>

        {/* Mission */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Our Mission</h2>
          <p className="text-gray-700 leading-relaxed mb-4">
            CheckKaro is an Indian consumer awareness platform designed to help you understand the ingredients in food and cosmetic products sold in India. We believe that every consumer has the right to know what's in the products they use daily.
          </p>
          <p className="text-gray-700 leading-relaxed">
            Our goal is to provide clear, factual, and neutral information about product ingredients based on publicly available regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research — without jargon, without bias, and without making health claims.
          </p>
        </section>

        {/* How It Works */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">How CheckKaro Works</h2>
          
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
                We use advanced AI (Groq Llama 3) to analyze ingredients and cross-reference them with regulatory databases from multiple countries.
              </p>
            </div>
            
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">3. Classification</h3>
              <p className="text-gray-700">
                Each ingredient is classified into one of three categories based on regulatory status and research discussion.
              </p>
            </div>
            
            <div>
              <h3 className="font-poppins font-semibold text-lg text-primary mb-2">4. Awareness Score</h3>
              <p className="text-gray-700">
                We calculate an Awareness Score (0-100) that reflects how commonly ingredients are discussed by researchers and flagged by regulators.
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

        {/* Awareness Score */}
        <section className="card p-8 mb-8">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Understanding the Awareness Score</h2>
          <p className="text-gray-700 mb-4">
            The Awareness Score (0-100) is calculated based on ingredient classifications:
          </p>
          <ul className="space-y-2 text-gray-700 mb-4">
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Start at 100</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Subtract 3 points for each "worth knowing" ingredient</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Subtract 12 points for each "commonly questioned" ingredient</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Minimum score is 5</span>
            </li>
          </ul>
          <div className="p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-gray-700">
              <strong>Important:</strong> The Awareness Score reflects regulatory discussion frequency, not product quality or health impact. It is not a safety rating or health claim.
            </p>
          </div>
        </section>

        {/* Legal Disclaimer */}
        <section className="mb-8">
          <DisclaimerBox variant="legal">
            <h3 className="font-poppins font-bold text-lg mb-3">Legal Disclaimer</h3>
            <div className="space-y-3 text-sm">
              <p>
                CheckKaro provides ingredient information for general awareness only. Our classifications are based on publicly available international regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research.
              </p>
              <p>
                <strong>This is not medical advice.</strong> CheckKaro does not certify any product as safe or unsafe. We do not make health claims. Individual responses to ingredients vary.
              </p>
              <p>
                The Awareness Score is not a safety rating, health claim, or medical assessment. It reflects how commonly ingredients are discussed by researchers and flagged by international regulatory bodies.
              </p>
              <p>
                Always read the actual product label and consult a qualified healthcare professional for personal health decisions.
              </p>
              <p>
                CheckKaro is an educational tool and should not be used as the sole basis for product selection or health decisions.
              </p>
            </div>
          </DisclaimerBox>
        </section>

        {/* Contact/Feedback */}
        <section className="card p-8 text-center">
          <h2 className="font-poppins font-bold text-2xl text-navy mb-4">Questions or Feedback?</h2>
          <p className="text-gray-700 mb-6">
            CheckKaro is continuously improving. If you have suggestions or find any issues, we'd love to hear from you.
          </p>
          <p className="text-sm text-gray-500">
            This is an open-source educational project built to empower Indian consumers.
          </p>
        </section>
      </div>
    </motion.div>
  )
}

export default About
