import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/models/product.dart';
import '../../core/theme/app_theme.dart';

final _popularIngredientsProvider =
    FutureProvider<List<Map<String, dynamic>>>((ref) async {
  return ApiClient.getPopularIngredients();
});

class CheckIngredientScreen extends ConsumerStatefulWidget {
  final String? initialQuery;
  const CheckIngredientScreen({super.key, this.initialQuery});

  @override
  ConsumerState<CheckIngredientScreen> createState() =>
      _CheckIngredientScreenState();
}

class _CheckIngredientScreenState
    extends ConsumerState<CheckIngredientScreen> {
  late final TextEditingController _ctrl;
  bool _loading = false;
  IngredientDetail? _result;
  String? _error;
  bool _searched = false;

  @override
  void initState() {
    super.initState();
    _ctrl = TextEditingController(text: widget.initialQuery ?? '');
    if (widget.initialQuery != null && widget.initialQuery!.isNotEmpty) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _search(widget.initialQuery!);
      });
    }
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  Future<void> _search(String query) async {
    final q = query.trim();
    if (q.isEmpty) return;
    setState(() {
      _loading = true;
      _error = null;
      _result = null;
      _searched = true;
    });
    try {
      final data = await ApiClient.searchIngredient(q);
      setState(() {
        _loading = false;
        if (data != null) {
          _result = IngredientDetail.fromJson(data);
        } else {
          _error = 'Ingredient not found.';
        }
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _error = 'Failed to search. Please try again.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final popularAsync = ref.watch(_popularIngredientsProvider);

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          // Header
          SliverToBoxAdapter(
            child: Container(
              width: double.infinity,
              padding: EdgeInsets.fromLTRB(
                  20, MediaQuery.of(context).padding.top + 28, 20, 36),
              decoration: const BoxDecoration(
                color: AppColors.textPrimary,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: AppColors.brandGreen.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: AppColors.brandGreen.withOpacity(0.4)),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            const Icon(Icons.science, color: AppColors.brandGreen, size: 14),
                            const SizedBox(width: 5),
                            const Text('Ingredient Checker',
                                style: TextStyle(
                                    fontSize: 12, fontWeight: FontWeight.w700,
                                    color: AppColors.brandGreen, letterSpacing: 0.3)),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 14),
                  const Text('What does this\ningredient do?',
                      style: TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.w900,
                          color: Colors.white,
                          fontFamily: 'Poppins',
                          height: 1.2)),
                  const SizedBox(height: 10),
                  const Text('Type any ingredient name or E-number from a product label and get instant information.',
                      style: TextStyle(fontSize: 13, color: Color(0xFFD1D5DB), height: 1.5)),
                ],
              ),
            ),
          ),

          // White content area — search bar at top
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(16, 20, 16, 0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Search bar in white area
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _ctrl,
                          textInputAction: TextInputAction.search,
                          onSubmitted: _search,
                          style: const TextStyle(
                              fontSize: 15, color: AppColors.textPrimary),
                          decoration: InputDecoration(
                            filled: true,
                            fillColor: AppColors.surface,
                            hintText: 'e.g. Sodium Benzoate, TBHQ, E211...',
                            hintStyle: const TextStyle(
                                color: AppColors.textMuted, fontSize: 13),
                            prefixIcon: const Icon(Icons.search,
                                color: AppColors.textMuted, size: 20),
                            border: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                                borderSide: const BorderSide(
                                    color: AppColors.border)),
                            enabledBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                                borderSide: const BorderSide(
                                    color: AppColors.border)),
                            focusedBorder: OutlineInputBorder(
                                borderRadius: BorderRadius.circular(12),
                                borderSide: const BorderSide(
                                    color: AppColors.brandOrange, width: 1.5)),
                            contentPadding: const EdgeInsets.symmetric(
                                horizontal: 14, vertical: 14),
                          ),
                        ),
                      ),
                      const SizedBox(width: 10),
                      ElevatedButton(
                        onPressed: () => _search(_ctrl.text),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.brandOrange,
                          foregroundColor: Colors.white,
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12)),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 18, vertical: 14),
                        ),
                        child: const Text('Search',
                            style: TextStyle(fontWeight: FontWeight.w700)),
                      ),
                    ],
                  ),

                  const SizedBox(height: 20),

                  // Popular ingredients — Wrap (all visible, no scroll)
                  popularAsync.when(
                    loading: () => const SizedBox.shrink(),
                    error: (_, __) => const SizedBox.shrink(),
                    data: (items) => items.isEmpty
                        ? const SizedBox.shrink()
                        : _PopularChipsWrap(
                            items: items,
                            onTap: (name) {
                              _ctrl.text = name;
                              _search(name);
                            },
                          ),
                  ),

                  const SizedBox(height: 20),

                  if (_loading)
                    const Center(
                        child: Padding(
                      padding: EdgeInsets.only(top: 40),
                      child: CircularProgressIndicator(
                          color: AppColors.brandOrange),
                    )),
                  if (_error != null && !_loading)
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.only(top: 40),
                        child: Column(
                          children: [
                            const Icon(Icons.search_off,
                                size: 48, color: AppColors.textMuted),
                            const SizedBox(height: 12),
                            Text(_error!,
                                style: const TextStyle(
                                    color: AppColors.textMuted, fontSize: 14)),
                          ],
                        ),
                      ),
                    ),
                  if (_result != null && !_loading)
                    _IngredientResultCard(detail: _result!),
                  if (!_searched && !_loading)
                    const _EmptyState(),
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

class _EmptyState extends StatelessWidget {
  const _EmptyState();
  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 8),

        // Classification system section
        Container(
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppColors.border),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2))],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 30, height: 30,
                    decoration: BoxDecoration(color: AppColors.brandGreenLight, shape: BoxShape.circle),
                    child: const Icon(Icons.info_outline, color: AppColors.brandGreen, size: 18),
                  ),
                  const SizedBox(width: 10),
                  const Expanded(
                    child: Text('Understanding Our Classification System',
                        style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              const Text(
                'We classify ingredients into three categories based on scientific research from FSSAI, WHO, EU, FDA, and peer-reviewed studies:',
                style: TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.5),
              ),
              const SizedBox(height: 16),

              // Three cards
              _ClassCard(
                color: AppColors.gradeA,
                bg: AppColors.gradeBgA,
                borderColor: AppColors.gradeA,
                icon: Icons.check_circle,
                title: 'Generally Recognised',
                desc: 'Safe ingredients with no known adverse effects at normal consumption levels. Approved by major regulatory bodies without restrictions.',
                bullets: const ['Extensive safety data', 'No significant concerns', 'Widely approved globally'],
                bulletPrefix: '✓',
              ),
              const SizedBox(height: 10),
              _ClassCard(
                color: AppColors.gradeC,
                bg: AppColors.gradeBgC,
                borderColor: AppColors.gradeC,
                icon: Icons.warning_amber_rounded,
                title: 'Worth Knowing',
                desc: 'Ingredients with some concerns or restrictions. May cause issues in sensitive individuals or at high doses. Mixed scientific findings.',
                bullets: const ['Some restrictions apply', 'Sensitivity possible', 'Emerging research'],
                bulletPrefix: '⚠',
              ),
              const SizedBox(height: 10),
              _ClassCard(
                color: AppColors.gradeD,
                bg: AppColors.gradeBgD,
                borderColor: AppColors.gradeD,
                icon: Icons.cancel,
                title: 'Commonly Questioned',
                desc: 'Ingredients with significant health concerns backed by scientific research. May be restricted or banned in some countries.',
                bullets: const ['Significant concerns', 'Restricted/banned', 'Health risks identified'],
                bulletPrefix: '✕',
              ),

              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(10)),
                child: RichText(
                  text: const TextSpan(
                    style: TextStyle(fontSize: 12, color: AppColors.textMuted, height: 1.5, fontFamily: 'Poppins'),
                    children: [
                      TextSpan(text: 'Our Mission: ', style: TextStyle(fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
                      TextSpan(text: 'To provide transparent, science-based information about food and cosmetic ingredients so you can make informed choices for your health and well-being.'),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 32),
      ],
    );
  }
}

class _ClassCard extends StatelessWidget {
  final Color color, bg, borderColor;
  final IconData icon;
  final String title, desc;
  final List<String> bullets;
  final String bulletPrefix;

  const _ClassCard({
    required this.color, required this.bg, required this.borderColor,
    required this.icon, required this.title, required this.desc,
    required this.bullets, required this.bulletPrefix,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: borderColor.withOpacity(0.5)),
      ),
      child: Column(
        children: [
          Container(
            width: 44, height: 44,
            decoration: BoxDecoration(color: color, shape: BoxShape.circle),
            child: Icon(icon, color: Colors.white, size: 22),
          ),
          const SizedBox(height: 10),
          Text(title, textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: color, fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          Text(desc, textAlign: TextAlign.center,
              style: TextStyle(fontSize: 11, color: color.withOpacity(0.8), height: 1.5)),
          const Divider(height: 20),
          ...bullets.map((b) => Padding(
            padding: const EdgeInsets.only(bottom: 4),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('$bulletPrefix ', style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: color)),
                Text(b, style: TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: color)),
              ],
            ),
          )),
        ],
      ),
    );
  }
}

class _PopularChipsWrap extends StatelessWidget {
  final List<Map<String, dynamic>> items;
  final void Function(String) onTap;
  const _PopularChipsWrap({required this.items, required this.onTap});

  Color _chipColor(String cls) {
    switch (cls) {
      case 'commonly_questioned': return AppColors.gradeD;
      case 'worth_knowing':       return AppColors.gradeC;
      default:                    return AppColors.gradeA;
    }
  }

  Color _chipBg(String cls) {
    switch (cls) {
      case 'commonly_questioned': return AppColors.gradeBgD;
      case 'worth_knowing':       return AppColors.gradeBgC;
      default:                    return AppColors.gradeBgA;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Popular Ingredients to Check',
            style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w700,
                color: AppColors.textMuted,
                letterSpacing: 0.3)),
        const SizedBox(height: 10),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          children: items.map((item) {
            final name = (item['name'] ?? '') as String;
            final cls = (item['classification'] ?? 'generally_recognised') as String;
            final color = _chipColor(cls);
            final bg = _chipBg(cls);
            return GestureDetector(
              onTap: () => onTap(name),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                decoration: BoxDecoration(
                    color: bg,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: color.withOpacity(0.35))),
                child: Text(name,
                    style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: color)),
              ),
            );
          }).toList(),
        ),
      ],
    );
  }
}

class _IngredientResultCard extends StatelessWidget {
  final IngredientDetail detail;
  const _IngredientResultCard({required this.detail});

  Color get _classColor {
    if (detail.isQuestioned) return AppColors.gradeD;
    if (detail.isWorthKnowing) return AppColors.gradeC;
    return AppColors.gradeA;
  }

  Color get _classBg {
    if (detail.isQuestioned) return AppColors.gradeBgD;
    if (detail.isWorthKnowing) return AppColors.gradeBgC;
    return AppColors.gradeBgA;
  }

  String get _classLabel {
    switch (detail.classification) {
      case 'commonly_questioned': return 'Commonly Questioned';
      case 'worth_knowing':       return 'Worth Knowing';
      default:                    return 'Generally Recognised Safe';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Main card
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border(left: BorderSide(color: _classColor, width: 4)),
            boxShadow: [
              BoxShadow(
                  color: Colors.black.withOpacity(0.05),
                  blurRadius: 10,
                  offset: const Offset(0, 2))
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Text(detail.name,
                        style: const TextStyle(
                            fontSize: 20,
                            fontWeight: FontWeight.w800,
                            color: AppColors.textPrimary,
                            fontFamily: 'Poppins')),
                  ),
                  const SizedBox(width: 10),
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                        color: _classBg,
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: _classColor.withOpacity(0.4))),
                    child: Text(_classLabel,
                        style: TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w700,
                            color: _classColor)),
                  ),
                ],
              ),
              if (detail.whatItIs != null) ...[
                const SizedBox(height: 10),
                Text(detail.whatItIs!,
                    style: const TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w600,
                        color: AppColors.textPrimary)),
              ],
              if (detail.oneLineNote != null) ...[
                const SizedBox(height: 6),
                Text(detail.oneLineNote!,
                    style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textMuted,
                        height: 1.5)),
              ],
            ],
          ),
        ),
        const SizedBox(height: 12),

        // Health & Safety
        if (detail.healthEffects != null && detail.healthEffects!.isNotEmpty)
          _HealthCard(effects: detail.healthEffects!)
        else if (detail.classification == 'generally_recognised')
          _InfoBox(
            icon: Icons.check_circle_outline,
            iconColor: AppColors.gradeA,
            bg: AppColors.gradeBgA,
            borderColor: AppColors.gradeA,
            title: 'Health & Safety',
            body: 'No significant safety concerns at normal use levels. Approved by FSSAI, FDA, EU and WHO without restrictions.',
          )
        else
          _InfoBox(
            icon: Icons.health_and_safety_outlined,
            iconColor: _classColor,
            bg: _classBg,
            borderColor: _classColor,
            title: 'Health & Safety',
            body: detail.classification == 'worth_knowing'
                ? 'May cause reactions in sensitive individuals or at high doses.'
                : 'Linked to adverse health effects in studies. May be restricted or banned in some countries.',
          ),

        const SizedBox(height: 12),

        // Regulatory note
        if (detail.regulatoryNote != null) ...[
          _InfoBox(
            icon: Icons.policy_outlined,
            iconColor: AppColors.gradeB,
            bg: AppColors.gradeBgB,
            borderColor: AppColors.gradeB,
            title: 'Regulatory Note',
            body: detail.regulatoryNote!,
          ),
          const SizedBox(height: 12),
        ],

        // Commonly found in
        if (detail.commonlyFoundIn != null &&
            detail.commonlyFoundIn!.isNotEmpty) ...[
          _SectionCard(
            icon: Icons.shopping_bag_outlined,
            iconColor: AppColors.textMuted,
            title: 'Commonly Found In',
            child: Wrap(
              spacing: 8,
              runSpacing: 6,
              children: detail.commonlyFoundIn!
                  .split(',')
                  .map((s) => s.trim())
                  .where((s) => s.isNotEmpty)
                  .map((s) => Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                            color: AppColors.surface,
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: AppColors.border)),
                        child: Text(s,
                            style: const TextStyle(
                                fontSize: 12, color: AppColors.textMuted)),
                      ))
                  .toList(),
            ),
          ),
          const SizedBox(height: 12),
        ],

        // Countries restricted
        if (detail.countriesRestricted.isNotEmpty) ...[
          _SectionCard(
            icon: Icons.block_outlined,
            iconColor: AppColors.gradeD,
            title: 'Restricted or Banned In',
            child: Wrap(
              spacing: 8,
              runSpacing: 6,
              children: detail.countriesRestricted
                  .map((c) => Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                            color: AppColors.gradeBgD,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(
                                color: AppColors.gradeD.withOpacity(0.4))),
                        child: Text(c,
                            style: const TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.w600,
                                color: AppColors.gradeD)),
                      ))
                  .toList(),
            ),
          ),
          const SizedBox(height: 12),
        ],

        // FSSAI Position
        if (detail.fssaiPosition != null) ...[
          _InfoBox(
            icon: Icons.gavel_outlined,
            iconColor: AppColors.gradeC,
            bg: AppColors.gradeBgC,
            borderColor: AppColors.gradeC,
            title: 'FSSAI Position (India)',
            body: detail.fssaiPosition!,
          ),
          const SizedBox(height: 12),
        ],
      ],
    );
  }
}

class _InfoBox extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final Color bg;
  final Color borderColor;
  final String title;
  final String body;
  const _InfoBox({
    required this.icon,
    required this.iconColor,
    required this.bg,
    required this.borderColor,
    required this.title,
    required this.body,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: borderColor.withOpacity(0.3))),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: iconColor, size: 18),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title,
                    style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w700,
                        color: iconColor)),
                const SizedBox(height: 4),
                Text(body,
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

class _SectionCard extends StatelessWidget {
  final IconData icon;
  final Color iconColor;
  final String title;
  final Widget child;
  const _SectionCard(
      {required this.icon,
      required this.iconColor,
      required this.title,
      required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: iconColor, size: 16),
              const SizedBox(width: 8),
              Text(title,
                  style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary)),
            ],
          ),
          const SizedBox(height: 10),
          child,
        ],
      ),
    );
  }
}

class _HealthCard extends StatelessWidget {
  final Map<String, dynamic> effects;
  const _HealthCard({required this.effects});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppColors.border)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.health_and_safety_outlined,
                  color: AppColors.textPrimary, size: 16),
              SizedBox(width: 8),
              Text('Health & Safety',
                  style: TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                      color: AppColors.textPrimary)),
            ],
          ),
          const SizedBox(height: 10),
          if (effects['short_term'] != null)
            _EffectRow(
                label: 'Short-term',
                value: '${effects['short_term']}',
                color: AppColors.gradeC),
          if (effects['long_term'] != null) ...[
            const SizedBox(height: 8),
            _EffectRow(
                label: 'Long-term',
                value: '${effects['long_term']}',
                color: AppColors.gradeD),
          ],
          if (effects['vulnerable_groups'] != null) ...[
            const SizedBox(height: 8),
            _EffectRow(
                label: 'Vulnerable groups',
                value: '${effects['vulnerable_groups']}',
                color: AppColors.gradeB),
          ],
        ],
      ),
    );
  }
}

class _EffectRow extends StatelessWidget {
  final String label;
  final String value;
  final Color color;
  const _EffectRow(
      {required this.label, required this.value, required this.color});

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
            width: 8,
            height: 8,
            margin: const EdgeInsets.only(top: 4, right: 8),
            decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label,
                  style: TextStyle(
                      fontSize: 11, fontWeight: FontWeight.w700, color: color)),
              Text(value,
                  style: const TextStyle(
                      fontSize: 12, color: AppColors.textMuted, height: 1.4)),
            ],
          ),
        ),
      ],
    );
  }
}
