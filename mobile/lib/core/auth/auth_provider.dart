import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import '../config/app_config.dart';

// Auth tokens are stored in a Hive box named 'auth'.
// Keys: 'access_token', 'refresh_token', 'user_email', 'user_id'

Box get _authBox => Hive.box('auth');

class AuthNotifier extends Notifier<AuthUser?> {
  @override
  AuthUser? build() {
    final token = _authBox.get('access_token') as String?;
    final email = _authBox.get('user_email') as String?;
    final id    = _authBox.get('user_id')    as String?;
    if (token != null && email != null) return AuthUser(id: id ?? '', email: email, accessToken: token);
    return null;
  }

  void setUser({required String accessToken, required String refreshToken, required String email, required String id}) {
    _authBox.put('access_token',   accessToken);
    _authBox.put('refresh_token',  refreshToken);
    _authBox.put('user_email',     email);
    _authBox.put('user_id',        id);
    state = AuthUser(id: id, email: email, accessToken: accessToken);
  }

  // Exchanges the stored refresh token for a new access token.
  // Returns the fresh access token, or throws if refresh fails.
  Future<String> getFreshAccessToken() async {
    final refreshToken = _authBox.get('refresh_token') as String?;
    if (refreshToken == null) throw Exception('Not logged in');

    final res = await Dio().post(
      '$supabaseUrl/auth/v1/token?grant_type=refresh_token',
      data: {'refresh_token': refreshToken},
      options: Options(headers: {
        'apikey': supabaseAnonKey,
        'Content-Type': 'application/json',
      }),
    );

    final newAccess  = res.data['access_token']  as String;
    final newRefresh = res.data['refresh_token'] as String;
    final email      = res.data['user']['email'] as String;
    final id         = res.data['user']['id']    as String;
    setUser(accessToken: newAccess, refreshToken: newRefresh, email: email, id: id);
    return newAccess;
  }

  void signOut() {
    _authBox.deleteAll(['access_token', 'refresh_token', 'user_email', 'user_id']);
    state = null;
  }
}

class AuthUser {
  final String id, email, accessToken;
  const AuthUser({required this.id, required this.email, required this.accessToken});
}

final authProvider = NotifierProvider<AuthNotifier, AuthUser?>(() => AuthNotifier());
