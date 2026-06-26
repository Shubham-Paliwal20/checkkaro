import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:url_launcher/url_launcher.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

enum _Mode { signIn, signUp }

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailCtrl    = TextEditingController();
  final _passwordCtrl = TextEditingController();
  _Mode   _mode    = _Mode.signIn;
  bool    _loading = false;
  String? _message;
  bool    _isError = false;

  final _dio = Dio(BaseOptions(connectTimeout: const Duration(seconds: 15)));

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final email    = _emailCtrl.text.trim();
    final password = _passwordCtrl.text;
    if (email.isEmpty)    return _show('Please enter your email.', error: true);
    if (password.isEmpty) return _show('Please enter a password.', error: true);

    setState(() { _loading = true; _message = null; });
    try {
      if (_mode == _Mode.signIn) {
        final res = await _dio.post(
          '$supabaseUrl/auth/v1/token?grant_type=password',
          data: {'email': email, 'password': password},
          options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
        );
        final user = (res.data as Map)['user'] as Map? ?? {};
        ref.read(authProvider.notifier).setUser(
          accessToken:  (res.data as Map)['access_token']  as String? ?? '',
          refreshToken: (res.data as Map)['refresh_token'] as String? ?? '',
          email:        (user['email'] as String?) ?? email,
          id:           (user['id']    as String?) ?? '',
        );
        if (mounted) context.pop();
      } else {
        await _dio.post(
          '$supabaseUrl/auth/v1/signup',
          data: {'email': email, 'password': password},
          options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
        );
        _show('Account created! Check your email to confirm before logging in.', error: false);
      }
    } on DioException catch (e) {
      final msg = (e.response?.data as Map?)?['error_description']
                ?? (e.response?.data as Map?)?['msg']
                ?? 'Login failed. Please check your credentials.';
      _show(msg.toString(), error: true);
    } catch (_) {
      _show('Something went wrong. Please try again.', error: true);
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _googleSignIn() async {
    final uri = Uri.parse(
      '$supabaseUrl/auth/v1/authorize?provider=google&redirect_to=https%3A%2F%2Fwww.parkho.in',
    );
    try {
      await launchUrl(uri, mode: LaunchMode.externalApplication);
    } catch (_) {
      _show('Could not open Google sign-in. Please try email login.', error: true);
    }
  }

  void _show(String msg, {required bool error}) {
    setState(() { _message = msg; _isError = error; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 16),
              Align(
                alignment: Alignment.centerLeft,
                child: GestureDetector(
                  onTap: () => context.pop(),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.arrow_back_ios, size: 16, color: AppColors.textMuted),
                      Text('Back', style: TextStyle(color: AppColors.textMuted, fontSize: 14)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 32),

              // Logo + app name
              Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: Image.asset('assets/images/logo.png', width: 44, height: 44, fit: BoxFit.cover),
                  ),
                  const SizedBox(width: 12),
                  const Text('Parkho',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: AppColors.textPrimary, fontFamily: 'Poppins')),
                ],
              ),
              const SizedBox(height: 24),

              Text(
                _mode == _Mode.signIn ? 'Welcome back' : 'Create an account',
                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins'),
              ),
              const SizedBox(height: 6),
              Text(
                _mode == _Mode.signIn
                    ? 'Log in to submit products and write reviews'
                    : 'Join to contribute and earn rewards',
                style: const TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
              ),
              const SizedBox(height: 28),

              // ── Google button ──────────────────────────────────────────────
              GestureDetector(
                onTap: _googleSignIn,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: const Color(0xFFD1D5DB), width: 1.5),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 4, offset: const Offset(0, 1))],
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // Google G icon
                      SizedBox(
                        width: 20, height: 20,
                        child: CustomPaint(painter: _GoogleIconPainter()),
                      ),
                      const SizedBox(width: 10),
                      const Text('Continue with Google',
                          style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // ── Divider ────────────────────────────────────────────────────
              const Row(children: [
                Expanded(child: Divider()),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: 12),
                  child: Text('or', style: TextStyle(color: AppColors.textMuted, fontSize: 12)),
                ),
                Expanded(child: Divider()),
              ]),
              const SizedBox(height: 20),

              // ── Email / Password ───────────────────────────────────────────
              const _Label('Email'),
              const SizedBox(height: 6),
              TextField(
                controller: _emailCtrl,
                keyboardType: TextInputType.emailAddress,
                textInputAction: TextInputAction.next,
                decoration: _inputDeco('you@example.com'),
              ),
              const SizedBox(height: 16),
              const _Label('Password'),
              const SizedBox(height: 6),
              TextField(
                controller: _passwordCtrl,
                obscureText: true,
                textInputAction: TextInputAction.done,
                onSubmitted: (_) => _submit(),
                decoration: _inputDeco('••••••••'),
              ),

              const SizedBox(height: 20),
              if (_message != null)
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: _isError ? const Color(0xFFFEF2F2) : const Color(0xFFF0FDF4),
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: _isError ? const Color(0xFFFCA5A5) : const Color(0xFF86EFAC)),
                  ),
                  child: Text(_message!, style: TextStyle(fontSize: 13, color: _isError ? const Color(0xFFDC2626) : const Color(0xFF15803D))),
                ),
              const SizedBox(height: 16),

              // ── Submit button ──────────────────────────────────────────────
              GestureDetector(
                onTap: _loading ? null : _submit,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 15),
                  decoration: BoxDecoration(
                    color: _loading ? AppColors.textMuted : AppColors.brandOrange,
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: _loading ? [] : [BoxShadow(color: AppColors.brandOrange.withOpacity(0.3), blurRadius: 8, offset: const Offset(0, 3))],
                  ),
                  alignment: Alignment.center,
                  child: _loading
                      ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5))
                      : Text(
                          _mode == _Mode.signIn ? 'Log In' : 'Create Account',
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15),
                        ),
                ),
              ),
              const SizedBox(height: 20),

              if (_mode == _Mode.signIn)
                _TextBtn("Don't have an account? Sign up", () => setState(() { _mode = _Mode.signUp; _message = null; })),
              if (_mode == _Mode.signUp)
                _TextBtn('Already have an account? Log in', () => setState(() { _mode = _Mode.signIn; _message = null; })),
            ],
          ),
        ),
      ),
    );
  }

  InputDecoration _inputDeco(String hint) => InputDecoration(
    hintText: hint,
    hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 14),
    filled: true, fillColor: AppColors.surface,
    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.border)),
    enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.border)),
    focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
  );
}

// Draws the Google "G" logo using canvas
class _GoogleIconPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()..style = PaintingStyle.fill;
    final cx = size.width / 2;
    final cy = size.height / 2;
    final r  = size.width / 2;

    // White circle background
    paint.color = Colors.white;
    canvas.drawCircle(Offset(cx, cy), r, paint);

    // Red arc (top + left)
    paint.color = const Color(0xFFEA4335);
    canvas.drawArc(Rect.fromCircle(center: Offset(cx, cy), radius: r * 0.85),
        -2.36, 2.09, true, paint);
    // Blue arc (right)
    paint.color = const Color(0xFF4285F4);
    canvas.drawArc(Rect.fromCircle(center: Offset(cx, cy), radius: r * 0.85),
        -0.27, 0.9, true, paint);
    // Green arc (bottom)
    paint.color = const Color(0xFF34A853);
    canvas.drawArc(Rect.fromCircle(center: Offset(cx, cy), radius: r * 0.85),
        0.63, 0.85, true, paint);
    // Yellow arc (bottom-left)
    paint.color = const Color(0xFFFBBC05);
    canvas.drawArc(Rect.fromCircle(center: Offset(cx, cy), radius: r * 0.85),
        1.48, 0.88, true, paint);
    // White inner circle to make ring
    paint.color = Colors.white;
    canvas.drawCircle(Offset(cx, cy), r * 0.5, paint);
    // Blue bar (horizontal right bar of G)
    paint.color = const Color(0xFF4285F4);
    canvas.drawRect(Rect.fromLTWH(cx, cy - r * 0.13, r * 0.85, r * 0.26), paint);
  }

  @override
  bool shouldRepaint(_GoogleIconPainter old) => false;
}

class _Label extends StatelessWidget {
  final String text;
  const _Label(this.text);
  @override
  Widget build(BuildContext context) =>
      Text(text, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.textPrimary));
}

class _TextBtn extends StatelessWidget {
  final String text;
  final VoidCallback onTap;
  const _TextBtn(this.text, this.onTap);
  @override
  Widget build(BuildContext context) => GestureDetector(
    onTap: onTap,
    child: Center(child: Text(text, style: const TextStyle(fontSize: 13, color: AppColors.brandBlue, fontWeight: FontWeight.w600))),
  );
}
