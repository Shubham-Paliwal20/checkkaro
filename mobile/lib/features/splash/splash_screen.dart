import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
import '../../core/theme/app_theme.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _ctrl;
  late Animation<double> _fade;
  late Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 600));
    _fade  = CurvedAnimation(parent: _ctrl, curve: Curves.easeIn);
    _scale = Tween<double>(begin: 0.92, end: 1.0).animate(CurvedAnimation(parent: _ctrl, curve: Curves.easeOut));
    _ctrl.forward();
    ApiClient.ping();
    Future.delayed(const Duration(milliseconds: 1800), () {
      if (mounted) context.go('/');
    });
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: FadeTransition(
          opacity: _fade,
          child: ScaleTransition(
            scale: _scale,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      width: 48,
                      height: 48,
                      decoration: BoxDecoration(
                        color: Colors.white,
                        borderRadius: BorderRadius.circular(12),
                        boxShadow: [
                          BoxShadow(color: AppColors.brandOrange.withOpacity(0.22), blurRadius: 14, spreadRadius: 2),
                          BoxShadow(color: Colors.black.withOpacity(0.07), blurRadius: 8, offset: const Offset(0, 3)),
                        ],
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: Image.asset('assets/images/logo.png', fit: BoxFit.cover),
                      ),
                    ),
                    const SizedBox(width: 12),
                    const Text(
                      'Parkho',
                      style: TextStyle(
                        fontSize: 34,
                        fontWeight: FontWeight.w900,
                        color: AppColors.textPrimary,
                        fontFamily: 'Poppins',
                        letterSpacing: -1,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                const Text(
                  'Know what\'s inside your products',
                  style: TextStyle(fontSize: 13, color: AppColors.textMuted),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
