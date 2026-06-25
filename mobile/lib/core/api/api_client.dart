import 'package:dio/dio.dart';

const _baseUrl = 'https://checkkaro.onrender.com';

class ApiClient {
  static final _dio = Dio(BaseOptions(
    baseUrl: _baseUrl,
    connectTimeout: const Duration(seconds: 20),
    receiveTimeout: const Duration(seconds: 30),
    headers: {'Content-Type': 'application/json'},
  ));

  static Dio get instance => _dio;

  static Future<List<Map<String, dynamic>>> searchProducts(String query) async {
    final res = await _dio.get('/api/product/browse', queryParameters: {'q': query, 'limit': 20});
    final data = res.data;
    if (data is Map && data['products'] is List) {
      return (data['products'] as List).cast<Map<String, dynamic>>();
    }
    return [];
  }

  static Future<Map<String, dynamic>?> getProductByName(String name) async {
    final res = await _dio.get('/api/product/search', queryParameters: {'name': name});
    return res.data as Map<String, dynamic>?;
  }

  static Future<Map<String, dynamic>?> getProductByBarcode(String barcode) async {
    final res = await _dio.get('/api/product/barcode/$barcode');
    return res.data as Map<String, dynamic>?;
  }

  static Future<Map<String, dynamic>?> searchIngredient(String name) async {
    final res = await _dio.get('/api/ingredient/search', queryParameters: {'name': name});
    return res.data as Map<String, dynamic>?;
  }

  static Future<List<Map<String, dynamic>>> getPopularIngredients() async {
    final res = await _dio.get('/api/ingredient/popular', queryParameters: {'limit': 16});
    final data = res.data;
    return data is List ? data.cast<Map<String, dynamic>>() : [];
  }

  static Future<List<Map<String, dynamic>>> getSaferAlternatives(
      String category, String name, String excludeId) async {
    final res = await _dio.get('/api/product/safer-alternatives', queryParameters: {
      'category': category,
      'name': name,
      'exclude_id': excludeId,
      'limit': 6,
    });
    final data = res.data;
    if (data is Map && data['alternatives'] is List) {
      return (data['alternatives'] as List).cast<Map<String, dynamic>>();
    }
    return [];
  }

  static Future<void> reportProduct({
    required String productId,
    required String productName,
    required String reportedIngredients,
    required String reason,
  }) async {
    await _dio.post('/api/admin-products/reports', data: {
      'product_id': productId,
      'product_name': productName,
      'reported_ingredients': reportedIngredients,
      'reason': reason,
    });
  }
}
