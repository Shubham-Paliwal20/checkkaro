import 'package:dio/dio.dart';

const _baseUrl = 'https://checkkaro.onrender.com';

class ApiClient {
  static final _dio = Dio(BaseOptions(
    baseUrl: _baseUrl,
    connectTimeout: const Duration(seconds: 60),
    receiveTimeout: const Duration(seconds: 90),
    headers: {'Content-Type': 'application/json'},
  ));

  static Dio get instance => _dio;

  // Fire-and-forget warm-up call — called from splash so server is ready when user acts
  static void ping() {
    _dio.get('/api/product/browse', queryParameters: {'limit': 1}).ignore();
  }

  static Future<List<Map<String, dynamic>>> searchProducts(String query) async {
    final res = await _dio.get('/api/product/browse', queryParameters: {'q': query, 'limit': 20});
    final data = res.data;
    if (data is Map && data['products'] is List) {
      return (data['products'] as List).cast<Map<String, dynamic>>();
    }
    return [];
  }

  static Future<Map<String, dynamic>> browseProducts({
    int page = 1, int limit = 24, String sort = 'score',
    String? category, String? brand, String? q,
  }) async {
    final params = <String, dynamic>{'page': page, 'limit': limit, 'sort': sort};
    if (category != null && category.isNotEmpty) params['category'] = category;
    if (brand    != null && brand.isNotEmpty)    params['brand']    = brand;
    if (q        != null && q.isNotEmpty)        params['q']        = q;
    final res = await _dio.get('/api/product/browse', queryParameters: params);
    final data = res.data;
    if (data is Map<String, dynamic>) return data;
    return {};
  }

  static Future<Map<String, String>> batchPhotos(List<String> ids) async {
    if (ids.isEmpty) return {};
    try {
      final res = await _dio.post('/api/photos/batch', data: {'ids': ids});
      final photos = (res.data?['photos'] as List? ?? []);
      final map = <String, String>{};
      for (final ph in photos) {
        final id  = ph['product_id']?.toString() ?? '';
        final url = ph['image_url']?.toString()  ?? '';
        if (id.isNotEmpty && url.isNotEmpty) map[id] = url;
      }
      return map;
    } catch (_) {
      return {};
    }
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

  static Future<List<Map<String, dynamic>>> getReviews() async {
    try {
      final res = await _dio.get(
        'https://ecyuhdegovjhhqvasiez.supabase.co/rest/v1/reviews',
        queryParameters: {
          'is_approved': 'eq.true',
          'select': 'id,reviewer_name,review_text,rating',
          'order': 'created_at.desc',
          'limit': '20',
        },
        options: Options(headers: {
          'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjeXVoZGVnb3ZqaGhxdmFzaWV6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4OTI5MzIsImV4cCI6MjA5MTQ2ODkzMn0.Kqjqp0hvkRLAGuKCY1g202sUD74YD2wEixM8r0Ka5GA',
          'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVjeXVoZGVnb3ZqaGhxdmFzaWV6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4OTI5MzIsImV4cCI6MjA5MTQ2ODkzMn0.Kqjqp0hvkRLAGuKCY1g202sUD74YD2wEixM8r0Ka5GA',
        }),
      );
      final data = res.data;
      if (data is List) return data.cast<Map<String, dynamic>>();
      return [];
    } catch (_) {
      return [];
    }
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
