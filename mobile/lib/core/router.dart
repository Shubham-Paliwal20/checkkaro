import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../features/home/home_screen.dart';
import '../features/search/search_screen.dart';
import '../features/product/product_screen.dart';
import '../features/scanner/scanner_screen.dart';
import '../features/contribute/contribute_screen.dart';
import '../features/check_ingredient/check_ingredient_screen.dart';
import '../features/about/about_screen.dart';
import '../features/blog/blog_screen.dart';
import '../features/blog/blog_post_screen.dart';
import '../features/auth/login_screen.dart';
import '../features/more/more_screen.dart';
import '../features/products/products_screen.dart';
import '../features/splash/splash_screen.dart';
import '../shared/widgets/main_shell.dart';

final appRouter = GoRouter(
  initialLocation: '/splash',
  routes: [
    GoRoute(path: '/splash', builder: (c, s) => const SplashScreen()),

    ShellRoute(
      builder: (context, state, child) => MainShell(child: child),
      routes: [
        GoRoute(path: '/',                 builder: (c, s) => const HomeScreen()),
        GoRoute(path: '/search',           builder: (c, s) => const SearchScreen()),
        GoRoute(path: '/scanner',          builder: (c, s) => const ScannerScreen()),
        GoRoute(path: '/check-ingredient', builder: (c, s) => const CheckIngredientScreen()),
        GoRoute(
          path: '/check-ingredient/:name',
          builder: (c, s) => CheckIngredientScreen(initialQuery: s.pathParameters['name']),
        ),
        GoRoute(path: '/products',   builder: (c, s) => const ProductsScreen()),
        GoRoute(path: '/contribute', builder: (c, s) => const ContributeScreen()),
        GoRoute(path: '/about',      builder: (c, s) => const AboutScreen()),
        GoRoute(path: '/blog',       builder: (c, s) => const BlogScreen()),
        GoRoute(path: '/more',       builder: (c, s) => const MoreScreen()),
      ],
    ),

    // Full-screen routes (no bottom nav)
    GoRoute(
      path: '/product/:key',
      builder: (c, s) => ProductScreen(
        productKey: s.pathParameters['key']!,
        productName: s.uri.queryParameters['name'],
      ),
    ),
    GoRoute(
      path: '/blog/:slug',
      builder: (c, s) => BlogPostScreen(
        slug: s.pathParameters['slug']!,
        isDynamic: s.uri.queryParameters['dyn'] == '1',
      ),
    ),
    GoRoute(path: '/login', builder: (c, s) => const LoginScreen()),
  ],
);
