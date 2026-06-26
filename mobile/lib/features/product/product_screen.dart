import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/models/product.dart';
import '../../core/theme/app_theme.dart';
import '../../shared/widgets/grade_badge.dart';

final _productProvider =
    FutureProvider.family<Product?, String>((ref, nameOrKey) async {
  for (int attempt = 0; attempt < 3; attempt++) {
    try {
      final data = await ApiClient.getProductByName(nameOrKey);
      return data == null ? null : Product.fromJson(data);
    } catch (_) {
      if (attempt == 2) rethrow;
      await Future.delayed(const Duration(seconds: 8));
    }
  }
  return null;
});

final _alternativesProvider = FutureProvider.family<
    List<Map<String, dynamic>>,
    ({String category, String name, String excludeId})>((ref, args) async {
  if (args.category.isEmpty) return [];
  return ApiClient.getSaferAlternatives(
      args.category, args.name, args.excludeId);
});

class ProductScreen extends ConsumerWidget {
  final String productKey;
  final String? productName;
  const ProductScreen(
      {super.key, required this.productKey, this.productName});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(_productProvider(productName ?? productKey));
    return state.when(
      loading: () => Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(backgroundColor: Colors.white, elevation: 0),
        body: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 14),
              Text('Loading product…', style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
            ],
          ),
        ),
      ),
      error: (e, _) => Scaffold(
        backgroundColor: Colors.white,
        appBar: AppBar(backgroundColor: Colors.white, elevation: 0),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('😕', style: TextStyle(fontSize: 48)),
                const SizedBox(height: 12),
                const Text('Could not load product',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: AppColors.textPrimary)),
                const SizedBox(height: 8),
                const Text(
                  'Please check your internet connection and try again.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
                ),
                const SizedBox(height: 24),
                ElevatedButton(
                  onPressed: () => ref.invalidate(_productProvider(productName ?? productKey)),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.brandBlue,
                    foregroundColor: Colors.white,
                    elevation: 0,
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 14),
                  ),
                  child: const Text('Retry', style: TextStyle(fontWeight: FontWeight.w700)),
                ),
              ],
            ),
          ),
        ),
      ),
      data: (product) => product == null
          ? Scaffold(
              appBar: AppBar(title: const Text('Not Found')),
              body: const Center(child: Text('Product not found')))
          : _ProductDetail(product: product),
    );
  }
}

class _ProductDetail extends ConsumerWidget {
  final Product product;
  const _ProductDetail({required this.product});

  String _gradeInsight(String grade) {
    switch (grade.toUpperCase()) {
      case 'A':
        return 'Excellent ingredient profile — safe for regular consumption.';
      case 'B':
        return 'Good ingredient profile with minor ingredients to note.';
      case 'C':
        return 'Average profile — a few ingredients worth being aware of.';
      default:
        return 'Several ingredients worth checking before regular use.';
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final gradeColor = AppColors.forGrade(product.grade);
    final gradeBg = AppColors.bgForGrade(product.grade);

    final questioned =
        product.ingredients.where((i) => i.isQuestioned).toList();
    final worthKnowing =
        product.ingredients.where((i) => i.isWorthKnowing).toList();
    final safe = product.ingredients.where((i) => i.isSafe).toList();

    final altArgs = (
      category: product.category ?? '',
      name: product.name,
      excludeId: product.id,
    );
    final altState = ref.watch(_alternativesProvider(altArgs));

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 200,
            pinned: true,
            backgroundColor: Colors.white,
            foregroundColor: AppColors.textPrimary,
            flexibleSpace: FlexibleSpaceBar(
              background: product.imageUrl != null
                  ? CachedNetworkImage(
                      imageUrl: product.imageUrl!,
                      fit: BoxFit.contain,
                      httpHeaders: const {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'},
                      errorWidget: (_, __, ___) => const _PlaceholderImage())
                  : const _PlaceholderImage(),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _HeaderCard(product: product, gradeColor: gradeColor, gradeBg: gradeBg),
                  const SizedBox(height: 14),

                  _QuickInsightCard(
                      grade: product.grade,
                      gradeColor: gradeColor,
                      gradeBg: gradeBg,
                      insight: _gradeInsight(product.grade),
                      recommendation: product.recommendation),
                  const SizedBox(height: 20),

                  if (product.ingredients.isNotEmpty) ...[
                    _CompleteIngredientsList(
                        ingredients: product.ingredients),
                    const SizedBox(height: 20),
                  ],

                  if (questioned.isNotEmpty) ...[
                    _QuestionedSection(ingredients: questioned),
                    const SizedBox(height: 16),
                  ],

                  if (worthKnowing.isNotEmpty) ...[
                    _WorthKnowingSection(ingredients: worthKnowing),
                    const SizedBox(height: 16),
                  ],

                  if (safe.isNotEmpty) ...[
                    _SafeSection(ingredients: safe),
                    const SizedBox(height: 16),
                  ],

                  if (product.ingredients.isEmpty &&
                      product.ingredientsRaw != null) ...[
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                          color: Colors.white,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: AppColors.border)),
                      child: Text(product.ingredientsRaw!,
                          style: const TextStyle(
                              fontSize: 12,
                              color: AppColors.textMuted,
                              height: 1.6)),
                    ),
                    const SizedBox(height: 16),
                  ],

                  if (product.summary != null) ...[
                    _SummaryCard(summary: product.summary!),
                    const SizedBox(height: 16),
                  ],

                  if (product.fssaiNote != null) ...[
                    _FssaiCard(note: product.fssaiNote!),
                    const SizedBox(height: 16),
                  ],

                  altState.when(
                    loading: () => const SizedBox.shrink(),
                    error: (_, __) => const SizedBox.shrink(),
                    data: (alts) => alts.isEmpty
                        ? const SizedBox.shrink()
                        : _SaferAlternatives(alternatives: alts),
                  ),

                  const SizedBox(height: 20),

                  _ReportButton(
                      productId: product.id, productName: product.name),

                  const SizedBox(height: 32),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _PlaceholderImage extends StatelessWidget {
  const _PlaceholderImage();
  @override
  Widget build(BuildContext context) => Container(
        color: AppColors.surface,
        child: const Center(
            child: Icon(Icons.inventory_2_outlined,
                size: 80, color: AppColors.textMuted)),
      );
}

class _HeaderCard extends StatelessWidget {
  final Product product;
  final Color gradeColor;
  final Color gradeBg;
  const _HeaderCard(
      {required this.product,
      required this.gradeColor,
      required this.gradeBg});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border),
          boxShadow: [
            BoxShadow(
                color: Colors.black.withOpacity(0.04),
                blurRadius: 8,
                offset: const Offset(0, 2))
          ]),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(product.name,
                    style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary,
                        fontFamily: 'Poppins')),
                if (product.brand != null) ...[
                  const SizedBox(height: 4),
                  Text(product.brand!,
                      style: const TextStyle(
                          fontSize: 14,
                          color: AppColors.brandBlue,
                          fontWeight: FontWeight.w600)),
                ],
                if (product.category != null) ...[
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                        color: AppColors.surface,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: AppColors.border)),
                    child: Text(product.category!,
                        style: const TextStyle(
                            fontSize: 11,
                            color: AppColors.textMuted,
                            fontWeight: FontWeight.w600)),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(width: 12),
          GradeBadge(grade: product.grade, size: 72, showLabel: true),
        ],
      ),
    );
  }
}

class _QuickInsightCard extends StatelessWidget {
  final String grade;
  final Color gradeColor;
  final Color gradeBg;
  final String insight;
  final String? recommendation;
  const _QuickInsightCard(
      {required this.grade,
      required this.gradeColor,
      required this.gradeBg,
      required this.insight,
      this.recommendation});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: gradeBg,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: gradeColor.withOpacity(0.3))),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.lightbulb_outline, color: gradeColor, size: 18),
              const SizedBox(width: 8),
              Text('Quick Insight',
                  style: TextStyle(
                      color: gradeColor,
                      fontWeight: FontWeight.w800,
                      fontSize: 13,
                      fontFamily: 'Poppins')),
            ],
          ),
          const SizedBox(height: 8),
          Text(insight,
              style: TextStyle(
                  color: gradeColor, fontSize: 13, height: 1.5)),
          if (recommendation != null) ...[
            const SizedBox(height: 8),
            Text(recommendation!,
                style: TextStyle(
                    color: gradeColor.withOpacity(0.8),
                    fontSize: 12,
                    fontStyle: FontStyle.italic,
                    height: 1.4)),
          ],
        ],
      ),
    );
  }
}

class _CompleteIngredientsList extends StatelessWidget {
  final List<Ingredient> ingredients;
  const _CompleteIngredientsList({required this.ingredients});

  @override
  Widget build(BuildContext context) {
    final spans = <InlineSpan>[];
    for (var i = 0; i < ingredients.length; i++) {
      final ing = ingredients[i];
      Color color;
      FontWeight weight;
      if (ing.isQuestioned) {
        color = AppColors.gradeD;
        weight = FontWeight.w700;
      } else if (ing.isWorthKnowing) {
        color = AppColors.gradeC;
        weight = FontWeight.w700;
      } else {
        color = AppColors.textMuted;
        weight = FontWeight.w400;
      }
      spans.add(TextSpan(
          text: ing.name,
          style: TextStyle(color: color, fontWeight: weight, fontSize: 12)));
      if (i < ingredients.length - 1) {
        spans.add(const TextSpan(
            text: ', ',
            style: TextStyle(color: AppColors.textMuted, fontSize: 12)));
      }
    }

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Complete Ingredients List (${ingredients.length} ingredients)',
              style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary,
                  fontFamily: 'Poppins')),
          const SizedBox(height: 10),
          RichText(
              text: TextSpan(
                  children: spans,
                  style: const TextStyle(height: 1.7))),
        ],
      ),
    );
  }
}

class _QuestionedSection extends StatelessWidget {
  final List<Ingredient> ingredients;
  const _QuestionedSection({required this.ingredients});

  @override
  Widget build(BuildContext context) {
    const color = AppColors.gradeD;
    const bg = AppColors.gradeBgD;
    final useExpansion = ingredients.length > 3;
    final cards = ingredients
        .map((ing) => _IngredientCard(ingredient: ing, color: color, bg: bg))
        .toList();

    return Container(
      decoration: BoxDecoration(
          border: const Border(
              left: BorderSide(color: color, width: 4)),
          borderRadius: BorderRadius.circular(12)),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
            color: bg,
            borderRadius: const BorderRadius.only(
                topRight: Radius.circular(12),
                bottomRight: Radius.circular(12))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Commonly Questioned',
                style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w800,
                    color: color,
                    fontFamily: 'Poppins')),
            const SizedBox(height: 10),
            if (useExpansion)
              _ExpandableList(children: cards, color: color)
            else
              ...cards,
          ],
        ),
      ),
    );
  }
}

class _WorthKnowingSection extends StatelessWidget {
  final List<Ingredient> ingredients;
  const _WorthKnowingSection({required this.ingredients});

  @override
  Widget build(BuildContext context) {
    const color = AppColors.gradeC;
    const bg = AppColors.gradeBgC;
    final useExpansion = ingredients.length > 3;
    final cards = ingredients
        .map((ing) => _IngredientCard(ingredient: ing, color: color, bg: bg))
        .toList();

    return Container(
      decoration: BoxDecoration(
          border: const Border(
              left: BorderSide(color: color, width: 4)),
          borderRadius: BorderRadius.circular(12)),
      child: Container(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
            color: bg,
            borderRadius: const BorderRadius.only(
                topRight: Radius.circular(12),
                bottomRight: Radius.circular(12))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Worth Knowing',
                style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w800,
                    color: color,
                    fontFamily: 'Poppins')),
            const SizedBox(height: 10),
            if (useExpansion)
              _ExpandableList(children: cards, color: color)
            else
              ...cards,
          ],
        ),
      ),
    );
  }
}

class _SafeSection extends StatelessWidget {
  final List<Ingredient> ingredients;
  const _SafeSection({required this.ingredients});

  @override
  Widget build(BuildContext context) {
    const color = AppColors.gradeA;
    final useExpansion = ingredients.length > 3;

    final grid = Wrap(
      spacing: 8,
      runSpacing: 8,
      children: ingredients
          .map((ing) => Container(
                padding: const EdgeInsets.symmetric(
                    horizontal: 10, vertical: 7),
                decoration: BoxDecoration(
                    color: AppColors.gradeBgA,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(
                        color: color.withOpacity(0.3))),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(ing.name,
                        style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w700,
                            color: color)),
                    if (ing.concern != null)
                      Text(ing.concern!,
                          style: const TextStyle(
                              fontSize: 11,
                              color: AppColors.textMuted,
                              height: 1.3)),
                  ],
                ),
              ))
          .toList(),
    );

    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
          color: AppColors.gradeBgA,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: color.withOpacity(0.25))),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Generally Recognised Safe',
              style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w800,
                  color: color,
                  fontFamily: 'Poppins')),
          const SizedBox(height: 10),
          if (useExpansion)
            _ExpandableList(
                children: [grid], color: color, label: 'Show all ${ingredients.length}')
          else
            grid,
        ],
      ),
    );
  }
}

class _ExpandableList extends StatefulWidget {
  final List<Widget> children;
  final Color color;
  final String? label;
  const _ExpandableList(
      {required this.children, required this.color, this.label});

  @override
  State<_ExpandableList> createState() => _ExpandableListState();
}

class _ExpandableListState extends State<_ExpandableList> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (_expanded) ...widget.children,
        if (!_expanded) widget.children.first,
        const SizedBox(height: 8),
        GestureDetector(
          onTap: () => setState(() => _expanded = !_expanded),
          child: Text(
            _expanded
                ? 'Show less'
                : (widget.label ?? 'Show all'),
            style: TextStyle(
                color: widget.color,
                fontSize: 12,
                fontWeight: FontWeight.w700,
                decoration: TextDecoration.underline),
          ),
        ),
      ],
    );
  }
}

class _IngredientCard extends StatefulWidget {
  final Ingredient ingredient;
  final Color color;
  final Color bg;
  const _IngredientCard(
      {required this.ingredient, required this.color, required this.bg});

  @override
  State<_IngredientCard> createState() => _IngredientCardState();
}

class _IngredientCardState extends State<_IngredientCard> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    final ing = widget.ingredient;
    final color = widget.color;
    final note = ing.concern ?? '';
    final isLong = note.length > 140;

    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: color.withOpacity(0.25))),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(ing.name,
              style: TextStyle(
                  fontSize: 13,
                  fontWeight: FontWeight.w700,
                  color: color)),
          if (note.isNotEmpty) ...[
            const SizedBox(height: 4),
            Text(
              isLong && !_expanded
                  ? '${note.substring(0, 140)}...'
                  : note,
              style: TextStyle(
                  fontSize: 12, color: color.withOpacity(0.8), height: 1.4),
            ),
            if (isLong) ...[
              const SizedBox(height: 4),
              GestureDetector(
                onTap: () => setState(() => _expanded = !_expanded),
                child: Text(
                  _expanded ? 'Show less' : 'Read more',
                  style: TextStyle(
                      color: color,
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      decoration: TextDecoration.underline),
                ),
              ),
            ],
          ],
          if (ing.regulatoryNote != null) ...[
            const SizedBox(height: 4),
            Text(ing.regulatoryNote!,
                style: const TextStyle(
                    fontSize: 11,
                    color: AppColors.textMuted,
                    fontStyle: FontStyle.italic,
                    height: 1.4)),
          ],
        ],
      ),
    );
  }
}

class _SummaryCard extends StatelessWidget {
  final String summary;
  const _SummaryCard({required this.summary});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Summary',
              style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w800,
                  color: AppColors.textPrimary,
                  fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          Text(summary,
              style: const TextStyle(
                  fontSize: 13, color: AppColors.textMuted, height: 1.6)),
        ],
      ),
    );
  }
}

class _FssaiCard extends StatelessWidget {
  final String note;
  const _FssaiCard({required this.note});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
          color: AppColors.gradeBgC,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.gradeC.withOpacity(0.3))),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.info_outline, color: AppColors.gradeC, size: 18),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('FSSAI Note',
                    style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                        color: AppColors.gradeC)),
                const SizedBox(height: 4),
                Text(note,
                    style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textMuted,
                        height: 1.5)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _SaferAlternatives extends StatelessWidget {
  final List<Map<String, dynamic>> alternatives;
  const _SaferAlternatives({required this.alternatives});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Safer Alternatives',
            style: TextStyle(
                fontSize: 15,
                fontWeight: FontWeight.w800,
                color: AppColors.textPrimary,
                fontFamily: 'Poppins')),
        const SizedBox(height: 10),
        SizedBox(
          height: 160,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: alternatives.length,
            separatorBuilder: (_, __) => const SizedBox(width: 10),
            itemBuilder: (context, i) {
              final alt = alternatives[i];
              final grade = (alt['grade'] ?? 'D') as String;
              final name = (alt['name'] ?? '') as String;
              final imageUrl = alt['image_url'] as String?;
              final staticKey = alt['static_key'] ?? alt['id'] ?? '';
              return GestureDetector(
                onTap: () => context.push(
                    '/product/${Uri.encodeComponent(staticKey)}?name=${Uri.encodeComponent(name)}'),
                child: Container(
                  width: 140,
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(14),
                      border: Border.all(color: AppColors.border),
                      boxShadow: [
                        BoxShadow(
                            color: Colors.black.withOpacity(0.04),
                            blurRadius: 6)
                      ]),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (imageUrl != null)
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: CachedNetworkImage(
                              imageUrl: imageUrl,
                              height: 60,
                              width: double.infinity,
                              fit: BoxFit.contain,
                              httpHeaders: const {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'},
                              errorWidget: (_, __, ___) => const Icon(
                                  Icons.inventory_2_outlined,
                                  size: 40,
                                  color: AppColors.textMuted)),
                        )
                      else
                        const SizedBox(
                            height: 60,
                            child: Center(
                                child: Icon(Icons.inventory_2_outlined,
                                    size: 40,
                                    color: AppColors.textMuted))),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          GradeBadge(grade: grade, size: 22),
                          const Text('Check →',
                              style: TextStyle(
                                  fontSize: 10,
                                  color: AppColors.brandBlue,
                                  fontWeight: FontWeight.w700)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(name,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: AppColors.textPrimary,
                              height: 1.3)),
                    ],
                  ),
                ),
              );
            },
          ),
        ),
        const SizedBox(height: 16),
      ],
    );
  }
}

class _ReportButton extends ConsumerWidget {
  final String productId;
  final String productName;
  const _ReportButton(
      {required this.productId, required this.productName});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider);
    return SizedBox(
      width: double.infinity,
      child: OutlinedButton.icon(
        onPressed: () {
          if (user == null) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: const Text('Please log in to report an issue'),
                action: SnackBarAction(label: 'Log In', onPressed: () => context.push('/login')),
                duration: const Duration(seconds: 4),
              ),
            );
            return;
          }
          _showReportDialog(context);
        },
        icon: const Icon(Icons.flag_outlined, color: AppColors.gradeD, size: 18),
        label: const Text('Ingredients wrong? Report it',
            style: TextStyle(
                color: AppColors.gradeD,
                fontWeight: FontWeight.w700,
                fontSize: 13)),
        style: OutlinedButton.styleFrom(
          side: BorderSide(color: AppColors.gradeD.withOpacity(0.5)),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          padding: const EdgeInsets.symmetric(vertical: 14),
        ),
      ),
    );
  }

  void _showReportDialog(BuildContext context) {
    final ingredientsCtrl = TextEditingController();
    final reasonCtrl = TextEditingController();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Report Issue',
            style: TextStyle(
                fontWeight: FontWeight.w700,
                color: AppColors.textPrimary,
                fontFamily: 'Poppins')),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: ingredientsCtrl,
              decoration: const InputDecoration(
                  labelText: 'Incorrect ingredients',
                  hintText: 'List the ingredients that are wrong'),
              maxLines: 2,
            ),
            const SizedBox(height: 12),
            TextField(
              controller: reasonCtrl,
              decoration: const InputDecoration(
                  labelText: 'Reason',
                  hintText: 'Why do you think this is wrong?'),
              maxLines: 2,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.of(ctx).pop();
              try {
                await ApiClient.reportProduct(
                  productId: productId,
                  productName: productName,
                  reportedIngredients: ingredientsCtrl.text,
                  reason: reasonCtrl.text,
                );
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                        content:
                            Text('Report submitted. Thank you!')));
                }
              } catch (_) {
                if (context.mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                        content: Text(
                            'Failed to submit report. Try again.')));
                }
              }
            },
            style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.gradeD),
            child: const Text('Submit'),
          ),
        ],
      ),
    );
  }
}
