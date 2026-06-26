import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:go_router/go_router.dart';
import '../../core/models/product.dart';
import '../../core/theme/app_theme.dart';
import 'grade_badge.dart';

class ProductCard extends StatelessWidget {
  final Product product;
  const ProductCard({super.key, required this.product});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => context.push('/product/${product.staticKey ?? product.id}?name=${Uri.encodeComponent(product.name)}'),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: AppColors.border),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 2))],
        ),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              // Image
              Container(
                width: 56, height: 56,
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(10),
                ),
                clipBehavior: Clip.antiAlias,
                child: product.imageUrl != null
                    ? CachedNetworkImage(imageUrl: product.imageUrl!, fit: BoxFit.cover,
                        errorWidget: (_, __, ___) => const Icon(Icons.inventory_2_outlined, color: AppColors.textMuted))
                    : const Icon(Icons.inventory_2_outlined, color: AppColors.textMuted),
              ),
              const SizedBox(width: 12),
              // Name + brand
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(product.name, maxLines: 2, overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: AppColors.textPrimary)),
                    if (product.brand != null)
                      Text(product.brand!, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                    if (product.category != null)
                      Text(product.category!, style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              GradeBadge(grade: product.grade),
            ],
          ),
        ),
      ),
    );
  }
}
