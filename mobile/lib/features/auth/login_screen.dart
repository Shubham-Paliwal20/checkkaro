import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

enum _Mode { signIn, signUp, magicLink }

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailCtrl    = TextEditingController();
  final _passwordCtrl = TextEditingController();
  _Mode  _mode    = _Mode.signIn;
  bool   _loading = false;
  String? _message;
  bool   _isError = false;

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
    if (email.isEmpty) return _show('Please enter your email.', error: true);
    if (_mode != _Mode.magicLink && password.isEmpty) return _show('Please enter a password.', error: true);

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
      } else if (_mode == _Mode.signUp) {
        await _dio.post(
          '$supabaseUrl/auth/v1/signup',
          data: {'email': email, 'password': password},
          options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
        );
        _show('Account created! Check your email to confirm before logging in.', error: false);
      } else {
        await _dio.post(
          '$supabaseUrl/auth/v1/otp',
          data: {'email': email, 'create_user': true},
          options: Options(headers: {'apikey': supabaseAnonKey, 'Content-Type': 'application/json'}),
        );
        _show('Magic link sent! Check your inbox.', error: false);
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
              Row(
                children: [
                  Container(
                    width: 44, height: 44,
                    decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(12)),
                    child: const Center(child: Text('P', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 24, fontFamily: 'Poppins'))),
                  ),
                  const SizedBox(width: 12),
                  const Text('Parkho', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: AppColors.textPrimary, fontFamily: 'Poppins')),
                ],
              ),
              const SizedBox(height: 24),
              Text(
                _mode == _Mode.signIn   ? 'Welcome back'           :
                _mode == _Mode.signUp   ? 'Create an account'      :
                                          'Sign in with email link',
                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins'),
              ),
              const SizedBox(height: 6),
              Text(
                _mode == _Mode.signIn   ? 'Log in to submit products and write reviews' :
                _mode == _Mode.signUp   ? 'Join to contribute and earn rewards'         :
                                          'We\'ll email you a one-click sign-in link',
                style: const TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5),
              ),
              const SizedBox(height: 28),
              const _Label('Email'),
              const SizedBox(height: 6),
              TextField(
                controller: _emailCtrl,
                keyboardType: TextInputType.emailAddress,
                textInputAction: _mode == _Mode.magicLink ? TextInputAction.done : TextInputAction.next,
                onSubmitted: _mode == _Mode.magicLink ? (_) => _submit() : null,
                decoration: _inputDeco('you@example.com'),
              ),
              if (_mode != _Mode.magicLink) ...[
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
                          _mode == _Mode.signIn   ? 'Log In'         :
                          _mode == _Mode.signUp   ? 'Create Account' :
                                                    'Send Magic Link',
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15),
                        ),
                ),
              ),
              const SizedBox(height: 24),
              const Row(children: [Expanded(child: Divider()), Padding(padding: EdgeInsets.symmetric(horizontal: 12), child: Text('or', style: TextStyle(color: AppColors.textMuted, fontSize: 12))), Expanded(child: Divider())]),
              const SizedBox(height: 18),
              if (_mode != _Mode.magicLink)
                _TextBtn('Sign in with magic link instead', () => setState(() { _mode = _Mode.magicLink; _message = null; })),
              if (_mode == _Mode.magicLink)
                _TextBtn('Sign in with password instead', () => setState(() { _mode = _Mode.signIn; _message = null; })),
              const SizedBox(height: 10),
              if (_mode == _Mode.signIn)
                _TextBtn('Don\'t have an account? Sign up', () => setState(() { _mode = _Mode.signUp; _message = null; })),
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
