import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/api/api_client.dart';
import '../../core/models/product.dart';
import '../../core/theme/app_theme.dart';
import '../../shared/widgets/product_card.dart';

final _searchProvider = FutureProvider.family<List<Product>, String>((ref, query) async {
  if (query.trim().isEmpty) return [];
  final results = await ApiClient.searchProducts(query.trim());
  return results.map(Product.fromJson).toList();
});

class SearchScreen extends ConsumerStatefulWidget {
  const SearchScreen({super.key});

  @override
  ConsumerState<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends ConsumerState<SearchScreen> {
  final _controller = TextEditingController();
  String _query = '';

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final results = _query.isNotEmpty ? ref.watch(_searchProvider(_query)) : null;

    return Scaffold(
      backgroundColor: AppColors.surface,
      appBar: AppBar(
        title: const Text('Search Products'),
        backgroundColor: Colors.white,
        elevation: 0,
      ),
      body: Column(
        children: [
          // Search input
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
            child: TextField(
              controller: _controller,
              autofocus: true,
              textInputAction: TextInputAction.search,
              decoration: InputDecoration(
                hintText: 'Search products, brands...',
                prefixIcon: const Icon(Icons.search, color: AppColors.textMuted),
                suffixIcon: _controller.text.isNotEmpty
                    ? IconButton(icon: const Icon(Icons.clear), onPressed: () { _controller.clear(); setState(() => _query = ''); })
                    : null,
              ),
              onChanged: (v) => setState(() => _query = v),
              onSubmitted: (v) => setState(() => _query = v),
            ),
          ),
          // Results
          Expanded(
            child: results == null
                ? const Center(child: Text('Type to search products', style: TextStyle(color: AppColors.textMuted)))
                : results.when(
                    loading: () => const Center(child: CircularProgressIndicator()),
                    error: (e, _) => Center(child: Text('Error: $e', style: const TextStyle(color: AppColors.gradeD))),
                    data: (products) => products.isEmpty
                        ? const Center(child: Text('No products found', style: TextStyle(color: AppColors.textMuted)))
                        : ListView.separated(
                            padding: const EdgeInsets.fromLTRB(16, 0, 16, 20),
                            itemCount: products.length,
                            separatorBuilder: (_, __) => const SizedBox(height: 10),
                            itemBuilder: (_, i) => ProductCard(product: products[i]),
                          ),
                  ),
          ),
        ],
      ),
    );
  }
}
