import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/app_theme.dart';

class MainShell extends StatelessWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  int _selectedIndex(BuildContext context) {
    final loc = GoRouterState.of(context).uri.path;
    if (loc.startsWith('/products') || loc.startsWith('/search')) return 1;
    if (loc.startsWith('/scanner')) return 2;
    if (loc.startsWith('/check-ingredient')) return 3;
    if (loc.startsWith('/more') || loc.startsWith('/blog') || loc.startsWith('/about') || loc.startsWith('/contribute')) return 4;
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    final idx = _selectedIndex(context);
    void onTap(int i) {
      switch (i) {
        case 0: context.go('/'); break;
        case 1: context.go('/products'); break;
        case 2: context.go('/scanner'); break;
        case 3: context.go('/check-ingredient'); break;
        case 4: context.go('/more'); break;
      }
    }

    final bottom = MediaQuery.of(context).padding.bottom;
    return Scaffold(
      body: child,
      bottomNavigationBar: Container(
        height: 68 + bottom,
        decoration: const BoxDecoration(
          color: Colors.white,
          boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 12, offset: Offset(0, -2))],
        ),
        child: Padding(
          padding: EdgeInsets.only(bottom: bottom),
          child: Row(
            children: [
              _NavItem(icon: Icons.home_outlined,     activeIcon: Icons.home,         label: 'Home',        selected: idx == 0, onTap: () => onTap(0)),
              _NavItem(icon: Icons.grid_view_outlined, activeIcon: Icons.grid_view,   label: 'Products',    selected: idx == 1, onTap: () => onTap(1)),
              _ScanButton(selected: idx == 2, onTap: () => onTap(2)),
              _NavItem(icon: Icons.science_outlined,  activeIcon: Icons.science,      label: 'Ingredients', selected: idx == 3, onTap: () => onTap(3)),
              _NavItem(icon: Icons.menu_book_outlined, activeIcon: Icons.menu_book,   label: 'More',        selected: idx == 4, onTap: () => onTap(4)),
            ],
          ),
        ),
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  final IconData icon, activeIcon;
  final String label;
  final bool selected;
  final VoidCallback onTap;
  const _NavItem({required this.icon, required this.activeIcon, required this.label, required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final color = selected ? AppColors.brandOrange : const Color(0xFF94a3b8);
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        behavior: HitTestBehavior.opaque,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(selected ? activeIcon : icon, color: color, size: 24),
            const SizedBox(height: 2),
            Text(label, style: TextStyle(fontSize: 10, color: color, fontWeight: selected ? FontWeight.w700 : FontWeight.w400)),
          ],
        ),
      ),
    );
  }
}

class _ScanButton extends StatelessWidget {
  final bool selected;
  final VoidCallback onTap;
  const _ScanButton({required this.selected, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        behavior: HitTestBehavior.opaque,
        child: SizedBox(
          height: 68,
          child: Center(
            child: Transform.translate(
              offset: const Offset(0, -10),
              child: Container(
                width: 64,
                height: 64,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  gradient: const LinearGradient(
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                    colors: [
                      AppColors.brandOrange,
                      Colors.white,
                      AppColors.brandGreen,
                    ],
                    stops: [0.0, 0.5, 1.0],
                  ),
                  border: Border.all(color: Colors.white, width: 3),
                  boxShadow: [
                    BoxShadow(color: AppColors.brandOrange.withOpacity(0.35), blurRadius: 10, offset: const Offset(0, -3)),
                    BoxShadow(color: AppColors.brandGreen.withOpacity(0.35),  blurRadius: 10, offset: const Offset(0, 4)),
                  ],
                ),
                child: Icon(
                  Icons.qr_code_scanner,
                  color: selected ? Colors.white : Colors.white.withOpacity(0.92),
                  size: 30,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
