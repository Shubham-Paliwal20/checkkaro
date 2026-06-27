import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';
import 'onboarding_quiz_screen.dart';

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

  Future<void> _forgotPassword() async {
    final emailCtrl = TextEditingController(text: _emailCtrl.text.trim());
    await showDialog(
      context: context,
      builder: (ctx) => _ForgotPasswordDialog(emailCtrl: emailCtrl, dio: _dio),
    );
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
        final data        = res.data as Map;
        final user        = data['user'] as Map? ?? {};
        final accessToken = data['access_token']  as String? ?? '';
        final userId      = user['id']             as String? ?? '';
        ref.read(authProvider.notifier).setUser(
          accessToken:  accessToken,
          refreshToken: data['refresh_token'] as String? ?? '',
          email:        (user['email'] as String?) ?? email,
          id:           userId,
        );
        if (!mounted) return;
        setState(() => _loading = false);
        await _checkAndShowQuiz(userId, accessToken);
        if (mounted) context.pop();
      } else {
        await _dio.post(
          '$supabaseUrl/auth/v1/signup',
          data: {'email': email, 'password': password},
          options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
        );
        if (mounted) setState(() => _loading = false);
        _show('Account created! Check your email to confirm before logging in.', error: false);
      }
    } on DioException catch (e) {
      if (mounted) setState(() => _loading = false);
      final msg = (e.response?.data as Map?)?['error_description']
                ?? (e.response?.data as Map?)?['msg']
                ?? 'Login failed. Please check your credentials.';
      _show(msg.toString(), error: true);
    } catch (_) {
      if (mounted) setState(() => _loading = false);
      _show('Something went wrong. Please try again.', error: true);
    }
  }

  Future<void> _checkAndShowQuiz(String userId, String accessToken) async {
    if (userId.isEmpty || accessToken.isEmpty) return;
    try {
      final res = await _dio.get(
        '$supabaseUrl/rest/v1/user_profiles',
        queryParameters: {'id': 'eq.$userId', 'select': 'id,quiz_completed'},
        options: Options(headers: {'apikey': supabaseAnonKey, 'Authorization': 'Bearer $accessToken'}),
      );
      final data = res.data;
      final quizCompleted = data is List && data.isNotEmpty && data[0]['quiz_completed'] == true;
      if (!quizCompleted && mounted) {
        await Navigator.of(context).push(MaterialPageRoute(
          fullscreenDialog: true,
          builder: (_) => OnboardingQuizScreen(userId: userId, accessToken: accessToken),
        ));
      }
    } catch (_) {
      // On error, skip quiz silently
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

              if (_mode == _Mode.signIn) ...[
                const SizedBox(height: 8),
                Align(
                  alignment: Alignment.centerRight,
                  child: GestureDetector(
                    onTap: _forgotPassword,
                    child: const Text('Forgot password?',
                        style: TextStyle(fontSize: 13, color: AppColors.brandBlue, fontWeight: FontWeight.w600)),
                  ),
                ),
              ],
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

class _ForgotPasswordDialog extends StatefulWidget {
  final TextEditingController emailCtrl;
  final Dio dio;
  const _ForgotPasswordDialog({required this.emailCtrl, required this.dio});

  @override
  State<_ForgotPasswordDialog> createState() => _ForgotPasswordDialogState();
}

class _ForgotPasswordDialogState extends State<_ForgotPasswordDialog> {
  bool _loading = false;
  bool _sent = false;
  String? _error;

  Future<void> _send() async {
    final email = widget.emailCtrl.text.trim();
    if (email.isEmpty) {
      setState(() => _error = 'Please enter your email address.');
      return;
    }
    setState(() { _loading = true; _error = null; });
    try {
      await widget.dio.post(
        '$supabaseUrl/auth/v1/recover',
        data: {'email': email},
        options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
      );
      if (mounted) setState(() { _loading = false; _sent = true; });
    } catch (_) {
      if (mounted) setState(() { _loading = false; _error = 'Failed to send reset email. Please try again.'; });
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      title: const Text('Reset Password',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
      content: _sent
          ? Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.mark_email_read_outlined, size: 48, color: AppColors.gradeA),
                const SizedBox(height: 12),
                const Text(
                  'Password reset email sent!\nCheck your inbox and follow the link to set a new password.',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
                ),
              ],
            )
          : Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Enter your email and we\'ll send you a link to reset your password.',
                    style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
                const SizedBox(height: 16),
                TextField(
                  controller: widget.emailCtrl,
                  keyboardType: TextInputType.emailAddress,
                  autofocus: true,
                  decoration: InputDecoration(
                    hintText: 'you@example.com',
                    hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 14),
                    filled: true, fillColor: AppColors.surface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                    enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                    focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  ),
                ),
                if (_error != null) ...[
                  const SizedBox(height: 10),
                  Text(_error!, style: const TextStyle(fontSize: 12, color: AppColors.gradeD)),
                ],
              ],
            ),
      actions: _sent
          ? [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('Done', style: TextStyle(fontWeight: FontWeight.w700, color: AppColors.brandOrange)),
              ),
            ]
          : [
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text('Cancel', style: TextStyle(color: AppColors.textMuted)),
              ),
              ElevatedButton(
                onPressed: _loading ? null : _send,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.brandOrange,
                  foregroundColor: Colors.white,
                  elevation: 0,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                ),
                child: _loading
                    ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Text('Send Link', style: TextStyle(fontWeight: FontWeight.w700)),
              ),
            ],
    );
  }
}
