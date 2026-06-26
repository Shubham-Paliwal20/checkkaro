import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _staticBlogs = [
  (
    id: 'static-1',
    title: 'Why You Should Read Food Labels Before Buying Packaged Snacks in India',
    excerpt: 'Most Indians never read the ingredient list on packaged food. Here\'s what you\'re missing — and why it matters for your family\'s health.',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=600&q=70',
  ),
  (
    id: 'static-2',
    title: 'Parabens in Indian Skincare: Should You Really Be Worried?',
    excerpt: 'Parabens are in almost every moisturiser, shampoo, and cream on the market. But are they actually dangerous? Here\'s what the science says.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=600&q=70',
  ),
  (
    id: 'static-3',
    title: 'Hidden Sugar in "Healthy" Indian Foods — What Brands Don\'t Tell You',
    excerpt: 'Oats, granola, fruit juice, multigrain bread — they all sound healthy. But the sugar content might shock you.',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&q=70',
  ),
  (
    id: 'static-4',
    title: '5 Harmful Ingredients Hiding in Your Daily Face Cream',
    excerpt: 'Your moisturiser may be doing more harm than good. These five ingredients are worth avoiding — especially in products you use every day.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600&q=70',
  ),
  (
    id: 'static-5',
    title: 'E-Numbers in Indian Food: Which Are Safe and Which to Avoid',
    excerpt: 'E-numbers are everywhere in packaged food. But not all of them are harmful. Here\'s a simple guide to understanding what they mean.',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce?w=600&q=70',
  ),
  (
    id: 'static-6',
    title: 'How to Read a Cosmetic Ingredient List Like an Expert',
    excerpt: 'INCI names look intimidating. But once you know the basics, you\'ll never look at a skincare product the same way again.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=600&q=70',
  ),
  (
    id: 'static-7',
    title: 'Processed Meats and Cancer: What the WHO Classification Actually Means',
    excerpt: 'In 2015, the WHO classified processed meats as a Group 1 carcinogen — same as cigarettes. But does that mean salami is as dangerous as smoking?',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&q=70',
  ),
  (
    id: 'static-8',
    title: 'Aspartame, Sucralose or Stevia? What 2023 Research Changed About Artificial Sweeteners',
    excerpt: 'The WHO issued a major advisory on non-sugar sweeteners in 2023. Three landmark studies raised new concerns. Here is what the evidence says.',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1548636581-eb82ef43c3ec?w=600&q=70',
  ),
  (
    id: 'static-9',
    title: 'The Ultra-Processed Food Trap: Why the NOVA Classification Is Changing Nutrition Science',
    excerpt: 'Not all processed food is harmful. But "ultra-processed" food is a different story. Here\'s the science behind NOVA and why it matters for India.',
    category: 'Food',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=600&q=70',
  ),
  (
    id: 'static-10',
    title: 'Retinol: The Science Behind the Most Clinically Proven Anti-Ageing Skincare Ingredient',
    excerpt: 'Retinol has more peer-reviewed evidence than almost any other skincare ingredient. Here is how it works and how to use it correctly.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600&q=70',
  ),
  (
    id: 'static-11',
    title: 'Chemical vs Mineral Sunscreen: What the Science Actually Says in 2024',
    excerpt: 'The FDA flagged four major chemical UV filters as lacking sufficient safety data. Here\'s what the evidence says about which sunscreen is actually better.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=600&q=70',
  ),
  (
    id: 'static-12',
    title: 'Your Skin Barrier: The Science Behind Why It Matters More Than Any Serum You Use',
    excerpt: 'Every dermatologist gives the same advice first: fix your skin barrier before adding actives. Here\'s the biology and what\'s damaging it every day.',
    category: 'Cosmetics',
    author: 'Parkho Editorial',
    cover: 'https://images.unsplash.com/photo-1631729371254-42c2892f0e6e?w=600&q=70',
  ),
];

const _catStyle = {
  'Food':           (bg: Color(0xFFFFF7ED), text: Color(0xFFEA580C)),
  'Cosmetics':      (bg: Color(0xFFFDF2F8), text: Color(0xFFBE185D)),
  'Health':         (bg: Color(0xFFF0FDF4), text: Color(0xFF15803D)),
  'Lifestyle':      (bg: Color(0xFFEFF6FF), text: Color(0xFF1D4ED8)),
  'Product Review': (bg: Color(0xFFFAF5FF), text: Color(0xFF7E22CE)),
};

final _dynamicBlogsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  try {
    final dio = Dio();
    final res = await dio.get(
      '$supabaseUrl/rest/v1/blogs',
      queryParameters: {'status': 'eq.approved', 'order': 'created_at.desc', 'limit': '20',
        'select': 'id,title,excerpt,category,author_name,created_at,cover_image,slug'},
      options: Options(headers: {'apikey': supabaseAnonKey}),
    );
    return (res.data as List).cast<Map<String, dynamic>>();
  } catch (_) {
    return [];
  }
});

class BlogScreen extends ConsumerWidget {
  const BlogScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dynamicAsync = ref.watch(_dynamicBlogsProvider);

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
                children: const [
                  Text('Parkho Blog',
                      style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Colors.white, fontFamily: 'Poppins')),
                  SizedBox(height: 6),
                  Text('Ingredient insights, food transparency, and consumer awareness',
                      style: TextStyle(fontSize: 13, color: Color(0xFFD1D5DB), height: 1.5)),
                ],
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverToBoxAdapter(
              child: dynamicAsync.when(
                loading: () => _BlogList(dynamicPosts: null),
                error: (_, __) => _BlogList(dynamicPosts: null),
                data: (posts) => _BlogList(dynamicPosts: posts),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _BlogList extends StatelessWidget {
  final List<Map<String, dynamic>>? dynamicPosts;
  const _BlogList({required this.dynamicPosts});

  @override
  Widget build(BuildContext context) {
    final dyn = dynamicPosts ?? [];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (dyn.isNotEmpty) ...[
          const Text('Community Posts',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 10),
          ...dyn.map((b) => _DynamicCard(blog: b)),
          const SizedBox(height: 20),
        ],
        const Text('Parkho Originals',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
        const SizedBox(height: 10),
        ..._staticBlogs.map((b) => _StaticCard(blog: b)),
        const SizedBox(height: 32),
      ],
    );
  }
}

class _StaticCard extends StatelessWidget {
  final ({String id, String title, String excerpt, String category, String author, String cover}) blog;
  const _StaticCard({required this.blog});

  @override
  Widget build(BuildContext context) {
    final cat = _catStyle[blog.category];
    return GestureDetector(
      onTap: () => context.push('/blog/${blog.id}'),
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 8)]),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              child: Image.network(blog.cover, height: 160, width: double.infinity, fit: BoxFit.cover,
                  errorBuilder: (_, __, ___) => Container(height: 100, color: AppColors.surface)),
            ),
            Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (cat != null)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(color: cat.bg, borderRadius: BorderRadius.circular(20)),
                      child: Text(blog.category, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: cat.text)),
                    ),
                  const SizedBox(height: 8),
                  Text(blog.title, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textPrimary, height: 1.3)),
                  const SizedBox(height: 6),
                  Text(blog.excerpt, maxLines: 2, overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.5)),
                  const SizedBox(height: 10),
                  Row(children: [
                    const Icon(Icons.person_outline, size: 13, color: AppColors.textMuted),
                    const SizedBox(width: 4),
                    Text(blog.author, style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                  ]),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _DynamicCard extends StatelessWidget {
  final Map<String, dynamic> blog;
  const _DynamicCard({required this.blog});

  @override
  Widget build(BuildContext context) {
    final cat   = (blog['category'] as String?) ?? '';
    final cs    = _catStyle[cat];
    final slug  = (blog['slug'] as String?) ?? (blog['id'] as String);
    final cover = blog['cover_image'] as String?;

    return GestureDetector(
      onTap: () => context.push('/blog/$slug?dyn=1'),
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8)]),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (cover != null)
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Image.network(cover, width: 80, height: 80, fit: BoxFit.cover,
                    errorBuilder: (_, __, ___) => Container(width: 80, height: 80, color: AppColors.surface)),
              ),
            SizedBox(width: cover != null ? 12 : 0),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (cs != null)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(color: cs.bg, borderRadius: BorderRadius.circular(20)),
                      child: Text(cat, style: TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: cs.text)),
                    ),
                  const SizedBox(height: 6),
                  Text(blog['title'] ?? '', maxLines: 2, overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: AppColors.textPrimary, height: 1.3)),
                  const SizedBox(height: 4),
                  Text(blog['excerpt'] ?? '', maxLines: 2, overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 11, color: AppColors.textMuted, height: 1.4)),
                  const SizedBox(height: 6),
                  Text(blog['author_name'] ?? 'Contributor', style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
