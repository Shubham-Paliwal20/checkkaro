import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Container(
              padding: EdgeInsets.fromLTRB(20, MediaQuery.of(context).padding.top + 20, 20, 28),
              decoration: const BoxDecoration(
                gradient: LinearGradient(colors: [Color(0xFF0D1B2A), Color(0xFF1B3F8A)]),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('About Parkho',
                      style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Colors.white, fontFamily: 'Poppins')),
                  const SizedBox(height: 6),
                  const Text('Empowering Indian consumers with ingredient awareness',
                      style: TextStyle(fontSize: 13, color: Color(0xFFD1D5DB), height: 1.5)),
                ],
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                _Section(
                  title: 'Our Mission',
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text(
                        'Parkho is an Indian consumer awareness platform designed to help you understand the ingredients in food and cosmetic products sold in India. We believe that every consumer has the right to know what\'s in the products they use daily.',
                        style: TextStyle(fontSize: 13, color: Color(0xFF374151), height: 1.7),
                      ),
                      SizedBox(height: 10),
                      Text(
                        'Our goal is to provide clear, factual, and neutral information about product ingredients based on publicly available regulatory data from FSSAI, WHO, EFSA, EU regulations, and peer-reviewed research — without jargon, without bias, and without making health claims.',
                        style: TextStyle(fontSize: 13, color: Color(0xFF374151), height: 1.7),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                _Section(
                  title: 'How Parkho Works',
                  child: Column(
                    children: [
                      _HowStep(num: '1', title: 'Search',         desc: 'Type any Indian product name or ingredient. Our system searches our database and external sources like Open Food Facts.'),
                      _HowStep(num: '2', title: 'AI Analysis',    desc: 'We use advanced AI to analyze ingredients and cross-reference them with regulatory databases from multiple countries.'),
                      _HowStep(num: '3', title: 'Classification', desc: 'Each ingredient is classified into one of three categories based on regulatory status and research discussion.'),
                      _HowStep(num: '4', title: 'Ingredient Grade', desc: 'We assign an Ingredient Grade (A/B/C/D) based on the percentage of clean ingredients, weighing different ingredient categories.'),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                _Section(
                  title: 'Classification System',
                  child: Column(
                    children: const [
                      _ClassCard(
                        color: Color(0xFF16a34a), bg: Color(0xFFF0FDF4), borderColor: Color(0xFF22c55e),
                        title: 'Generally Recognised',
                        desc: 'Ingredients with no notable regulatory flags in major jurisdictions. These are widely accepted and used globally.',
                      ),
                      SizedBox(height: 10),
                      _ClassCard(
                        color: Color(0xFFd97706), bg: Color(0xFFFFFBEB), borderColor: Color(0xFFF59E0B),
                        title: 'Worth Knowing',
                        desc: 'Ingredients that are permitted but discussed in research or have regulatory limits in some contexts.',
                      ),
                      SizedBox(height: 10),
                      _ClassCard(
                        color: Color(0xFFdc2626), bg: Color(0xFFFEF2F2), borderColor: Color(0xFFF87171),
                        title: 'Commonly Questioned',
                        desc: 'Ingredients that are restricted or banned in one or more countries, or subject to significant scientific debate.',
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                _Section(
                  title: 'Ingredient Grade',
                  child: Column(
                    children: const [
                      _GradeRow(grade: 'A', color: Color(0xFF16a34a), bg: Color(0xFFDCFCE7), desc: '80%+ generally recognised ingredients'),
                      SizedBox(height: 8),
                      _GradeRow(grade: 'B', color: Color(0xFF0891b2), bg: Color(0xFFE0F2FE), desc: '60–79% generally recognised'),
                      SizedBox(height: 8),
                      _GradeRow(grade: 'C', color: Color(0xFFd97706), bg: Color(0xFFFEF3C7), desc: '40–59% generally recognised'),
                      SizedBox(height: 8),
                      _GradeRow(grade: 'D', color: Color(0xFFdc2626), bg: Color(0xFFFEF2F2), desc: 'Below 40% generally recognised'),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                _Section(
                  title: 'Data Sources',
                  child: Column(
                    children: const [
                      _Source(name: 'FSSAI', desc: 'Food Safety and Standards Authority of India public guidelines and regulations'),
                      _Source(name: 'Open Food Facts', desc: 'Collaborative database of food products from around the world'),
                      _Source(name: 'WHO & EFSA', desc: 'World Health Organization and European Food Safety Authority guidelines'),
                      _Source(name: 'Peer-reviewed research', desc: 'Published scientific studies on ingredient safety and regulation'),
                    ],
                  ),
                ),

                const SizedBox(height: 12),

                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFFF7ED),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: const Color(0xFFFED7AA)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text('Disclaimer', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: Color(0xFF92400E), fontFamily: 'Poppins')),
                      SizedBox(height: 8),
                      Text(
                        'Parkho provides ingredient information for awareness only. We do not make medical or health claims. Regulatory classifications reflect publicly available data and may not be up-to-date. Always consult a healthcare professional for health-related decisions.',
                        style: TextStyle(fontSize: 12, color: Color(0xFF78350F), height: 1.6),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 32),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _Section extends StatelessWidget {
  final String title;
  final Widget child;
  const _Section({required this.title, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(16),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 14),
          child,
        ],
      ),
    );
  }
}

class _HowStep extends StatelessWidget {
  final String num, title, desc;
  const _HowStep({required this.num, required this.title, required this.desc});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 28, height: 28,
            decoration: const BoxDecoration(color: AppColors.brandGreen, shape: BoxShape.circle),
            child: Center(child: Text(num, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 13))),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: AppColors.brandGreen)),
                const SizedBox(height: 3),
                Text(desc, style: const TextStyle(fontSize: 12, color: Color(0xFF374151), height: 1.6)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ClassCard extends StatelessWidget {
  final Color color, bg, borderColor;
  final String title, desc;
  const _ClassCard({required this.color, required this.bg, required this.borderColor, required this.title, required this.desc});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bg, borderRadius: BorderRadius.circular(10),
        border: Border(left: BorderSide(color: borderColor, width: 3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: color)),
          const SizedBox(height: 4),
          Text(desc, style: const TextStyle(fontSize: 12, color: Color(0xFF374151), height: 1.5)),
        ],
      ),
    );
  }
}

class _GradeRow extends StatelessWidget {
  final String grade, desc;
  final Color color, bg;
  const _GradeRow({required this.grade, required this.desc, required this.color, required this.bg});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(
          width: 36, height: 36,
          decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(8), border: Border.all(color: color.withOpacity(0.3))),
          child: Center(child: Text(grade, style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 16))),
        ),
        const SizedBox(width: 12),
        Expanded(child: Text(desc, style: const TextStyle(fontSize: 13, color: Color(0xFF374151)))),
      ],
    );
  }
}

class _Source extends StatelessWidget {
  final String name, desc;
  const _Source({required this.name, required this.desc});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 10),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.check_circle, color: AppColors.brandGreen, size: 18),
          const SizedBox(width: 10),
          Expanded(child: RichText(text: TextSpan(style: const TextStyle(fontSize: 13, color: Color(0xFF374151), height: 1.5), children: [
            TextSpan(text: '$name: ', style: const TextStyle(fontWeight: FontWeight.w700)),
            TextSpan(text: desc),
          ]))),
        ],
      ),
    );
  }
}
