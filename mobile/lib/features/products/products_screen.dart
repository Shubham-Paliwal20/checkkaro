import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

const _catIcon = {
  'Skincare': '✨', 'Hair Care': '💆', 'Personal Care': '🧴',
  'Cosmetics': '💄', 'Food': '🍱', 'Snacks': '🍿',
  'Beverages': '🥤', 'Soft Drink': '🫧', 'Health Drink': '🥛',
  'Biscuits': '🍪', 'Chocolate': '🍫', 'Nutrition': '🥗',
  'Protein Supplement': '💪', 'Baby Care': '👶', 'Oral Care': '🦷',
  'Dairy': '🫙', 'Instant Noodles': '🍜', 'Spices': '🌶️',
  'Condiments': '🫙', 'Cooking Oil': '🫙', 'Breakfast Cereal': '🥣',
  'Energy Drink': '⚡', 'Sports Drink': '🏃', 'Confectionery': '🍬',
  'Bakery': '🥖', 'Ready to Eat': '🍽️', 'Fruit Drink': '🍹',
  'Fruit Juice': '🍊',
};

class ProductsScreen extends StatefulWidget {
  const ProductsScreen({super.key});

  @override
  State<ProductsScreen> createState() => _ProductsScreenState();
}

class _ProductsScreenState extends State<ProductsScreen> {
  // Data
  List<Map<String, dynamic>> _products = [];
  List<String> _categories = [];
  int _total = 0;
  int _pages = 1;

  // Filters
  String _query = '';
  String _category = '';
  String _brand = '';
  int _page = 1;
  String _sort = 'score';

  // UI state
  bool _loading = true;
  bool _slowLoad = false;
  String? _error;

  final _searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<void> _fetch() async {
    if (!mounted) return;
    setState(() { _loading = true; _error = null; _slowLoad = false; });

    for (int attempt = 0; attempt < 3; attempt++) {
      try {
        final data = await ApiClient.browseProducts(
          page: _page, limit: 24, sort: _sort,
          category: _category.isEmpty ? null : _category,
          brand:    _brand.isEmpty    ? null : _brand,
          q:        _query.isEmpty    ? null : _query,
        );
        if (!mounted) return;

        final prods = (data['products'] as List? ?? []).cast<Map<String, dynamic>>();
        setState(() {
          _products = prods;
          _total    = (data['total'] as num?)?.toInt() ?? 0;
          _pages    = (data['pages'] as num?)?.toInt() ?? 1;
          _loading  = false;
          _slowLoad = false;
          if ((data['categories'] as List?)?.isNotEmpty == true) {
            _categories = (data['categories'] as List).cast<String>();
          }
        });
        _fetchPhotos(prods);
        return;
      } catch (_) {
        if (attempt < 2) {
          // Show hint only on second retry
          if (attempt == 1 && mounted) setState(() => _slowLoad = true);
          await Future.delayed(const Duration(seconds: 8));
          if (!mounted) return;
        } else {
          if (!mounted) return;
          setState(() {
            _loading  = false;
            _slowLoad = false;
            _error    = 'Could not connect. Please check your internet and try again.';
          });
        }
      }
    }
  }

  Future<void> _fetchPhotos(List<Map<String, dynamic>> prods) async {
    // Send BOTH static_key and id for each product (deduplicated) — same logic as website
    final ids = <String>{};
    for (final p in prods) {
      final sk = p['static_key']?.toString();
      final id = p['id']?.toString();
      if (sk != null && sk.isNotEmpty) ids.add(sk);
      if (id != null && id.isNotEmpty) ids.add(id);
    }
    if (ids.isEmpty) return;
    final map = await ApiClient.batchPhotos(ids.toList());
    if (!mounted || map.isEmpty) return;
    setState(() {
      _products = _products.map((p) {
        // Check static_key first, then id — same order as website
        final sk  = p['static_key']?.toString() ?? '';
        final id  = p['id']?.toString() ?? '';
        final freshUrl = (sk.isNotEmpty ? map[sk] : null) ?? (id.isNotEmpty ? map[id] : null);
        if (freshUrl != null && freshUrl.isNotEmpty) return {...p, 'image_url': freshUrl};
        return p;
      }).toList();
    });
  }

  void _setCategory(String cat) {
    setState(() { _category = cat; _brand = ''; _page = 1; });
    _fetch();
  }

  void _setSort(String s) {
    setState(() { _sort = s; _page = 1; });
    _fetch();
  }

  void _clearFilters() {
    _searchCtrl.clear();
    setState(() { _query = ''; _category = ''; _brand = ''; _page = 1; _sort = 'score'; });
    _fetch();
  }

  void _submitSearch(String v) {
    setState(() { _query = v.trim(); _page = 1; });
    _fetch();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          // ── Header ──────────────────────────────────────────────────────────
          SliverToBoxAdapter(
            child: Container(
              color: Colors.white,
              padding: EdgeInsets.fromLTRB(16, MediaQuery.of(context).padding.top + 16, 16, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Product Directory',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.w900, color: AppColors.brandBlue, fontFamily: 'Poppins')),
                  const SizedBox(height: 2),
                  Text(
                    _loading ? 'Loading products…' : '$_total products${_category.isNotEmpty ? " in $_category" : ""}',
                    style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
                  ),
                  const SizedBox(height: 12),
                  // Search bar
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _searchCtrl,
                          textInputAction: TextInputAction.search,
                          onSubmitted: _submitSearch,
                          decoration: InputDecoration(
                            filled: true,
                            fillColor: AppColors.surface,
                            hintText: 'Search products or brands…',
                            hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
                            prefixIcon: const Icon(Icons.search, color: AppColors.textMuted, size: 20),
                            suffixIcon: _searchCtrl.text.isNotEmpty
                                ? IconButton(
                                    icon: const Icon(Icons.clear, size: 18),
                                    onPressed: () { _searchCtrl.clear(); _submitSearch(''); })
                                : null,
                            border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.border)),
                            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.border)),
                            focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.brandBlue, width: 1.5)),
                            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                          ),
                        ),
                      ),
                      const SizedBox(width: 8),
                      ElevatedButton(
                        onPressed: () => _submitSearch(_searchCtrl.text),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.brandBlue,
                          foregroundColor: Colors.white,
                          elevation: 0,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 13),
                        ),
                        child: const Text('Search', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13)),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),

          // ── Category pills ────────────────────────────────────────────────
          if (_categories.isNotEmpty)
            SliverToBoxAdapter(
              child: Container(
                color: Colors.white,
                padding: const EdgeInsets.fromLTRB(0, 0, 0, 12),
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    children: [
                      _CatPill(label: '🔍 All', selected: _category.isEmpty, onTap: () => _setCategory('')),
                      ...(_categories.map((cat) => _CatPill(
                            label: '${_catIcon[cat] ?? "📦"} $cat',
                            selected: _category == cat,
                            onTap: () => _setCategory(cat),
                          ))),
                    ],
                  ),
                ),
              ),
            ),

          // ── Sort bar + active filters ──────────────────────────────────────
          SliverToBoxAdapter(
            child: Container(
              color: Colors.white,
              padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
              child: Row(
                children: [
                  if (_category.isNotEmpty || _query.isNotEmpty)
                    GestureDetector(
                      onTap: _clearFilters,
                      child: Container(
                        margin: const EdgeInsets.only(right: 8),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: const Color(0xFFFEF2F2),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(color: const Color(0xFFFCA5A5)),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.close, size: 12, color: AppColors.gradeD),
                            SizedBox(width: 4),
                            Text('Clear', style: TextStyle(fontSize: 11, color: AppColors.gradeD, fontWeight: FontWeight.w600)),
                          ],
                        ),
                      ),
                    ),
                  const Spacer(),
                  // Sort chips
                  ...[('score', 'Best Grade'), ('name', 'A–Z'), ('brand', 'Brand')].map((opt) =>
                    GestureDetector(
                      onTap: () => _setSort(opt.$1),
                      child: Container(
                        margin: const EdgeInsets.only(left: 6),
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: _sort == opt.$1 ? AppColors.brandBlue : Colors.white,
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: _sort == opt.$1 ? AppColors.brandBlue : AppColors.border),
                        ),
                        child: Text(opt.$2,
                            style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w600,
                                color: _sort == opt.$1 ? Colors.white : AppColors.textMuted)),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),

          // ── Content ───────────────────────────────────────────────────────
          if (_loading)
            SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverGrid(
                delegate: SliverChildBuilderDelegate(
                  (_, i) => _SkeletonCard(),
                  childCount: 12,
                ),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2, childAspectRatio: 0.72,
                  crossAxisSpacing: 12, mainAxisSpacing: 12,
                ),
              ),
            )
          else if (_error != null)
            SliverToBoxAdapter(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.all(40),
                  child: Column(
                    children: [
                      const Text('😕', style: TextStyle(fontSize: 48)),
                      const SizedBox(height: 12),
                      const Text('Something went wrong', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
                      const SizedBox(height: 6),
                      Text(_error!, textAlign: TextAlign.center, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                      const SizedBox(height: 20),
                      ElevatedButton(
                        onPressed: _fetch,
                        style: ElevatedButton.styleFrom(backgroundColor: AppColors.brandBlue, foregroundColor: Colors.white),
                        child: const Text('Retry'),
                      ),
                    ],
                  ),
                ),
              ),
            )
          else if (_products.isEmpty)
            SliverToBoxAdapter(
              child: Center(
                child: Padding(
                  padding: const EdgeInsets.all(40),
                  child: Column(
                    children: [
                      const Text('🔍', style: TextStyle(fontSize: 48)),
                      const SizedBox(height: 12),
                      const Text('No products found', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
                      const SizedBox(height: 6),
                      const Text('Try a different filter or search term', style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
                      const SizedBox(height: 16),
                      TextButton(onPressed: _clearFilters, child: const Text('Clear all filters')),
                    ],
                  ),
                ),
              ),
            )
          else
            SliverPadding(
              padding: const EdgeInsets.fromLTRB(16, 4, 16, 8),
              sliver: SliverGrid(
                delegate: SliverChildBuilderDelegate(
                  (_, i) => _BrowseCard(product: _products[i]),
                  childCount: _products.length,
                ),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2, childAspectRatio: 0.72,
                  crossAxisSpacing: 12, mainAxisSpacing: 12,
                ),
              ),
            ),

          // ── Slow load hint ────────────────────────────────────────────────
          if (_slowLoad)
            SliverToBoxAdapter(
              child: Container(
                margin: const EdgeInsets.fromLTRB(16, 0, 16, 8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: const Color(0xFFFFFBEB), borderRadius: BorderRadius.circular(10), border: Border.all(color: const Color(0xFFFDE68A))),
                child: const Text('⏳ Loading products… this may take a moment on first visit.',
                    textAlign: TextAlign.center, style: TextStyle(fontSize: 12, color: Color(0xFF92400E))),
              ),
            ),

          // ── Pagination ────────────────────────────────────────────────────
          if (!_loading && _pages > 1)
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 32),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    _PageBtn(label: '← Prev', enabled: _page > 1, onTap: () { setState(() => _page--); _fetch(); }),
                    const SizedBox(width: 12),
                    Text('Page $_page of $_pages', style: const TextStyle(fontSize: 13, color: AppColors.textMuted)),
                    const SizedBox(width: 12),
                    _PageBtn(label: 'Next →', enabled: _page < _pages, onTap: () { setState(() => _page++); _fetch(); }),
                  ],
                ),
              ),
            ),

          const SliverToBoxAdapter(child: SizedBox(height: 20)),
        ],
      ),
    );
  }
}

// ── Sub-widgets ───────────────────────────────────────────────────────────────

class _CatPill extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;
  const _CatPill({required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(right: 8),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
        decoration: BoxDecoration(
          color: selected ? AppColors.brandBlue : Colors.white,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: selected ? AppColors.brandBlue : AppColors.border),
        ),
        child: Text(label,
            style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: selected ? Colors.white : const Color(0xFF374151))),
      ),
    );
  }
}

class _BrowseCard extends StatelessWidget {
  final Map<String, dynamic> product;
  const _BrowseCard({required this.product});

  Color _gradeColor(String? g) {
    switch (g) {
      case 'A': return AppColors.gradeA;
      case 'B': return AppColors.gradeB;
      case 'C': return AppColors.gradeC;
      default:  return AppColors.gradeD;
    }
  }

  Color _gradeBg(String? g) {
    switch (g) {
      case 'A': return AppColors.gradeBgA;
      case 'B': return AppColors.gradeBgB;
      case 'C': return AppColors.gradeBgC;
      default:  return AppColors.gradeBgD;
    }
  }

  @override
  Widget build(BuildContext context) {
    final name     = product['name']      as String? ?? '';
    final brand    = product['brand']     as String? ?? '';
    final category = product['category']  as String? ?? '';
    final grade    = product['grade']     as String? ?? 'C';
    final imageUrl = product['image_url'] as String?;
    final key      = (product['static_key'] ?? product['id'])?.toString() ?? '';

    return GestureDetector(
      onTap: () => context.push('/product/$key?name=${Uri.encodeComponent(name)}'),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2))],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image
            Expanded(
              child: ClipRRect(
                borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                child: Container(
                  width: double.infinity,
                  color: AppColors.surface,
                  child: imageUrl != null && imageUrl.isNotEmpty
                      ? CachedNetworkImage(
                          imageUrl: imageUrl,
                          fit: BoxFit.contain,
                          memCacheWidth: 300,
                          fadeInDuration: const Duration(milliseconds: 200),
                          httpHeaders: const {'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'},
                          placeholder: (_, __) => _ImageShimmer(),
                          errorWidget: (_, __, ___) => _NoImagePlaceholder(brand: brand, grade: grade, gradeColor: _gradeColor(grade)),
                        )
                      : _NoImagePlaceholder(brand: brand, grade: grade, gradeColor: _gradeColor(grade)),
                ),
              ),
            ),
            // Info
            Padding(
              padding: const EdgeInsets.fromLTRB(10, 8, 10, 4),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  if (brand.isNotEmpty)
                    Text(brand.toUpperCase(),
                        maxLines: 1, overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: AppColors.brandBlue, letterSpacing: 0.3)),
                  Text(name,
                      maxLines: 2, overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary, height: 1.3)),
                  const SizedBox(height: 6),
                  Row(
                    children: [
                      Expanded(
                        child: Text(category,
                            maxLines: 1, overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontSize: 10, color: AppColors.textMuted)),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                        decoration: BoxDecoration(
                          color: _gradeBg(grade),
                          borderRadius: BorderRadius.circular(10),
                          border: Border.all(color: _gradeColor(grade).withOpacity(0.4)),
                        ),
                        child: Text('Grade $grade',
                            style: TextStyle(fontSize: 10, fontWeight: FontWeight.w700, color: _gradeColor(grade))),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            // Button
            Padding(
              padding: const EdgeInsets.fromLTRB(10, 0, 10, 10),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(vertical: 7),
                decoration: BoxDecoration(
                  color: const Color(0xFFEFF4FF),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: const Center(
                  child: Text('Check Ingredients',
                      style: TextStyle(fontSize: 11, fontWeight: FontWeight.w700, color: AppColors.brandBlue)),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SkeletonCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(16), border: Border.all(color: AppColors.border)),
      child: Column(
        children: [
          Expanded(child: Container(color: const Color(0xFFF3F4F6))),
          Padding(
            padding: const EdgeInsets.all(10),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(height: 8, width: 60, decoration: BoxDecoration(color: const Color(0xFFF3F4F6), borderRadius: BorderRadius.circular(4))),
                const SizedBox(height: 6),
                Container(height: 12, width: double.infinity, decoration: BoxDecoration(color: const Color(0xFFF3F4F6), borderRadius: BorderRadius.circular(4))),
                const SizedBox(height: 4),
                Container(height: 12, width: 100, decoration: BoxDecoration(color: const Color(0xFFF3F4F6), borderRadius: BorderRadius.circular(4))),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ImageShimmer extends StatefulWidget {
  @override
  State<_ImageShimmer> createState() => _ImageShimmerState();
}

class _ImageShimmerState extends State<_ImageShimmer> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _anim;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 1000))..repeat(reverse: true);
    _anim = Tween<double>(begin: 0.3, end: 0.7).animate(_ctrl);
  }

  @override
  void dispose() { _ctrl.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) => AnimatedBuilder(
    animation: _anim,
    builder: (_, __) => Container(color: Color.lerp(const Color(0xFFF3F4F6), const Color(0xFFE5E7EB), _anim.value)),
  );
}

class _NoImagePlaceholder extends StatelessWidget {
  final String brand;
  final String grade;
  final Color gradeColor;
  const _NoImagePlaceholder({required this.brand, required this.grade, required this.gradeColor});

  @override
  Widget build(BuildContext context) {
    final initial = brand.isNotEmpty ? brand[0].toUpperCase() : '?';
    return Container(
      color: AppColors.surface,
      child: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 52, height: 52,
              decoration: BoxDecoration(
                color: gradeColor.withOpacity(0.12),
                shape: BoxShape.circle,
                border: Border.all(color: gradeColor.withOpacity(0.3), width: 1.5),
              ),
              child: Center(
                child: Text(initial,
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: gradeColor)),
              ),
            ),
            const SizedBox(height: 6),
            Text('No photo yet', style: TextStyle(fontSize: 9, color: AppColors.textMuted.withOpacity(0.7))),
          ],
        ),
      ),
    );
  }
}

class _PageBtn extends StatelessWidget {
  final String label;
  final bool enabled;
  final VoidCallback onTap;
  const _PageBtn({required this.label, required this.enabled, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: enabled ? onTap : null,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: enabled ? AppColors.brandBlue : AppColors.surface,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: enabled ? AppColors.brandBlue : AppColors.border),
        ),
        child: Text(label,
            style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: enabled ? Colors.white : AppColors.textMuted)),
      ),
    );
  }
}
