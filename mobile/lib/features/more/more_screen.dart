import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/app_theme.dart';

class MoreScreen extends StatelessWidget {
  const MoreScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            backgroundColor: Colors.white,
            surfaceTintColor: Colors.transparent,
            pinned: true,
            expandedHeight: 100,
            flexibleSpace: FlexibleSpaceBar(
              titlePadding: const EdgeInsets.fromLTRB(20, 0, 20, 16),
              title: const Text(
                'More',
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.w900,
                  color: AppColors.textPrimary,
                  fontFamily: 'Poppins',
                ),
              ),
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(20, 8, 20, 32),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _SectionHeader('Explore'),
                  const SizedBox(height: 10),
                  _MenuTile(
                    icon: Icons.article_outlined,
                    iconColor: AppColors.brandOrange,
                    iconBg: const Color(0xFFFFF7ED),
                    title: 'Blog',
                    subtitle: 'Read expert articles on food & cosmetics',
                    onTap: () => context.go('/blog'),
                  ),
                  _MenuTile(
                    icon: Icons.info_outline,
                    iconColor: AppColors.brandGreen,
                    iconBg: AppColors.brandGreenLight,
                    title: 'About Parkho',
                    subtitle: 'Our mission, data sources & how it works',
                    onTap: () => context.go('/about'),
                  ),
                  const SizedBox(height: 20),
                  _SectionHeader('Contribute'),
                  const SizedBox(height: 10),
                  _MenuTile(
                    icon: Icons.add_box_outlined,
                    iconColor: AppColors.brandOrange,
                    iconBg: const Color(0xFFFFF7ED),
                    title: 'Add a Product',
                    subtitle: 'Submit a product we don\'t have yet — earn ₹1',
                    onTap: () => context.go('/contribute'),
                  ),
                  _MenuTile(
                    icon: Icons.camera_alt_outlined,
                    iconColor: AppColors.brandBlue,
                    iconBg: const Color(0xFFEFF6FF),
                    title: 'Submit a Photo',
                    subtitle: 'Upload a clearer ingredient label photo',
                    onTap: () => context.go('/contribute'),
                  ),
                  _MenuTile(
                    icon: Icons.edit_note_outlined,
                    iconColor: AppColors.brandGreen,
                    iconBg: AppColors.brandGreenLight,
                    title: 'Write a Blog Post',
                    subtitle: 'Share your ingredient knowledge with others',
                    onTap: () => context.go('/contribute'),
                  ),
                  const SizedBox(height: 20),
                  _SectionHeader('Account'),
                  const SizedBox(height: 10),
                  _MenuTile(
                    icon: Icons.login_outlined,
                    iconColor: AppColors.textPrimary,
                    iconBg: AppColors.surface,
                    title: 'Login / Sign Up',
                    subtitle: 'Create an account to track your contributions',
                    onTap: () => context.push('/login'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String text;
  const _SectionHeader(this.text);

  @override
  Widget build(BuildContext context) {
    return Text(
      text.toUpperCase(),
      style: const TextStyle(
        fontSize: 11,
        fontWeight: FontWeight.w700,
        color: AppColors.textMuted,
        letterSpacing: 1.1,
      ),
    );
  }
}

class _MenuTile extends StatelessWidget {
  final IconData icon;
  final Color iconColor, iconBg;
  final String title, subtitle;
  final VoidCallback onTap;

  const _MenuTile({
    required this.icon, required this.iconColor, required this.iconBg,
    required this.title, required this.subtitle, required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(14),
          border: Border.all(color: AppColors.border),
          boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 6, offset: const Offset(0, 2))],
        ),
        child: Row(
          children: [
            Container(
              width: 44, height: 44,
              decoration: BoxDecoration(color: iconBg, borderRadius: BorderRadius.circular(10)),
              child: Icon(icon, color: iconColor, size: 22),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
                  const SizedBox(height: 2),
                  Text(subtitle, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, color: AppColors.textMuted, size: 20),
          ],
        ),
      ),
    );
  }
}
