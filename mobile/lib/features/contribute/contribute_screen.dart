import 'dart:io';
import 'dart:math';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _backendUrl = 'https://checkkaro.onrender.com';

const _productCategories = [
  'Food', 'Snacks', 'Biscuits', 'Chocolate', 'Confectionery', 'Bakery',
  'Instant Noodles', 'Ready to Eat', 'Dairy', 'Breakfast Cereal',
  'Beverages', 'Soft Drink', 'Energy Drink', 'Sports Drink', 'Health Drink',
  'Fruit Juice', 'Fruit Drink', 'Spices', 'Condiments', 'Cooking Oil',
  'Skincare', 'Hair Care', 'Personal Care', 'Cosmetics', 'Oral Care',
  'Baby Care', 'Nutrition', 'Protein Supplement',
];

class ContributeScreen extends ConsumerWidget {
  const ContributeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authProvider);

    return Scaffold(
      backgroundColor: AppColors.surface,
      body: CustomScrollView(
        slivers: [
          SliverToBoxAdapter(
            child: Container(
              padding: EdgeInsets.fromLTRB(20, MediaQuery.of(context).padding.top + 20, 20, 28),
              decoration: const BoxDecoration(
                gradient: LinearGradient(colors: [Color(0xFF0D1B2A), Color(0xFF1B3F8A)]),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Contribute', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w900, color: Colors.white, fontFamily: 'Poppins')),
                  const SizedBox(height: 6),
                  const Text('Help us build the most complete Indian product database',
                      style: TextStyle(fontSize: 13, color: Color(0xFFD1D5DB), height: 1.5)),
                  if (user != null) ...[
                    const SizedBox(height: 12),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      decoration: BoxDecoration(color: Colors.white.withOpacity(0.1), borderRadius: BorderRadius.circular(10)),
                      child: Row(
                        children: [
                          const Icon(Icons.account_circle_outlined, color: Colors.white, size: 16),
                          const SizedBox(width: 8),
                          Text('Logged in as ${user.email}', style: const TextStyle(color: Colors.white, fontSize: 12)),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),
          ),
          SliverPadding(
            padding: const EdgeInsets.all(16),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                if (user == null) _LoginPrompt(),
                const SizedBox(height: 4),
                _ContributeCard(
                  icon: Icons.add_box_outlined,
                  title: 'Submit a Product',
                  subtitle: 'Know a product we don\'t have? Add it to the database.',
                  color: AppColors.brandBlue,
                  onTap: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent,
                      builder: (_) => _SubmitProductSheet(userToken: user?.accessToken, userId: user?.id, userEmail: user?.email)),
                ),
                const SizedBox(height: 12),
                _ContributeCard(
                  icon: Icons.camera_alt_outlined,
                  title: 'Submit Product Photo',
                  subtitle: 'Upload a product label photo. Earn ₹1 per approved submission.',
                  color: AppColors.brandOrange,
                  onTap: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent,
                      builder: (_) => _PhotoSheet(userToken: user?.accessToken, userId: user?.id, userEmail: user?.email)),
                ),
                const SizedBox(height: 12),
                _ContributeCard(
                  icon: Icons.report_outlined,
                  title: 'Report Wrong Ingredients',
                  subtitle: 'Found incorrect ingredient info? Help us fix it.',
                  color: AppColors.gradeC,
                  onTap: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent,
                      builder: (_) => _ReportSheet(userToken: user?.accessToken)),
                ),
                const SizedBox(height: 12),
                _ContributeCard(
                  icon: Icons.article_outlined,
                  title: 'Write a Blog Post',
                  subtitle: 'Share your knowledge about ingredients and consumer awareness.',
                  color: AppColors.brandGreen,
                  onTap: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent,
                      builder: (_) => SizedBox(height: MediaQuery.of(context).size.height * 0.92,
                          child: _BlogSheet(userToken: user?.accessToken, userId: user?.id, userEmail: user?.email))),
                ),
                const SizedBox(height: 24),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: Colors.white, borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: AppColors.border),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Can\'t find a product?',
                          style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: AppColors.textPrimary)),
                      const SizedBox(height: 6),
                      const Text('Search first — if it\'s not there, use Submit a Product above.',
                          style: TextStyle(fontSize: 13, color: AppColors.textMuted)),
                      const SizedBox(height: 12),
                      ElevatedButton.icon(
                        onPressed: () => context.go('/search'),
                        icon: const Icon(Icons.search, size: 18),
                        label: const Text('Search Products'),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 32),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Login prompt ──────────────────────────────────────────────────────────────

class _LoginPrompt extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: const Color(0xFFFFF7ED), borderRadius: BorderRadius.circular(14),
        border: Border.all(color: const Color(0xFFFED7AA)),
      ),
      child: Row(
        children: [
          const Icon(Icons.info_outline, color: AppColors.brandOrange, size: 20),
          const SizedBox(width: 10),
          const Expanded(child: Text('Log in to submit contributions and earn rewards.', style: TextStyle(fontSize: 13, color: Color(0xFF92400E)))),
          GestureDetector(
            onTap: () => context.push('/login'),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(8)),
              child: const Text('Log In', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 12)),
            ),
          ),
        ],
      ),
    );
  }
}

// ── Card ──────────────────────────────────────────────────────────────────────

class _ContributeCard extends StatelessWidget {
  final IconData icon;
  final String title, subtitle;
  final Color color;
  final VoidCallback onTap;
  const _ContributeCard({required this.icon, required this.title, required this.subtitle, required this.color, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(14),
            border: Border.all(color: AppColors.border),
            boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.03), blurRadius: 6)]),
        child: Row(
          children: [
            Container(width: 44, height: 44,
                decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                child: Icon(icon, color: color, size: 22)),
            const SizedBox(width: 14),
            Expanded(child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: AppColors.textPrimary)),
                const SizedBox(height: 3),
                Text(subtitle, style: const TextStyle(fontSize: 12, color: AppColors.textMuted)),
              ],
            )),
            Icon(Icons.arrow_forward_ios, size: 14, color: AppColors.textMuted),
          ],
        ),
      ),
    );
  }
}

// ── Submit Product sheet ──────────────────────────────────────────────────────

class _SubmitProductSheet extends StatefulWidget {
  final String? userToken;
  final String? userId;
  final String? userEmail;
  const _SubmitProductSheet({this.userToken, this.userId, this.userEmail});

  @override
  State<_SubmitProductSheet> createState() => _SubmitProductSheetState();
}

class _SubmitProductSheetState extends State<_SubmitProductSheet> {
  final _name    = TextEditingController();
  final _upiId   = TextEditingController();
  final _ingreds = TextEditingController();
  String? _category;
  List<XFile> _images = [];
  bool    _loading = false;
  String? _msg;
  bool    _success = false;
  final _picker = ImagePicker();
  final _rng    = Random();

  Future<void> _pickImages() async {
    try {
      final picked = await _picker.pickMultiImage();
      if (picked.isEmpty) return;
      setState(() {
        final combined = [..._images, ...picked];
        _images = combined.length > 5 ? combined.sublist(0, 5) : combined;
      });
    } catch (e) {
      if (mounted) setState(() => _msg = 'Could not open gallery: ${e.toString()}');
    }
  }

  void _removeImage(int idx) => setState(() => _images.removeAt(idx));

  Future<String> _uploadImage(XFile file) async {
    final bytes = await file.readAsBytes();
    final ext   = file.name.split('.').last.toLowerCase();
    final mime  = ext == 'png' ? 'image/png' : 'image/jpeg';
    final ts    = DateTime.now().millisecondsSinceEpoch;
    final rand  = _rng.nextInt(9999).toString().padLeft(4, '0');
    final path  = 'new-submissions/${widget.userId ?? 'anon'}/${ts}_$rand.$ext';
    final dio   = Dio();
    await dio.put(
      '$supabaseUrl/storage/v1/object/product-images/$path',
      data: bytes,
      options: Options(
        headers: {
          'apikey': supabaseAnonKey,
          'Authorization': 'Bearer ${widget.userToken}',
          'Content-Type': mime,
        },
      ),
    );
    return '$supabaseUrl/storage/v1/object/public/product-images/$path';
  }

  Future<void> _submit() async {
    final name = _name.text.trim();
    final upi  = _upiId.text.trim();
    if (name.isEmpty)        { setState(() => _msg = 'Product name is required.'); return; }
    if (_category == null)   { setState(() => _msg = 'Please select a category.'); return; }
    if (_images.length < 2)  { setState(() => _msg = 'Please upload at least 2 photos (front + back of label).'); return; }
    if (upi.isEmpty)         { setState(() => _msg = 'UPI ID is required.'); return; }

    setState(() { _loading = true; _msg = null; });
    try {
      final urls = <String>[];
      for (final img in _images) {
        urls.add(await _uploadImage(img));
      }
      final dio = Dio();
      await dio.post(
        '$supabaseUrl/rest/v1/product_submissions',
        data: {
          'product_name_searched': name,
          'images': urls,
          'contact': upi,
          'email': widget.userEmail ?? '',
          'ingredients_raw': _ingreds.text.trim().isEmpty ? null : _ingreds.text.trim(),
          'user_id': widget.userId,
          'status': 'pending',
        },
        options: Options(headers: {
          'apikey': supabaseAnonKey,
          'Authorization': 'Bearer ${widget.userToken}',
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal',
        }),
      );
      setState(() { _success = true; _msg = 'Submitted! You will earn ₹1 after admin approves your product.'; });
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['message']?.toString() ?? 'Submission failed. Please try again.');
    } catch (e) {
      setState(() => _msg = 'Submission failed: ${e.toString()}');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      padding: EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: [
            Center(child: Container(width: 36, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            const Text('📦 Submit a Product',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
            const SizedBox(height: 4),
            const Text('Earn ₹1 after admin approves your submission.',
                style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
            const SizedBox(height: 16),
            if (!_success) ...[
              // Product name
              _fieldLabel('Product name *'),
              const SizedBox(height: 5),
              _textField(_name, 'e.g. Maggi 2-Minute Noodles Masala'),
              const SizedBox(height: 12),

              // Category dropdown
              _fieldLabel('Category *'),
              const SizedBox(height: 5),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: AppColors.border),
                ),
                child: DropdownButtonHideUnderline(
                  child: DropdownButton<String>(
                    value: _category,
                    hint: const Text('Select category', style: TextStyle(color: AppColors.textMuted, fontSize: 13)),
                    isExpanded: true,
                    items: _productCategories.map((c) => DropdownMenuItem(value: c, child: Text(c, style: const TextStyle(fontSize: 14)))).toList(),
                    onChanged: (v) => setState(() => _category = v),
                  ),
                ),
              ),
              const SizedBox(height: 12),

              // Image picker
              _fieldLabel('Product photos * (min 2, max 5)'),
              const SizedBox(height: 4),
              const Text('Upload front + back of label clearly. Required.',
                  style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
              const SizedBox(height: 8),
              if (_images.isNotEmpty)
                SizedBox(
                  height: 90,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: _images.length,
                    itemBuilder: (_, i) => Stack(
                      children: [
                        Container(
                          width: 80, height: 80,
                          margin: const EdgeInsets.only(right: 8),
                          decoration: BoxDecoration(borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(10),
                            child: Image.file(File(_images[i].path), fit: BoxFit.cover),
                          ),
                        ),
                        Positioned(
                          top: 0, right: 4,
                          child: GestureDetector(
                            onTap: () => _removeImage(i),
                            child: Container(
                              width: 20, height: 20,
                              decoration: const BoxDecoration(color: Color(0xFFDC2626), shape: BoxShape.circle),
                              child: const Icon(Icons.close, size: 12, color: Colors.white),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              if (_images.length < 5)
                GestureDetector(
                  onTap: _pickImages,
                  child: Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(10),
                      border: Border.all(color: AppColors.border, style: BorderStyle.solid),
                    ),
                    child: Column(
                      children: [
                        Icon(Icons.add_photo_alternate_outlined, color: AppColors.brandBlue, size: 28),
                        const SizedBox(height: 4),
                        Text(
                          _images.isEmpty ? 'Add photos from gallery' : 'Add more photos (${_images.length}/5)',
                          style: const TextStyle(color: AppColors.brandBlue, fontSize: 13, fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
                  ),
                ),
              const SizedBox(height: 12),

              // UPI ID
              _fieldLabel('UPI ID *'),
              const SizedBox(height: 5),
              _textField(_upiId, 'e.g. name@upi or 9876543210@paytm'),
              const SizedBox(height: 12),

              // Ingredients (optional)
              _fieldLabel('Ingredients from label (optional)'),
              const SizedBox(height: 5),
              _textField(_ingreds, 'Paste ingredients from the label...', maxLines: 4),
              const SizedBox(height: 16),

              if (_msg != null)
                Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: const Color(0xFFFEF2F2), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFFCA5A5))),
                  child: Text(_msg!, style: const TextStyle(fontSize: 12, color: Color(0xFFDC2626))),
                ),
              GestureDetector(
                onTap: _loading ? null : _submit,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(
                    color: _loading ? AppColors.textMuted : AppColors.brandOrange,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  alignment: Alignment.center,
                  child: _loading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text('Submit', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ] else ...[
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: const Color(0xFFF0FDF4), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF86EFAC))),
                child: Row(
                  children: [
                    const Icon(Icons.check_circle, color: Color(0xFF16a34a), size: 24),
                    const SizedBox(width: 12),
                    Expanded(child: Text(_msg ?? 'Done!', style: const TextStyle(fontSize: 13, color: Color(0xFF15803D)))),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => Navigator.pop(context),
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: AppColors.textPrimary, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: const Text('Done', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _textField(TextEditingController ctrl, String hint, {int maxLines = 1}) =>
      TextField(
        controller: ctrl,
        maxLines: maxLines,
        style: const TextStyle(fontSize: 14),
        decoration: InputDecoration(
          hintText: hint,
          hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
          filled: true, fillColor: AppColors.surface,
          contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
        ),
      );
}

Widget _fieldLabel(String label) => Text(label,
    style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary));

// ── Photo sheet ───────────────────────────────────────────────────────────────

class _PhotoSheet extends StatefulWidget {
  final String? userToken;
  final String? userId;
  final String? userEmail;
  const _PhotoSheet({this.userToken, this.userId, this.userEmail});

  @override
  State<_PhotoSheet> createState() => _PhotoSheetState();
}

class _PhotoSheetState extends State<_PhotoSheet> {
  final _productName = TextEditingController();
  final _upiId       = TextEditingController();
  List<XFile> _images = [];
  bool    _loading = false;
  String? _msg;
  bool    _success = false;
  final _picker = ImagePicker();

  Future<void> _pickImages() async {
    try {
      final picked = await _picker.pickMultiImage();
      if (picked.isEmpty) return;
      setState(() {
        final combined = [..._images, ...picked];
        _images = combined.length > 5 ? combined.sublist(0, 5) : combined;
      });
    } catch (e) {
      if (mounted) setState(() => _msg = 'Could not open gallery: ${e.toString()}');
    }
  }

  void _removeImage(int idx) => setState(() => _images.removeAt(idx));

  Future<void> _submit() async {
    final name = _productName.text.trim();
    final upi  = _upiId.text.trim();
    if (name.isEmpty)       { setState(() => _msg = 'Product name is required.'); return; }
    if (_images.length < 2) { setState(() => _msg = 'Please upload at least 2 photos (front + back).'); return; }
    if (upi.isEmpty)        { setState(() => _msg = 'UPI ID is required.'); return; }

    final productId = name.toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '-').replaceAll(RegExp(r'^-|-$'), '');

    setState(() { _loading = true; _msg = null; });
    try {
      final formData = FormData();
      formData.fields.add(MapEntry('product_id', productId));
      formData.fields.add(MapEntry('product_name', name));
      formData.fields.add(MapEntry('upi_or_mobile', upi));
      for (final img in _images) {
        final bytes = await img.readAsBytes();
        final ext   = img.name.split('.').last.toLowerCase();
        final mime  = ext == 'png' ? 'image/png' : 'image/jpeg';
        formData.files.add(MapEntry('files',
            MultipartFile.fromBytes(bytes, filename: img.name, contentType: DioMediaType.parse(mime))));
      }
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/photos/submit',
        data: formData,
        options: Options(headers: {if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}'}),
      );
      setState(() { _success = true; _msg = 'Photos submitted! You\'ll earn ₹1 when approved.'; });
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['detail']?.toString() ?? 'Submission failed.');
    } catch (e) {
      setState(() => _msg = 'Submission failed: ${e.toString()}');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      padding: EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: [
            Center(child: Container(width: 36, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            const Text('📷 Submit Product Photo', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
            const SizedBox(height: 4),
            const Text('For products already in our database. Earn ₹1 per approved photo.', style: TextStyle(fontSize: 12, color: AppColors.textMuted)),
            const SizedBox(height: 16),
            if (!_success) ...[
              _fieldLabel('Product name *'),
              const SizedBox(height: 5),
              _tf(_productName, 'e.g. Dove Beauty Bar'),
              const SizedBox(height: 12),
              _fieldLabel('Photos * (min 2, max 5 — front + back of label)'),
              const SizedBox(height: 8),
              if (_images.isNotEmpty)
                SizedBox(
                  height: 90,
                  child: ListView.builder(
                    scrollDirection: Axis.horizontal,
                    itemCount: _images.length,
                    itemBuilder: (_, i) => Stack(
                      children: [
                        Container(width: 80, height: 80, margin: const EdgeInsets.only(right: 8),
                            decoration: BoxDecoration(borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
                            child: ClipRRect(borderRadius: BorderRadius.circular(10), child: Image.file(File(_images[i].path), fit: BoxFit.cover))),
                        Positioned(top: 0, right: 4,
                            child: GestureDetector(onTap: () => _removeImage(i),
                                child: Container(width: 20, height: 20, decoration: const BoxDecoration(color: Color(0xFFDC2626), shape: BoxShape.circle),
                                    child: const Icon(Icons.close, size: 12, color: Colors.white)))),
                      ],
                    ),
                  ),
                ),
              if (_images.length < 5)
                GestureDetector(
                  onTap: _pickImages,
                  child: Container(
                    margin: const EdgeInsets.only(top: 8),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
                    child: Column(children: [
                      const Icon(Icons.add_photo_alternate_outlined, color: AppColors.brandOrange, size: 28),
                      const SizedBox(height: 4),
                      Text(_images.isEmpty ? 'Add photos from gallery' : 'Add more (${_images.length}/5)',
                          style: const TextStyle(color: AppColors.brandOrange, fontSize: 13, fontWeight: FontWeight.w600)),
                    ]),
                  ),
                ),
              const SizedBox(height: 12),
              _fieldLabel('UPI ID *'),
              const SizedBox(height: 5),
              _tf(_upiId, 'e.g. name@upi or 9876543210@paytm'),
              const SizedBox(height: 16),
              if (_msg != null)
                Container(margin: const EdgeInsets.only(bottom: 8), padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(color: const Color(0xFFFEF2F2), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFFCA5A5))),
                    child: Text(_msg!, style: const TextStyle(fontSize: 12, color: Color(0xFFDC2626)))),
              GestureDetector(
                onTap: _loading ? null : _submit,
                child: Container(padding: const EdgeInsets.symmetric(vertical: 14),
                    decoration: BoxDecoration(color: _loading ? AppColors.textMuted : AppColors.brandOrange, borderRadius: BorderRadius.circular(12)),
                    alignment: Alignment.center,
                    child: _loading ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                        : const Text('Submit', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15))),
              ),
            ] else ...[
              Container(padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(color: const Color(0xFFF0FDF4), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF86EFAC))),
                  child: Row(children: [
                    const Icon(Icons.check_circle, color: Color(0xFF16a34a), size: 24),
                    const SizedBox(width: 12),
                    Expanded(child: Text(_msg ?? 'Done!', style: const TextStyle(fontSize: 13, color: Color(0xFF15803D)))),
                  ])),
              const SizedBox(height: 16),
              GestureDetector(onTap: () => Navigator.pop(context),
                  child: Container(padding: const EdgeInsets.symmetric(vertical: 14),
                      decoration: BoxDecoration(color: AppColors.textPrimary, borderRadius: BorderRadius.circular(12)),
                      alignment: Alignment.center,
                      child: const Text('Done', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)))),
            ],
          ],
        ),
      ),
    );
  }

  Widget _tf(TextEditingController ctrl, String hint) => TextField(
    controller: ctrl, style: const TextStyle(fontSize: 14),
    decoration: InputDecoration(hintText: hint, hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
        filled: true, fillColor: AppColors.surface, contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5))),
  );
}

// ── Report sheet ──────────────────────────────────────────────────────────────

class _ReportSheet extends StatefulWidget {
  final String? userToken;
  const _ReportSheet({this.userToken});

  @override
  State<_ReportSheet> createState() => _ReportSheetState();
}

class _ReportSheetState extends State<_ReportSheet> {
  final _product = TextEditingController();
  final _ingredients = TextEditingController();
  final _reason      = TextEditingController();
  bool  _loading = false;
  String? _msg;
  bool  _success = false;

  String _slugify(String name) => name.trim().toLowerCase()
      .replaceAll(RegExp(r'[^a-z0-9]+'), '-')
      .replaceAll(RegExp(r'^-|-$'), '');

  Future<void> _submit() async {
    if (_product.text.trim().isEmpty || _ingredients.text.trim().isEmpty) {
      setState(() => _msg = 'Product name and reported ingredients are required.');
      return;
    }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/admin-products/reports',
        data: {
          'product_id':            _slugify(_product.text),
          'product_name':          _product.text.trim(),
          'reported_ingredients':  _ingredients.text.trim(),
          'reason':                _reason.text.trim().isEmpty ? null : _reason.text.trim(),
        },
        options: Options(headers: {
          if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}',
          'Content-Type': 'application/json',
        }),
      );
      setState(() { _success = true; _msg = 'Report submitted! Thank you for helping us improve.'; });
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['detail']?.toString() ?? 'Submission failed.');
    } catch (_) {
      setState(() => _msg = 'Submission failed. Please try again.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return _Sheet(
      title: '🚩 Report Wrong Ingredients',
      loading: _loading, msg: _msg, success: _success, onSubmit: _submit,
      fields: [
        _Field('Product name *', _product, 'e.g. Kurkure Masala Munch'),
        _Field('Reported ingredients *', _ingredients, 'Paste the correct ingredients from the label...', maxLines: 4),
        _Field('Reason (optional)', _reason, 'e.g. Missing palm oil, wrong allergen info...'),
      ],
    );
  }
}

// ── Blog sheet ────────────────────────────────────────────────────────────────

const _blogCategories = ['Food', 'Cosmetics', 'Health', 'Lifestyle', 'Product Review'];

class _BlogSheet extends StatefulWidget {
  final String? userToken;
  final String? userId;
  final String? userEmail;
  const _BlogSheet({this.userToken, this.userId, this.userEmail});

  @override
  State<_BlogSheet> createState() => _BlogSheetState();
}

class _BlogSheetState extends State<_BlogSheet> {
  final _title       = TextEditingController();
  final _authorName  = TextEditingController();
  final _authorBio   = TextEditingController();
  final _coverUrl    = TextEditingController();
  final _content     = TextEditingController();
  String _category   = 'Food';
  bool   _loading    = false;
  String? _msg;
  bool   _success    = false;

  @override
  void initState() {
    super.initState();
    _authorName.text = widget.userEmail?.split('@')[0] ?? '';
  }

  int get _wordCount => _content.text.trim().isEmpty ? 0
      : _content.text.trim().split(RegExp(r'\s+')).where((w) => w.isNotEmpty).length;

  String _slugify(String t) {
    final base = t.trim().toLowerCase().replaceAll(RegExp(r'[^a-z0-9]+'), '-').replaceAll(RegExp(r'^-|-$'), '');
    return '$base-${DateTime.now().millisecondsSinceEpoch}';
  }

  Future<void> _submit() async {
    final title = _title.text.trim();
    final content = _content.text.trim();
    if (title.isEmpty)             { setState(() => _msg = 'Please add a title.'); return; }
    if (title.length > 120)        { setState(() => _msg = 'Title too long (max 120 characters).'); return; }
    if (_wordCount < 50)           { setState(() => _msg = 'Blog must be at least 50 words (${50 - _wordCount} more needed).'); return; }
    if (content.length > 50000)    { setState(() => _msg = 'Blog too long (max 50,000 characters).'); return; }

    setState(() { _loading = true; _msg = null; });
    try {
      final raw = content.replaceAll('\n', ' ');
      final excerpt = '${raw.substring(0, raw.length.clamp(0, 200))}...';
      final dio = Dio();
      await dio.post(
        '$supabaseUrl/rest/v1/blogs',
        data: {
          'title':         title,
          'slug':          _slugify(title),
          'content':       content,
          'excerpt':       excerpt,
          'category':      _category,
          'cover_image':   _coverUrl.text.trim().isEmpty ? null : _coverUrl.text.trim(),
          'author_id':     widget.userId,
          'author_name':   _authorName.text.trim().isEmpty ? (widget.userEmail?.split('@')[0] ?? 'Parkho User') : _authorName.text.trim(),
          'author_bio':    _authorBio.text.trim().isEmpty ? null : _authorBio.text.trim(),
          'author_avatar': null,
          'status':        'pending',
        },
        options: Options(headers: {
          'apikey': supabaseAnonKey,
          'Authorization': 'Bearer ${widget.userToken}',
          'Content-Type': 'application/json',
          'Prefer': 'return=minimal',
        }),
      );
      setState(() { _success = true; });
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['message']?.toString() ?? 'Submission failed.');
    } catch (_) {
      setState(() => _msg = 'Submission failed. Please try again.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_success) {
      return Container(
        decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
        padding: const EdgeInsets.all(32),
        child: Column(mainAxisSize: MainAxisSize.min, children: [
          Container(width: 72, height: 72,
              decoration: BoxDecoration(color: const Color(0xFFDCFCE7), shape: BoxShape.circle),
              child: const Icon(Icons.check_circle_outline, color: Color(0xFF16A34A), size: 40)),
          const SizedBox(height: 16),
          const Text('Blog Submitted!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
          const SizedBox(height: 8),
          const Text('Your blog is under review. Once approved by the admin it will be published on Parkho.',
              textAlign: TextAlign.center, style: TextStyle(fontSize: 13, color: AppColors.textMuted, height: 1.5)),
          const SizedBox(height: 24),
          GestureDetector(onTap: () => Navigator.pop(context),
              child: Container(padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: const Text('Done', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)))),
        ]),
      );
    }

    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      child: Column(mainAxisSize: MainAxisSize.min, children: [
        // Handle bar
        const SizedBox(height: 12),
        Center(child: Container(width: 36, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),

        // Guidelines banner
        const SizedBox(height: 12),
        Container(
          margin: const EdgeInsets.symmetric(horizontal: 20),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: BoxDecoration(color: const Color(0xFFFFF7ED), borderRadius: BorderRadius.circular(10), border: Border.all(color: const Color(0xFFFED7AA))),
          child: const Text('📋 Write original content (min 50 words). No promotions or spam. Blogs are reviewed by admin before publishing.',
              style: TextStyle(fontSize: 12, color: Color(0xFFC2410C))),
        ),

        Expanded(child: SingleChildScrollView(
          padding: EdgeInsets.fromLTRB(20, 16, 20, MediaQuery.of(context).viewInsets.bottom + 24),
          child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [

            const Text('✍️ Write a Blog Post', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
            const SizedBox(height: 16),

            // Title
            _lbl('Blog Title *'),
            const SizedBox(height: 5),
            _tf(_title, 'E.g. Why I stopped using products with SLS', maxLength: 120),
            Align(alignment: Alignment.centerRight, child: Text('${_title.text.length}/120', style: const TextStyle(fontSize: 11, color: AppColors.textMuted))),
            const SizedBox(height: 14),

            // Category + Author Name
            Row(children: [
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _lbl('Category *'),
                const SizedBox(height: 5),
                Container(padding: const EdgeInsets.symmetric(horizontal: 14),
                    decoration: BoxDecoration(color: AppColors.surface, borderRadius: BorderRadius.circular(10), border: Border.all(color: AppColors.border)),
                    child: DropdownButtonHideUnderline(child: DropdownButton<String>(
                      value: _category,
                      isExpanded: true,
                      items: _blogCategories.map((c) => DropdownMenuItem(value: c, child: Text(c, style: const TextStyle(fontSize: 14)))).toList(),
                      onChanged: (v) { if (v != null) setState(() => _category = v); },
                    ))),
              ])),
              const SizedBox(width: 12),
              Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                _lbl('Your Name'),
                const SizedBox(height: 5),
                _tf(_authorName, 'Display name'),
              ])),
            ]),
            const SizedBox(height: 14),

            // Author bio
            _lbl('About You (optional)'),
            const SizedBox(height: 5),
            _tf(_authorBio, 'E.g. Nutritionist based in Delhi. Passionate about healthy living.', maxLines: 2, maxLength: 250),
            const SizedBox(height: 14),

            // Cover image URL
            _lbl('Cover Image URL (optional)'),
            const SizedBox(height: 5),
            _tf(_coverUrl, 'https://example.com/image.jpg'),
            const SizedBox(height: 14),

            // Content
            _lbl('Blog Content *'),
            const SizedBox(height: 5),
            TextField(
              controller: _content,
              maxLines: 12,
              onChanged: (_) => setState(() {}),
              style: const TextStyle(fontSize: 14, height: 1.6),
              decoration: InputDecoration(
                hintText: 'Start writing your blog here... Share what you know about ingredients, products, or healthy habits. Be honest, be helpful.',
                hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
                filled: true, fillColor: AppColors.surface, contentPadding: const EdgeInsets.all(14),
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
                focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
              ),
            ),
            const SizedBox(height: 4),
            Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
              Text('$_wordCount words${_wordCount < 50 ? ' (${50 - _wordCount} more needed)' : ' ✓'}',
                  style: TextStyle(fontSize: 11, color: _wordCount < 50 ? const Color(0xFFDC2626) : const Color(0xFF16A34A))),
              Text('${_content.text.length} chars', style: const TextStyle(fontSize: 11, color: AppColors.textMuted)),
            ]),
            const SizedBox(height: 16),

            if (_msg != null)
              Container(margin: const EdgeInsets.only(bottom: 10), padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: const Color(0xFFFEF2F2), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFFCA5A5))),
                  child: Text(_msg!, style: const TextStyle(fontSize: 12, color: Color(0xFFDC2626)))),

            GestureDetector(
              onTap: _loading ? null : _submit,
              child: Container(padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: _loading ? AppColors.textMuted : AppColors.brandOrange, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: _loading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text('🚀 Submit for Review', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15))),
            ),
            const SizedBox(height: 10),
            const Text('Your blog will be reviewed by our team. We\'ll publish it if it meets our community guidelines.',
                textAlign: TextAlign.center, style: TextStyle(fontSize: 11, color: AppColors.textMuted)),
          ]),
        )),
      ]),
    );
  }

  Widget _lbl(String t) => Text(t, style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: AppColors.textPrimary));

  Widget _tf(TextEditingController ctrl, String hint, {int maxLines = 1, int? maxLength}) => TextField(
    controller: ctrl, maxLines: maxLines, maxLength: maxLength,
    onChanged: (_) => setState(() {}),
    style: const TextStyle(fontSize: 14),
    decoration: InputDecoration(
      hintText: hint, hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13), counterText: '',
      filled: true, fillColor: AppColors.surface, contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
      enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
      focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
    ),
  );
}

// ── Shared sheet shell ────────────────────────────────────────────────────────

class _Sheet extends StatelessWidget {
  final String title;
  final bool loading, success;
  final String? msg;
  final VoidCallback onSubmit;
  final List<_Field> fields;
  const _Sheet({required this.title, required this.loading, required this.success, required this.msg, required this.onSubmit, required this.fields});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(color: Colors.white, borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      padding: EdgeInsets.fromLTRB(20, 20, 20, MediaQuery.of(context).viewInsets.bottom + 24),
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          mainAxisSize: MainAxisSize.min,
          children: [
            Center(child: Container(width: 36, height: 4, decoration: BoxDecoration(color: AppColors.border, borderRadius: BorderRadius.circular(2)))),
            const SizedBox(height: 16),
            Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: AppColors.textPrimary, fontFamily: 'Poppins')),
            const SizedBox(height: 16),
            if (!success) ...[
              ...fields.map((f) => Padding(padding: const EdgeInsets.only(bottom: 12), child: f)),
              if (msg != null)
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(color: const Color(0xFFFEF2F2), borderRadius: BorderRadius.circular(8), border: Border.all(color: const Color(0xFFFCA5A5))),
                  child: Text(msg!, style: const TextStyle(fontSize: 12, color: Color(0xFFDC2626))),
                ),
              const SizedBox(height: 8),
              GestureDetector(
                onTap: loading ? null : onSubmit,
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(
                    color: loading ? AppColors.textMuted : AppColors.brandOrange,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  alignment: Alignment.center,
                  child: loading
                      ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                      : const Text('Submit', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ] else ...[
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(color: const Color(0xFFF0FDF4), borderRadius: BorderRadius.circular(12), border: Border.all(color: const Color(0xFF86EFAC))),
                child: Row(
                  children: [
                    const Icon(Icons.check_circle, color: Color(0xFF16a34a), size: 24),
                    const SizedBox(width: 12),
                    Expanded(child: Text(msg ?? 'Done!', style: const TextStyle(fontSize: 13, color: Color(0xFF15803D)))),
                  ],
                ),
              ),
              const SizedBox(height: 16),
              GestureDetector(
                onTap: () => Navigator.pop(context),
                child: Container(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  decoration: BoxDecoration(color: AppColors.textPrimary, borderRadius: BorderRadius.circular(12)),
                  alignment: Alignment.center,
                  child: const Text('Done', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w700, fontSize: 15)),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}

class _Field extends StatelessWidget {
  final String label, hint;
  final TextEditingController ctrl;
  final int maxLines;
  const _Field(this.label, this.ctrl, this.hint, {this.maxLines = 1});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600, color: AppColors.textPrimary)),
        const SizedBox(height: 5),
        TextField(
          controller: ctrl,
          maxLines: maxLines,
          style: const TextStyle(fontSize: 14),
          decoration: InputDecoration(
            hintText: hint,
            hintStyle: const TextStyle(color: AppColors.textMuted, fontSize: 13),
            filled: true, fillColor: AppColors.surface,
            contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
            enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.border)),
            focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange, width: 1.5)),
          ),
        ),
      ],
    );
  }
}
