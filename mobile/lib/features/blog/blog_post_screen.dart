import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _staticContent = {
  'static-1': '''Most Indians pick up a packet of chips or biscuits without a second glance at the ingredient list. But what if that list told a very different story than the attractive packaging?

India's packaged food industry is booming. With over 40,000 food products on shelves, we're eating more processed food than ever before. And yet, most of us have no idea what's actually inside these products.

## What to look for on a food label

The first thing to understand is that ingredients are listed in descending order of quantity. So if sugar is the first ingredient in your "health" cereal — it's mostly sugar.

Common red flags to watch out for:
- **Partially hydrogenated oils**: A source of trans fats, linked to heart disease
- **High Fructose Corn Syrup**: Added sugar that's metabolised differently by your body
- **Artificial colours like Tartrazine (E102)**: Linked to hyperactivity in children
- **Sodium nitrite**: Used in processed meats, a known carcinogen at high levels

## The "natural flavours" trick

Brands love to use the phrase "natural flavours" — but this can mean almost anything. Natural strawberry flavour can legally be derived from wood shavings treated with chemicals. It doesn't have to come from actual strawberries.

## What FSSAI requires

The Food Safety and Standards Authority of India (FSSAI) mandates that all packaged foods display a complete ingredient list, nutritional information per 100g, any allergens in bold, manufacturing and expiry date, and vegetarian/non-vegetarian symbol.

## Start small

You don't need to become an expert overnight. Start by checking the first three ingredients on your next grocery run. If you can't pronounce them or don't know what they are — look them up on Parkho before buying.''',

  'static-2': '''Walk into any pharmacy or beauty store in India and pick up a moisturiser. Flip it over. Chances are high you'll find methylparaben, propylparaben, or butylparaben somewhere in the ingredient list.

Parabens are preservatives. They've been used in cosmetics since the 1950s to prevent bacteria and mould from growing in your lotions and creams.

## Why people are worried

The alarm bells started in 2004 when a UK study found traces of parabens in breast tumour tissue. Headlines screamed that parabens cause cancer. Social media ran with it. "Paraben-free" became the hottest marketing claim in beauty.

But here's what that study actually showed: parabens were present in the tissue. It did NOT show that parabens caused the cancer. Correlation is not causation.

## What regulators say

The European Scientific Committee on Consumer Safety (SCCS) reviewed the evidence extensively. Their conclusion: parabens like methylparaben and ethylparaben are safe at current concentrations used in cosmetics.

## What this means for you

If you have sensitive skin or prefer to avoid them out of caution, go ahead — there are good paraben-free options available. But don't panic if you see them on a label. The science does not support avoiding them entirely.''',

  'static-3': '''E211 appears on ingredient lists of dozens of Indian soft drinks and packaged juices. But what exactly is it?

**E211 is sodium benzoate** — a salt of benzoic acid. It's been used as a food preservative since the 1900s.

## What does it do?

Sodium benzoate prevents the growth of microorganisms, particularly moulds and yeasts, in acidic foods like soft drinks, fruit juices, pickles, and sauces. Without it, your Limca would grow mould within days.

## Is it safe?

On its own, sodium benzoate is considered safe by most regulatory bodies at the concentrations allowed in food (typically 0.1% or less).

**The problem**: when sodium benzoate is combined with ascorbic acid (Vitamin C), they can react to form benzene — a known carcinogen. Many soft drinks contain both sodium benzoate and ascorbic acid.

## FSSAI stance

FSSAI permits sodium benzoate in certain food categories at specified limits. It hasn't issued specific warnings about the benzene formation issue.

## The Parkho verdict

Worth Knowing — safe on its own, but the combination with Vitamin C is a legitimate concern. Check if your drink has both E211 and Vitamin C listed.''',
};

const _staticMeta = {
  'static-1': (title: 'Why You Should Read Food Labels Before Buying Packaged Snacks in India', category: 'Food',      author: 'Parkho Editorial', date: 'Dec 01, 2025', cover: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800&q=70'),
  'static-2': (title: 'Parabens in Indian Skincare: Should You Really Be Worried?',            category: 'Cosmetics',  author: 'Parkho Editorial', date: 'Dec 03, 2025', cover: 'https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=800&q=70'),
  'static-3': (title: 'What Does E211 Mean? Understanding Sodium Benzoate in Your Drinks',     category: 'Food',      author: 'Parkho Editorial', date: 'Dec 05, 2025', cover: 'https://images.unsplash.com/photo-1543512214-318c7553f230?w=800&q=70'),
};

class BlogPostScreen extends StatefulWidget {
  final String slug;
  final bool isDynamic;
  const BlogPostScreen({super.key, required this.slug, this.isDynamic = false});

  @override
  State<BlogPostScreen> createState() => _BlogPostScreenState();
}

class _BlogPostScreenState extends State<BlogPostScreen> {
  Map<String, dynamic>? _post;
  bool   _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    if (!widget.isDynamic && _staticContent.containsKey(widget.slug)) {
      setState(() => _loading = false);
      return;
    }
    try {
      final dio = Dio();
      final res = await dio.get(
        '$supabaseUrl/rest/v1/blogs',
        queryParameters: {'or': '(slug.eq.${widget.slug},id.eq.${widget.slug})', 'status': 'eq.approved', 'limit': '1'},
        options: Options(headers: {'apikey': supabaseAnonKey}),
      );
      final list = res.data as List;
      if (mounted) setState(() { _post = list.isNotEmpty ? list.first as Map<String, dynamic> : null; _loading = false; });
    } catch (e) {
      if (mounted) setState(() { _error = 'Could not load this post. Please try again.'; _loading = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) return const Scaffold(body: Center(child: CircularProgressIndicator(color: AppColors.brandOrange)));
    if (_error != null) return Scaffold(appBar: AppBar(), body: Center(child: Text(_error!, style: const TextStyle(color: AppColors.textMuted))));

    final isStatic = _staticContent.containsKey(widget.slug) && !widget.isDynamic;
    final meta     = isStatic ? _staticMeta[widget.slug] : null;
    final content  = isStatic ? (_staticContent[widget.slug] ?? '') : (_post?['content'] as String? ?? '');

    final title    = meta?.title    ?? (_post?['title']       as String? ?? '');
    final author   = meta?.author   ?? (_post?['author_name'] as String? ?? 'Contributor');
    final category = meta?.category ?? (_post?['category']    as String? ?? '');
    final date     = meta?.date     ?? ((_post?['created_at'] as String? ?? '').substring(0, 10));
    final cover    = meta?.cover    ?? (_post?['cover_image'] as String?);

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            backgroundColor: AppColors.textPrimary,
            foregroundColor: Colors.white,
            pinned: true,
            expandedHeight: cover != null ? 220 : 0,
            flexibleSpace: cover != null
                ? FlexibleSpaceBar(background: Image.network(cover, fit: BoxFit.cover, errorBuilder: (_, __, ___) => const SizedBox()))
                : null,
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 48),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (category.isNotEmpty)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(color: const Color(0xFFFFF7ED), borderRadius: BorderRadius.circular(20)),
                      child: Text(category, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.brandOrange)),
                    ),
                  const SizedBox(height: 10),
                  Text(title, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.textPrimary, fontFamily: 'Poppins', height: 1.3)),
                  const SizedBox(height: 10),
                  Row(children: [
                    const Icon(Icons.person_outline, size: 14, color: AppColors.textMuted),
                    const SizedBox(width: 4),
                    Text(author, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                    const SizedBox(width: 12),
                    const Icon(Icons.calendar_today_outlined, size: 12, color: AppColors.textMuted),
                    const SizedBox(width: 4),
                    Text(date, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                  ]),
                  const SizedBox(height: 20),
                  const Divider(),
                  const SizedBox(height: 20),
                  _SimpleMarkdown(content),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Lightweight markdown renderer (no external package needed) ─────────────────

class _SimpleMarkdown extends StatelessWidget {
  final String text;
  const _SimpleMarkdown(this.text);

  @override
  Widget build(BuildContext context) {
    final lines = text.split('\n');
    final widgets = <Widget>[];

    for (int i = 0; i < lines.length; i++) {
      final line = lines[i];
      if (line.startsWith('## ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(top: 22, bottom: 8),
          child: Text(line.substring(3), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
        ));
      } else if (line.startsWith('### ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(top: 14, bottom: 4),
          child: Text(line.substring(4), style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
        ));
      } else if (line.startsWith('- ')) {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 6, left: 4),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Padding(
                padding: EdgeInsets.only(top: 7),
                child: CircleAvatar(radius: 3, backgroundColor: AppColors.brandOrange),
              ),
              const SizedBox(width: 10),
              Expanded(child: _InlineText(line.substring(2))),
            ],
          ),
        ));
      } else if (line.isEmpty) {
        widgets.add(const SizedBox(height: 10));
      } else {
        widgets.add(Padding(
          padding: const EdgeInsets.only(bottom: 4),
          child: _InlineText(line),
        ));
      }
    }

    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: widgets);
  }
}

class _InlineText extends StatelessWidget {
  final String text;
  const _InlineText(this.text);

  @override
  Widget build(BuildContext context) {
    // Parse **bold** inline
    final spans = <TextSpan>[];
    final pattern = RegExp(r'\*\*(.+?)\*\*');
    int last = 0;
    for (final m in pattern.allMatches(text)) {
      if (m.start > last) spans.add(TextSpan(text: text.substring(last, m.start)));
      spans.add(TextSpan(text: m.group(1), style: const TextStyle(fontWeight: FontWeight.w700, color: AppColors.textPrimary)));
      last = m.end;
    }
    if (last < text.length) spans.add(TextSpan(text: text.substring(last)));
    return RichText(
      text: TextSpan(
        style: const TextStyle(fontSize: 14, color: Color(0xFF374151), height: 1.8, fontFamily: 'Poppins'),
        children: spans,
      ),
    );
  }
}
