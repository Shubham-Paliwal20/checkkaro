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
          GestureDetector(
            onTap: () {
              if (ing.name.isEmpty) return;
              final router = GoRouter.of(context);
              showModalBottomSheet(
                context: context,
                isScrollControlled: true,
                backgroundColor: Colors.transparent,
                builder: (_) => _IngredientDetailSheet(name: ing.name, router: router),
              );
            },
            child: Row(
              children: [
                Expanded(
                  child: Text(ing.name,
                      style: TextStyle(fontSize: 13, fontWeight: FontWeight.w700, color: color)),
                ),
                Icon(Icons.info_outline, size: 14, color: color.withOpacity(0.6)),
              ],
            ),
          ),
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

// ── Ingredient detail bottom sheet ─────────────────────────────────────────

class _IngredientDetailSheet extends StatefulWidget {
  final String name;
  final GoRouter router;
  const _IngredientDetailSheet({required this.name, required this.router});

  @override
  State<_IngredientDetailSheet> createState() => _IngredientDetailSheetState();
}

class _IngredientDetailSheetState extends State<_IngredientDetailSheet> {
  bool _loading = true;
  IngredientDetail? _detail;
  bool _notFound = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final data = await ApiClient.searchIngredient(widget.name);
      if (!mounted) return;
      setState(() {
        _loading = false;
        if (data != null) {
          _detail = IngredientDetail.fromJson(data);
        } else {
          _notFound = true;
        }
      });
    } catch (_) {
      if (mounted) setState(() { _loading = false; _notFound = true; });
    }
  }

  Color get _color {
    final d = _detail;
    if (d == null) return AppColors.textMuted;
    if (d.isQuestioned) return AppColors.gradeD;
    if (d.isWorthKnowing) return AppColors.gradeC;
    return AppColors.gradeA;
  }

  Color get _bg {
    final d = _detail;
    if (d == null) return AppColors.surface;
    if (d.isQuestioned) return AppColors.gradeBgD;
    if (d.isWorthKnowing) return AppColors.gradeBgC;
    return AppColors.gradeBgA;
  }

  String get _label {
    switch (_detail?.classification) {
      case 'commonly_questioned': return 'Commonly Questioned';
      case 'worth_knowing':       return 'Worth Knowing';
      default:                    return 'Generally Recognised Safe';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      constraints: BoxConstraints(maxHeight: MediaQuery.of(context).size.height * 0.85),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const SizedBox(height: 12),
          Center(
            child: Container(
              width: 36, height: 4,
              decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)),
            ),
          ),
          const SizedBox(height: 16),
          Padding(
            padding: const EdgeInsets.fromLTRB(20, 0, 12, 12),
            child: Row(
              children: [
                Expanded(
                  child: Text(widget.name,
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800,
                          color: AppColors.textPrimary, fontFamily: 'Poppins')),
                ),
                IconButton(
                  icon: const Icon(Icons.close, size: 20, color: AppColors.textMuted),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          Flexible(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(20, 20, 20, 32),
              child: _loading
                  ? const Center(
                      child: Padding(
                        padding: EdgeInsets.symmetric(vertical: 60),
                        child: CircularProgressIndicator(color: AppColors.brandOrange),
                      ))
                  : _notFound
                      ? Padding(
                          padding: const EdgeInsets.symmetric(vertical: 40),
                          child: Column(
                            children: [
                              const Icon(Icons.search_off, size: 40, color: AppColors.textMuted),
                              const SizedBox(height: 12),
                              Text('No info found for "${widget.name}".',
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(color: AppColors.textMuted, fontSize: 14)),
                            ],
                          ),
                        )
                      : _buildContent(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildContent() {
    final d = _detail!;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(
            color: _bg,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: _color.withOpacity(0.4)),
          ),
          child: Text(_label,
              style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: _color)),
        ),
        if (d.whatItIs != null) ...[
          const SizedBox(height: 14),
          Text(d.whatItIs!,
              style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600,
                  color: AppColors.textPrimary, height: 1.4)),
        ],
        if (d.oneLineNote != null) ...[
          const SizedBox(height: 8),
          Text(d.oneLineNote!,
              style: const TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
        ],
        if (d.healthEffects != null && d.healthEffects!.isNotEmpty) ...[
          const SizedBox(height: 16),
          _SheetSection(
            title: 'Health & Safety',
            icon: Icons.health_and_safety_outlined,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (d.healthEffects!['short_term'] != null)
                  _SheetRow(label: 'Short-term',
                      value: '${d.healthEffects!['short_term']}', color: AppColors.gradeC),
                if (d.healthEffects!['long_term'] != null)
                  _SheetRow(label: 'Long-term',
                      value: '${d.healthEffects!['long_term']}', color: AppColors.gradeD),
                if (d.healthEffects!['vulnerable_groups'] != null)
                  _SheetRow(label: 'Vulnerable groups',
                      value: '${d.healthEffects!['vulnerable_groups']}', color: AppColors.gradeB),
              ],
            ),
          ),
        ],
        if (d.regulatoryNote != null) ...[
          const SizedBox(height: 12),
          _SheetSection(
            title: 'Regulatory Note',
            icon: Icons.policy_outlined,
            child: Text(d.regulatoryNote!,
                style: const TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
          ),
        ],
        if (d.countriesRestricted.isNotEmpty) ...[
          const SizedBox(height: 12),
          _SheetSection(
            title: 'Restricted / Banned In',
            icon: Icons.block_outlined,
            child: Wrap(
              spacing: 6, runSpacing: 6,
              children: d.countriesRestricted.map((c) => Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.gradeBgD,
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: AppColors.gradeD.withOpacity(0.4)),
                ),
                child: Text(c, style: const TextStyle(
                    fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.gradeD)),
              )).toList(),
            ),
          ),
        ],
        if (d.fssaiPosition != null) ...[
          const SizedBox(height: 12),
          _SheetSection(
            title: 'FSSAI Position (India)',
            icon: Icons.gavel_outlined,
            child: Text(d.fssaiPosition!,
                style: const TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
          ),
        ],
        const SizedBox(height: 20),
        GestureDetector(
          onTap: () {
            final encodedName = Uri.encodeComponent(d.name);
            Navigator.of(context).pop();
            widget.router.push('/check-ingredient/$encodedName');
          },
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 13),
            decoration: BoxDecoration(
              border: Border.all(color: AppColors.brandBlue),
              borderRadius: BorderRadius.circular(12),
            ),
            alignment: Alignment.center,
            child: const Text('View Full Ingredient Details →',
                style: TextStyle(color: AppColors.brandBlue,
                    fontWeight: FontWeight.w700, fontSize: 14)),
          ),
        ),
      ],
    );
  }
}

class _SheetSection extends StatelessWidget {
  final String title;
  final IconData icon;
  final Widget child;
  const _SheetSection({required this.title, required this.icon, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppColors.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 15, color: AppColors.textMuted),
              const SizedBox(width: 7),
              Text(title, style: const TextStyle(
                  fontSize: 13, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
            ],
          ),
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }
}

class _SheetRow extends StatelessWidget {
  final String label, value;
  final Color color;
  const _SheetRow({required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 7, height: 7,
            margin: const EdgeInsets.only(top: 5, right: 8),
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
          ),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(label, style: TextStyle(
                    fontSize: 11, fontWeight: FontWeight.w700, color: color)),
                Text(value, style: const TextStyle(
                    fontSize: 12, color: AppColors.textMuted, height: 1.4)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
