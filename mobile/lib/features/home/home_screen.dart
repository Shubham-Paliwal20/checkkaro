import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _quickSearchItems = [
  ('🍜 Maggi Masala',    'Maggi 2-Minute Masala Noodles',         'Instant Noodles'),
  ('🍪 Parle-G',         'Parle-G Gold Biscuits',                 'Biscuits'),
  ('🥤 Thums Up',        'Thums Up',                              'Soft Drink'),
  ('🧴 Dove Soap',       'Dove Beauty Bar',                       'Personal Care'),
  ('🌿 Parachute Oil',   'Parachute Advanced Coconut Hair Oil',   'Hair Care'),
  ('✨ Lakme Sunscreen',  'Lakme Sun Expert SPF 50',               'Skincare'),
  ('🧈 Amul Butter',     'Amul Butter',                           'Dairy'),
  ('🌶 Kurkure',         'Kurkure Masala Munch',                  'Snacks'),
];


class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider);
    return Scaffold(
      backgroundColor: Colors.white,
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _HeroSection(user: user),
            _ContributeCTA(),
            _FeaturesSection(),
            _HowItWorksSection(),
            _StatsSection(),
            _ReviewsSection(user: user),
            _IngredientCTA(),
            _AppFooter(),
          ],
        ),
      ),
    );
  }
}

// ── Hero ──────────────────────────────────────────────────────────────────────

class _HeroSection extends StatelessWidget {
  final AuthUser? user;
  const _HeroSection({this.user});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      padding: EdgeInsets.fromLTRB(
          20, MediaQuery.of(context).padding.top + 16, 20, 28),
      child: Column(
        children: [
          // ── Top bar: Parkho logo + Login ──
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.asset('assets/images/logo.png', width: 32, height: 32, fit: BoxFit.cover),
                  ),
                  const SizedBox(width: 8),
                  const Text('Parkho',
                      style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w900,
                          color: AppColors.brandBlue,
                          fontFamily: 'Poppins')),
                ],
              ),
              GestureDetector(
                onTap: () => context.push('/login'),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                      color: AppColors.brandBlue,
                      borderRadius: BorderRadius.circular(20)),
                  child: user != null
                      ? Row(mainAxisSize: MainAxisSize.min, children: [
                          CircleAvatar(radius: 9, backgroundColor: Colors.white,
                              child: Text(user!.email[0].toUpperCase(),
                                  style: const TextStyle(color: AppColors.brandBlue, fontSize: 11, fontWeight: FontWeight.w800))),
                          const SizedBox(width: 6),
                          Text(user!.email.split('@')[0],
                              style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700)),
                        ])
                      : const Text('Login',
                          style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w700, fontFamily: 'Poppins')),
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          // Indian flag badge
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                  colors: [Color(0xFFFFF7ED), Color(0xFFF0FDF4)]),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: AppColors.border),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _dot(AppColors.brandOrange),
                const SizedBox(width: 3),
                _dot(Colors.white, border: true),
                const SizedBox(width: 3),
                _dot(const Color(0xFF138808)),
                const SizedBox(width: 8),
                RichText(
                  text: const TextSpan(
                    style: TextStyle(fontSize: 12, fontFamily: 'Poppins'),
                    children: [
                      TextSpan(text: 'Loved', style: TextStyle(color: AppColors.brandOrange, fontWeight: FontWeight.w700)),
                      TextSpan(text: ' by users across ', style: TextStyle(color: AppColors.textMuted)),
                      TextSpan(text: 'India', style: TextStyle(color: Color(0xFF138808), fontWeight: FontWeight.w700)),
                    ],
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 20),

          const Text('Know Your',
              style: TextStyle(fontSize: 30, fontWeight: FontWeight.w400, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          Wrap(
            alignment: WrapAlignment.center,
            crossAxisAlignment: WrapCrossAlignment.center,
            spacing: 6,
            children: const [
              Text('FOOD', style: TextStyle(fontSize: 30, fontWeight: FontWeight.w900, color: AppColors.brandOrange, fontFamily: 'Poppins')),
              Text('AND',  style: TextStyle(fontSize: 20, fontWeight: FontWeight.w400, color: AppColors.textMuted,   fontFamily: 'Poppins')),
              Text('COSMETIC', style: TextStyle(fontSize: 30, fontWeight: FontWeight.w900, color: AppColors.brandGreen, fontFamily: 'Poppins')),
            ],
          ),
          const Text('Products',
              style: TextStyle(fontSize: 30, fontWeight: FontWeight.w400, color: AppColors.textPrimary, fontFamily: 'Poppins')),

          const SizedBox(height: 12),
          const Text(
            'Search any Indian product and understand every ingredient — explained simply, no jargon.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
          ),

          const SizedBox(height: 22),

          // Search bar
          GestureDetector(
            onTap: () => context.go('/products'),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: AppColors.border),
                boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10, offset: const Offset(0, 2))],
              ),
              child: Row(
                children: [
                  const Icon(Icons.search, color: AppColors.textMuted, size: 22),
                  const SizedBox(width: 12),
                  const Expanded(
                    child: Text('Search any product... e.g., Maggi, Dove Soap',
                        style: TextStyle(color: AppColors.textMuted, fontSize: 14)),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(8)),
                    child: const Text('Search',
                        style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w700)),
                  ),
                ],
              ),
            ),
          ),

          const SizedBox(height: 16),

          const Text('Popular searches across categories',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
          const SizedBox(height: 10),

          Wrap(
            alignment: WrapAlignment.center,
            spacing: 8,
            runSpacing: 8,
            children: _quickSearchItems.map((item) {
              return GestureDetector(
                onTap: () => context.push('/product/q?name=${Uri.encodeComponent(item.$2)}'),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: AppColors.border),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 4)],
                  ),
                  child: Column(
                    children: [
                      Text(item.$1, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                      const SizedBox(height: 2),
                      Text(item.$3, style: const TextStyle(fontSize: 10, color: AppColors.textMuted)),
                    ],
                  ),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _dot(Color color, {bool border = false}) => Container(
        width: 10, height: 10,
        decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
            border: border ? Border.all(color: const Color(0xFFD1D5DB)) : null),
      );
}

// ── Contribute CTA ────────────────────────────────────────────────────────────

class _ContributeCTA extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 28),
      decoration: const BoxDecoration(
        gradient: LinearGradient(colors: [Color(0xFFFFF7ED), Colors.white, Color(0xFFE8F5E9)]),
        border: Border.symmetric(horizontal: BorderSide(color: AppColors.border)),
      ),
      child: Column(
        children: [
          const Text('Know a product we don\'t have?',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          const Text(
            'Submit any Indian product — just a photo and the product name. You earn ₹1 for every approved submission.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
          ),
          const SizedBox(height: 16),
          GestureDetector(
            onTap: () => context.go('/contribute'),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              decoration: BoxDecoration(
                  color: AppColors.brandOrange,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [BoxShadow(color: AppColors.brandOrange.withOpacity(0.3), blurRadius: 8, offset: const Offset(0, 3))]),
              child: const Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text('📦', style: TextStyle(fontSize: 16)),
                  SizedBox(width: 8),
                  Text('Add Product and Earn ₹1', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 14)),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Features ──────────────────────────────────────────────────────────────────

class _FeaturesSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.fromLTRB(20, 32, 20, 32),
      child: Column(
        children: [
          const Text('WHAT PARKHO DOES',
              style: TextStyle(fontSize: 11, color: AppColors.brandOrange, fontWeight: FontWeight.w700, letterSpacing: 1.2)),
          const SizedBox(height: 6),
          const Text('Everything you need to know',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 20),
          _FeatureCard(
            icon: Icons.shopping_cart_outlined,
            iconColor: AppColors.brandOrange, iconBg: const Color(0xFFFFF7ED),
            borderColor: AppColors.brandOrange, title: 'Food Analysis', titleColor: AppColors.brandOrange,
            desc: 'Breaks down every ingredient in your favourite Indian packaged foods. Understand what each ingredient is and how regulators view it worldwide.',
            linkText: 'Search a food product →',
            onTap: () => context.go('/products'),
          ),
          const SizedBox(height: 12),
          // Cosmetic Analysis uses GREEN (website primary = #138808)
          _FeatureCard(
            icon: Icons.star_outline,
            iconColor: AppColors.brandGreen, iconBg: AppColors.brandGreenLight,
            borderColor: AppColors.brandGreen, title: 'Cosmetic Analysis', titleColor: AppColors.brandGreen,
            desc: 'Analyses ingredients in Indian personal care products and highlights chemicals avoided in other countries.',
            linkText: 'Search a cosmetic →',
            onTap: () => context.go('/products'),
          ),
          const SizedBox(height: 12),
          _FeatureCard(
            icon: Icons.science_outlined,
            iconColor: AppColors.brandOrange, iconBg: const Color(0xFFFFF7ED),
            borderColor: AppColors.brandOrange, title: 'Check Any Ingredient', titleColor: AppColors.brandOrange,
            desc: 'Spotted an unfamiliar ingredient on a label? Type it directly and get a plain-English explanation of what it is and its regulatory status globally.',
            linkText: 'Check an ingredient →',
            onTap: () => context.go('/check-ingredient'),
          ),
        ],
      ),
    );
  }
}

class _FeatureCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor, iconBg, borderColor, titleColor;
  final String title, desc, linkText;
  final VoidCallback onTap;
  const _FeatureCard({required this.icon, required this.iconColor, required this.iconBg, required this.borderColor, required this.title, required this.titleColor, required this.desc, required this.linkText, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white, borderRadius: BorderRadius.circular(16),
        border: Border(left: BorderSide(color: borderColor, width: 4)),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2))],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(width: 44, height: 44, decoration: BoxDecoration(color: iconBg, shape: BoxShape.circle), child: Icon(icon, color: iconColor, size: 22)),
          const SizedBox(height: 12),
          Text(title, style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: titleColor, fontFamily: 'Poppins')),
          const SizedBox(height: 6),
          Text(desc, style: const TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.6)),
          const SizedBox(height: 10),
          GestureDetector(onTap: onTap, child: Text(linkText, style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: titleColor))),
        ],
      ),
    );
  }
}

// ── How It Works ──────────────────────────────────────────────────────────────

class _HowItWorksSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.surface,
      padding: const EdgeInsets.fromLTRB(20, 32, 20, 32),
      child: Column(
        children: [
          const Text('How It Works',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 24),
          const Row(
            children: [
              _Step(number: '1', label: 'Search',    desc: 'Type any Indian product or ingredient name',               filled: true,  color: AppColors.brandOrange),
              SizedBox(width: 8),
              _Step(number: '2', label: 'Analyse',   desc: 'We check every ingredient against regulatory databases',    filled: false, color: AppColors.brandOrange),
              SizedBox(width: 8),
              // Step 3 = website primary = GREEN
              _Step(number: '3', label: 'Understand', desc: 'Get a clear breakdown without confusing jargon',          filled: true,  color: AppColors.brandGreen),
            ],
          ),
        ],
      ),
    );
  }
}

class _Step extends StatelessWidget {
  final String number, label, desc;
  final bool filled;
  final Color color;
  const _Step({required this.number, required this.label, required this.desc, required this.filled, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: [
          Container(
            width: 52, height: 52,
            decoration: BoxDecoration(
              color: filled ? color : Colors.white, shape: BoxShape.circle,
              border: filled ? null : Border.all(color: color, width: 2),
            ),
            child: Center(child: Text(number, style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900, color: filled ? Colors.white : color, fontFamily: 'Poppins'))),
          ),
          const SizedBox(height: 10),
          Text(label, textAlign: TextAlign.center, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
          const SizedBox(height: 4),
          Text(desc, textAlign: TextAlign.center, style: const TextStyle(fontSize: 11, color: AppColors.textMuted, height: 1.4)),
        ],
      ),
    );
  }
}

// ── Stats ─────────────────────────────────────────────────────────────────────

class _StatsSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 28, horizontal: 20),
      decoration: const BoxDecoration(
        gradient: LinearGradient(colors: [Color(0xFFFFF7ED), Colors.white, Color(0xFFE8F5E9)]),
      ),
      child: const Row(
        children: [
          _Stat(value: '1000+', label: 'Ingredients classified',   color: AppColors.brandOrange),
          _Stat(value: '1400+', label: 'Indian products analysed', color: AppColors.textPrimary),
          // "100% Free" uses website primary = GREEN
          _Stat(value: '100%',  label: 'Free — No login needed',   color: AppColors.brandGreen),
        ],
      ),
    );
  }
}

class _Stat extends StatelessWidget {
  final String value, label;
  final Color color;
  const _Stat({required this.value, required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: [
          Text(value, textAlign: TextAlign.center, style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: color, fontFamily: 'Poppins')),
          const SizedBox(height: 4),
          Text(label, textAlign: TextAlign.center, style: const TextStyle(fontSize: 10, color: AppColors.textMuted, height: 1.3)),
        ],
      ),
    );
  }
}

// ── Reviews ───────────────────────────────────────────────────────────────────

class _ReviewsSection extends StatefulWidget {
  final AuthUser? user;
  const _ReviewsSection({this.user});

  @override
  State<_ReviewsSection> createState() => _ReviewsSectionState();
}

class _ReviewsSectionState extends State<_ReviewsSection> {
  List<Map<String, dynamic>> _reviews = [];

  @override
  void initState() {
    super.initState();
    ApiClient.getReviews().then((data) {
      if (mounted && data.isNotEmpty) setState(() => _reviews = data);
    });
  }

  void _openWriteReview() {
    final user = widget.user;
    if (user == null) {
      showModalBottomSheet(
        context: context,
        backgroundColor: Colors.white,
        isScrollControlled: true,
        shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
        builder: (ctx) => Padding(
          padding: EdgeInsets.fromLTRB(24, 20, 24, MediaQuery.of(ctx).viewInsets.bottom + 36),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Container(width: 40, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2))),
              const SizedBox(height: 24),
              Container(
                width: 60, height: 60,
                decoration: const BoxDecoration(color: Color(0xFFFFF7ED), shape: BoxShape.circle),
                child: const Icon(Icons.star_outline, color: AppColors.brandOrange, size: 30),
              ),
              const SizedBox(height: 16),
              const Text('Login to Write a Review', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
              const SizedBox(height: 8),
              const Text('Share your experience with Parkho. Log in to write a review.', textAlign: TextAlign.center, style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () { Navigator.of(ctx).pop(); context.push('/login'); },
                  style: ElevatedButton.styleFrom(backgroundColor: AppColors.brandOrange, foregroundColor: Colors.white, elevation: 0, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)), padding: const EdgeInsets.symmetric(vertical: 15)),
                  child: const Text('Log In / Sign Up', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w700)),
                ),
              ),
              const SizedBox(height: 12),
              TextButton(onPressed: () => Navigator.of(ctx).pop(), child: const Text('Not now', style: TextStyle(color: AppColors.textMuted, fontSize: 14))),
            ],
          ),
        ),
      );
      return;
    }
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (_) => _WriteReviewSheet(user: user, onSubmitted: () {
        ApiClient.getReviews().then((data) {
          if (mounted && data.isNotEmpty) setState(() => _reviews = data);
        });
      }),
    );
  }

  @override
  Widget build(BuildContext context) {
    final colors = [AppColors.brandOrange, AppColors.brandGreen, AppColors.brandOrange];
    return Container(
      color: Colors.white,
      padding: const EdgeInsets.fromLTRB(20, 28, 0, 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(right: 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('What our users say', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
                GestureDetector(
                  onTap: _openWriteReview,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                    decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(20)),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.star_outline, color: Colors.white, size: 15),
                        SizedBox(width: 5),
                        Text('Write a Review', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w700)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          if (_reviews.isEmpty)
            const Padding(
              padding: EdgeInsets.only(right: 20, bottom: 4),
              child: Text('Be the first to write a review!', style: TextStyle(fontSize: 13, color: AppColors.textMuted)),
            )
          else
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.only(right: 20),
              child: Row(
                children: _reviews.asMap().entries.map((e) {
                  final c = colors[e.key % colors.length];
                  final name   = (e.value['reviewer_name'] as String? ?? 'User');
                  final text   = (e.value['review_text']   as String? ?? '');
                  final rating = (e.value['rating']        as num?)?.toInt() ?? 5;
                  return Container(
                    width: 260,
                    margin: const EdgeInsets.only(right: 12),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(16),
                      boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.07), blurRadius: 12, offset: const Offset(0, 2))],
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Container(height: 4, decoration: BoxDecoration(color: c, borderRadius: const BorderRadius.vertical(top: Radius.circular(16)))),
                        Padding(
                          padding: const EdgeInsets.all(16),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('"', style: TextStyle(fontSize: 40, color: c.withOpacity(0.25), height: 0.8, fontFamily: 'Georgia')),
                              const SizedBox(height: 6),
                              Text(text, style: const TextStyle(fontSize: 13, color: Color(0xFF374151), height: 1.6)),
                              const SizedBox(height: 10),
                              Row(children: List.generate(5, (i) => Icon(Icons.star, size: 14, color: i < rating ? AppColors.brandOrange : AppColors.border))),
                              const SizedBox(height: 10),
                              Row(
                                children: [
                                  Container(
                                    width: 36, height: 36,
                                    decoration: BoxDecoration(color: c.withOpacity(0.1), shape: BoxShape.circle, border: Border.all(color: c, width: 1.5)),
                                    child: Center(child: Text(name.isNotEmpty ? name[0].toUpperCase() : '?', style: TextStyle(color: c, fontWeight: FontWeight.w800, fontSize: 15))),
                                  ),
                                  const SizedBox(width: 10),
                                  Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Text(name, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 13)),
                                      const Text('Verified user', style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
                                    ],
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                }).toList(),
              ),
            ),
        ],
      ),
    );
  }
}

// ── Write Review sheet ────────────────────────────────────────────────────────

class _WriteReviewSheet extends StatefulWidget {
  final AuthUser user;
  final VoidCallback onSubmitted;
  const _WriteReviewSheet({required this.user, required this.onSubmitted});

  @override
  State<_WriteReviewSheet> createState() => _WriteReviewSheetState();
}

class _WriteReviewSheetState extends State<_WriteReviewSheet> {
  final _nameCtrl = TextEditingController();
  final _textCtrl = TextEditingController();
  int _rating = 5;
  bool _loading = false;
  String? _msg;
  bool _success = false;

  @override
  void initState() {
    super.initState();
    _nameCtrl.text = widget.user.email.split('@')[0];
  }

  @override
  void dispose() {
    _nameCtrl.dispose();
    _textCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (_nameCtrl.text.trim().isEmpty) { setState(() => _msg = 'Please enter your name.'); return; }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$supabaseUrl/rest/v1/reviews',
        data: {
          'reviewer_name': _nameCtrl.text.trim(),
          'rating': _rating,
          'review_text': _textCtrl.text.trim(),
          'is_approved': false,
        },
        options: Options(headers: {
          'apikey': supabaseAnonKey,
          'Authorization': 'Bearer ${widget.user.accessToken}',
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal',
        }),
      );
      setState(() { _success = true; });
      widget.onSubmitted();
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['message']?.toString() ?? 'Failed to submit review.');
    } catch (_) {
      setState(() => _msg = 'Something went wrong. Please try again.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      padding: EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: [
            Center(child: Container(width: 36, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            const Text('⭐ Write a Review', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
            const SizedBox(height: 4),
            const Text('Your review will appear after admin approval.', style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
            const SizedBox(height: 20),
            if (!_success) ...[
              // Star rating
              const Text('Rating', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
              const SizedBox(height: 8),
              Row(
                children: List.generate(5, (i) => GestureDetector(
                  onTap: () => setState(() => _rating = i + 1),
                  child: Padding(
                    padding: const EdgeInsets.only(right: 6),
                    child: Icon(Icons.star, size: 32, color: i < _rating ? AppColors.brandOrange : AppColors.border),
                  ),
                )),
              ),
              const SizedBox(height: 16),
              // Name
              const Text('Your name', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
              const SizedBox(height: 5),
              TextField(
                controller: _nameCtrl,
                style: const TextStyle(fontSize: 14),
                decoration: InputDecoration(
                  hintText: 'How should we display your name?',
                  hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
                  filled: true, fillColor: AppColors.surface,
                  contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                  focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
                ),
              ),
              const SizedBox(height: 12),
              // Review text
              const Text('Your review (optional)', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
              const SizedBox(height: 5),
              TextField(
                controller: _textCtrl,
                maxLines: 4,
                style: const TextStyle(fontSize: 14),
                decoration: InputDecoration(
                  hintText: 'Share your experience with Parkho...',
                  hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
                  filled: true, fillColor: AppColors.surface,
                  contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                  enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                  focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
                ),
              ),
              const SizedBox(height: 16),
              if (_msg != null)
                Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: const Color(0xFFFEF2F2), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFFCA5A5))),
                  child: Text(_msg!, style: const TextStyle(fontSize: 12, color: Color(0xFFDC2626))),
                ),
              GestureDetector(
                onTap: _loading ? null : _submit,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: _loading ? AppColors.textMuted : AppColors.brandOrange, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: _loading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text('Submit Review', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ] else ...[
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: const Color(0xFFF0FDF4), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF86EFAC))),
                child: const Row(
                  children: [
                    Icon(Icons.check_circle, color: Color(0xFF16a34a), size: 24),
                    SizedBox(width: 12),
                    Expanded(child: Text('Review submitted! It will appear after admin approval. Thank you!', style: TextStyle(fontSize: 13, color: Color(0xFF15803D)))),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => Navigator.pop(context),
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: AppColors.textPrimary, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: const Text('Done', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

// ── Ingredient CTA (dark navy) ────────────────────────────────────────────────

class _IngredientCTA extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: AppColors.textPrimary,
      padding: const EdgeInsets.fromLTRB(20, 32, 20, 32),
      child: Column(
        children: [
          const Text('Not sure about an ingredient?',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: Colors.white, fontFamily: 'Poppins')),
          const SizedBox(height: 10),
          const Text(
            'Type any ingredient name or E-number from a product label and get instant information — what it is, where it\'s used, and its regulatory status.',
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 12, color: Color(0xFFD1D5DB), height: 1.6),
          ),
          const SizedBox(height: 20),
          GestureDetector(
            onTap: () => context.go('/check-ingredient'),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 13),
              decoration: BoxDecoration(
                  color: AppColors.brandOrange, borderRadius: BorderRadius.circular(24),
                  boxShadow: [BoxShadow(color: AppColors.brandOrange.withOpacity(0.4), blurRadius: 10, offset: const Offset(0, 4))]),
              child: const Text('Check an Ingredient',
                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 14, fontFamily: 'Poppins')),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Footer ────────────────────────────────────────────────────────────────────

class _AppFooter extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: const Color(0xFF111827),
      padding: const EdgeInsets.fromLTRB(20, 28, 20, 32),
      child: Column(
        children: [
          Row(
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(7),
                child: Image.asset('assets/images/logo.png', width: 28, height: 28, fit: BoxFit.cover),
              ),
              const SizedBox(width: 8),
              const Text('Parkho', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w900, color: Colors.white, fontFamily: 'Poppins')),
            ],
          ),
          const SizedBox(height: 10),
          const Text(
            'Know what\'s inside your everyday products. Transparent. Simple. Free.',
            style: TextStyle(fontSize: 12, color: Color(0xFF9ca3af), height: 1.5),
          ),
          const SizedBox(height: 20),
          Wrap(
            spacing: 16,
            runSpacing: 10,
            children: [
              _footerLink('Home',             () => context.go('/')),
              _footerLink('Products',         () => context.go('/products')),
              _footerLink('Check Ingredient', () => context.go('/check-ingredient')),
              _footerLink('Blog',             () => context.go('/blog')),
              _footerLink('About',            () => context.go('/about')),
              _footerLink('Contribute',       () => context.go('/contribute')),
            ],
          ),
          const SizedBox(height: 20),
          const Divider(color: Color(0xFF374151)),
          const SizedBox(height: 12),
          const Text('© 2026 Parkho. All rights reserved.',
              style: TextStyle(fontSize: 11, color: Color(0xFF6b7280))),
          const SizedBox(height: 4),
          const Text('Data is for awareness only. Not medical advice.',
              style: TextStyle(fontSize: 10, color: Color(0xFF4b5563))),
        ],
      ),
    );
  }

  Widget _footerLink(String label, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Text(label, style: const TextStyle(fontSize: 12, color: Color(0xFFd1d5db), fontWeight: FontWeight.w500)),
    );
  }
}
