import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/theme/app_theme.dart';

class MainShell extends StatelessWidget {
  final Widget child;
  const MainShell({super.key, required this.child});

  int _selectedIndex(BuildContext context) {
    final loc = GoRouterState.of(context).uri.path;
    if (loc.startsWith('/search')) return 1;
    if (loc.startsWith('/scanner')) return 2;
    if (loc.startsWith('/check-ingredient')) return 3;
    if (loc.startsWith('/more') || loc.startsWith('/blog') || loc.startsWith('/about') || loc.startsWith('/contribute')) return 4;
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    final idx = _selectedIndex(context);
    return Scaffold(
      body: child,
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: idx,
        onTap: (i) {
          switch (i) {
            case 0:
              context.go('/');
              break;
            case 1:
              context.go('/search');
              break;
            case 2:
              context.go('/scanner');
              break;
            case 3:
              context.go('/check-ingredient');
              break;
            case 4:
              context.go('/more');
              break;
          }
        },
        items: const [
          BottomNavigationBarItem(
              icon: Icon(Icons.home_outlined),
              activeIcon: Icon(Icons.home),
              label: 'Home'),
          BottomNavigationBarItem(
              icon: Icon(Icons.search_outlined),
              activeIcon: Icon(Icons.search),
              label: 'Search'),
          BottomNavigationBarItem(
              icon: Icon(Icons.qr_code_scanner),
              activeIcon: Icon(Icons.qr_code_scanner),
              label: 'Scan'),
          BottomNavigationBarItem(
              icon: Icon(Icons.science_outlined),
              activeIcon: Icon(Icons.science),
              label: 'Ingredients'),
          BottomNavigationBarItem(
              icon: Icon(Icons.menu_book_outlined),
              activeIcon: Icon(Icons.menu_book),
              label: 'More'),
        ],
      ),
    );
  }
}
