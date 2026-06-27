import 'dart:io';
import 'dart:math';
import 'dart:async';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../../core/api/api_client.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';
import '../auth/login_screen.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  final _controller = MobileScannerController();
  bool _scanning = true;
  bool _loading  = false;
  String? _barcode;
  String? _error;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _onDetect(BarcodeCapture capture) async {
    if (!_scanning || _loading) return;
    final barcode = capture.barcodes.isNotEmpty ? capture.barcodes.first.rawValue : null;
    if (barcode == null) return;

    setState(() { _scanning = false; _loading = true; _error = null; _barcode = barcode; });
    _controller.stop();

    try {
      final product = await ApiClient.getProductByBarcode(barcode);
      if (!mounted) return;
      if (product != null) {
        final key = product['static_key'] ?? product['id'];
        context.push('/product/$key');
        setState(() { _loading = false; _scanning = true; });
        _controller.start();
      } else {
        setState(() { _loading = false; _error = 'not_found'; });
      }
    } catch (e) {
      if (!mounted) return;
      final is404 = e.toString().contains('404') || e.toString().contains('not found');
      setState(() { _loading = false; _error = is404 ? 'not_found' : 'error'; });
    }
  }

  void _retry() {
    setState(() { _scanning = true; _error = null; _barcode = null; });
    _controller.start();
  }

  void _openSubmitSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      backgroundColor: Colors.transparent,
      builder: (_) => _BarcodeSubmissionSheet(barcode: _barcode!),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: const Text('Scan Barcode'),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.flash_on),
            onPressed: () => _controller.toggleTorch(),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(controller: _controller, onDetect: _onDetect),

          Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 240, height: 240,
                  decoration: BoxDecoration(
                    border: Border.all(color: _error != null ? Colors.red : AppColors.brandOrange, width: 3),
                    borderRadius: BorderRadius.circular(16),
                  ),
                ),
                const SizedBox(height: 24),

                if (_loading)
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                    decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(12)),
                    child: const Row(mainAxisSize: MainAxisSize.min, children: [
                      SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)),
                      SizedBox(width: 12),
                      Text('Looking up product...', style: TextStyle(color: Colors.white, fontSize: 14)),
                    ]),
                  )

                else if (_error == 'not_found')
                  Container(
                    margin: const EdgeInsets.symmetric(horizontal: 24),
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(16)),
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                      const Icon(Icons.search_off, color: Colors.white54, size: 32),
                      const SizedBox(height: 8),
                      Text(
                        'Barcode $_barcode\nnot in our database yet.',
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: Colors.white, fontSize: 13, height: 1.4),
                      ),
                      const SizedBox(height: 14),
                      GestureDetector(
                        onTap: _openSubmitSheet,
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(10)),
                          alignment: Alignment.center,
                          child: const Text('Submit Product Info', style: TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w700)),
                        ),
                      ),
                      const SizedBox(height: 8),
                      GestureDetector(
                        onTap: _retry,
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(vertical: 10),
                          decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(10)),
                          alignment: Alignment.center,
                          child: const Text('Scan Again', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
                        ),
                      ),
                    ]),
                  )

                else if (_error == 'error')
                  Container(
                    margin: const EdgeInsets.symmetric(horizontal: 32),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(color: Colors.red.shade900, borderRadius: BorderRadius.circular(10)),
                    child: const Text('Could not connect. Check your internet.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white, fontSize: 13)),
                  )

                else
                  const Text('Point camera at product barcode', style: TextStyle(color: Colors.white70, fontSize: 14)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}


// ── Barcode Submission Sheet ──────────────────────────────────────────────────

class _BarcodeSubmissionSheet extends ConsumerStatefulWidget {
  final String barcode;
  const _BarcodeSubmissionSheet({required this.barcode});

  @override
  ConsumerState<_BarcodeSubmissionSheet> createState() => _BarcodeSubmissionSheetState();
}

class _BarcodeSubmissionSheetState extends ConsumerState<_BarcodeSubmissionSheet> {
  final _nameCtrl    = TextEditingController();
  final _variantCtrl = TextEditingController();
  final _picker      = ImagePicker();
  final _rng         = Random();
  List<XFile> _photos = [];
  bool _uploading  = false;
  bool _submitting = false;
  String? _error;
  bool _submitted  = false;

  @override
  void dispose() {
    _nameCtrl.dispose();
    _variantCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickPhotos() async {
    if (_photos.length >= 5) return;
    try {
      final picked = await _picker.pickMultiImage(imageQuality: 80);
      if (picked.isEmpty) return;
      final canAdd = 5 - _photos.length;
      setState(() => _photos = [..._photos, ...picked.take(canAdd)]);
    } catch (e) {
      setState(() => _error = 'Could not open gallery.');
    }
  }

  void _removePhoto(int index) {
    setState(() => _photos = [..._photos]..removeAt(index));
  }

  Future<String> _uploadPhoto(XFile file, String userId, String token) async {
    final bytes = await file.readAsBytes();
    final ext   = file.name.split('.').last.toLowerCase();
    final mime  = ext == 'png' ? 'image/png' : 'image/jpeg';
    final ts    = DateTime.now().millisecondsSinceEpoch;
    final rand  = _rng.nextInt(9999).toString().padLeft(4, '0');
    final path  = 'barcode-submissions/$userId/${ts}_$rand.$ext';
    await Dio().put(
      '$supabaseUrl/storage/v1/object/product-images/$path',
      data: bytes,
      options: Options(headers: {
        'apikey': supabaseAnonKey,
        'Authorization': 'Bearer $token',
        'Content-Type': mime,
      }),
    );
    return '$supabaseUrl/storage/v1/object/public/product-images/$path';
  }

  Future<void> _submit() async {
    final user = ref.read(authProvider);
    if (user == null) { _goToLogin(); return; }

    final name = _nameCtrl.text.trim();
    if (name.isEmpty) { setState(() => _error = 'Product name is required.'); return; }
    if (_photos.isEmpty) { setState(() => _error = 'Please add at least 1 front photo.'); return; }

    setState(() { _submitting = true; _uploading = true; _error = null; });
    try {
      final urls = <String>[];
      for (final photo in _photos) {
        urls.add(await _uploadPhoto(photo, user.id, user.accessToken));
      }
      setState(() => _uploading = false);

      await ApiClient.submitBarcodeWithPhotos(
        barcode: widget.barcode,
        productName: name,
        photos: urls,
        accessToken: user.accessToken,
        variantLabel: _variantCtrl.text.trim().isEmpty ? null : _variantCtrl.text.trim(),
      );
      if (mounted) setState(() { _submitted = true; _submitting = false; });
    } on DioException catch (e) {
      final detail = (e.response?.data as Map?)?['detail']?.toString() ?? 'Submission failed. Please try again.';
      if (mounted) setState(() { _error = detail; _submitting = false; _uploading = false; });
    } on Exception catch (_) {
      if (mounted) setState(() { _error = 'Submission failed. Please try again.'; _submitting = false; _uploading = false; });
    }
  }

  void _goToLogin() {
    Navigator.of(context, rootNavigator: true).push(
      MaterialPageRoute(fullscreenDialog: true, builder: (_) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(width: 40, height: 4, margin: const EdgeInsets.symmetric(vertical: 12),
              decoration: BoxDecoration(color: Colors.grey.shade300, borderRadius: BorderRadius.circular(2))),
          Flexible(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 28),
              child: _submitted ? _buildSuccess() : _buildForm(),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSuccess() {
    return Column(children: [
      const SizedBox(height: 32),
      Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(color: Colors.green.shade50, shape: BoxShape.circle),
        child: Icon(Icons.check_circle, color: Colors.green.shade600, size: 48),
      ),
      const SizedBox(height: 16),
      const Text('Submitted!', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w800, color: Color(0xFF0D1B2A))),
      const SizedBox(height: 8),
      const Text(
        'Our team will review the product info\nyou submitted. You\'ll earn ₹1 once approved.',
        textAlign: TextAlign.center,
        style: TextStyle(fontSize: 13, color: Color(0xFF6B7280), height: 1.5),
      ),
      const SizedBox(height: 32),
    ]);
  }

  Widget _buildForm() {
    final user = ref.watch(authProvider);
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const Text('Submit Product Info', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: Color(0xFF0D1B2A))),
      const SizedBox(height: 4),
      Text('Barcode: ${widget.barcode}', style: const TextStyle(fontSize: 12, color: Color(0xFF6B7280), fontFamily: 'monospace')),
      const SizedBox(height: 4),
      const Text('Our team will review & add it to the database.', style: TextStyle(fontSize: 12, color: Color(0xFF9CA3AF))),
      const SizedBox(height: 18),

      // Product name
      const Text('Product Name *', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
      const SizedBox(height: 6),
      TextField(
        controller: _nameCtrl,
        textCapitalization: TextCapitalization.words,
        decoration: InputDecoration(
          hintText: 'e.g. Maggi Masala Noodles',
          hintStyle: const TextStyle(fontSize: 13, color: Color(0xFF9CA3AF)),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          filled: true, fillColor: const Color(0xFFF9FAFB),
        ),
        style: const TextStyle(fontSize: 14),
      ),
      const SizedBox(height: 18),

      // Photos
      Row(children: [
        const Text('Photos *', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
        const SizedBox(width: 6),
        Text('(front photo required, max 5)', style: TextStyle(fontSize: 11, color: Colors.grey.shade500)),
      ]),
      const SizedBox(height: 8),

      if (_photos.isNotEmpty) ...[
        SizedBox(
          height: 90,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            itemCount: _photos.length + (_photos.length < 5 ? 1 : 0),
            separatorBuilder: (_, __) => const SizedBox(width: 8),
            itemBuilder: (ctx, i) {
              if (i == _photos.length) {
                // Add more button
                return GestureDetector(
                  onTap: _pickPhotos,
                  child: Container(
                    width: 80,
                    decoration: BoxDecoration(
                      border: Border.all(color: AppColors.brandOrange, width: 1.5),
                      borderRadius: BorderRadius.circular(10),
                      color: Colors.orange.shade50,
                    ),
                    child: const Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                      Icon(Icons.add_photo_alternate_outlined, color: AppColors.brandOrange, size: 24),
                      SizedBox(height: 4),
                      Text('Add', style: TextStyle(fontSize: 11, color: AppColors.brandOrange, fontWeight: FontWeight.w600)),
                    ]),
                  ),
                );
              }
              return Stack(children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(10),
                  child: Image.file(File(_photos[i].path), width: 80, height: 80, fit: BoxFit.cover),
                ),
                Positioned(top: 2, right: 2,
                  child: GestureDetector(
                    onTap: () => _removePhoto(i),
                    child: Container(
                      decoration: const BoxDecoration(color: Colors.black54, shape: BoxShape.circle),
                      padding: const EdgeInsets.all(2),
                      child: const Icon(Icons.close, color: Colors.white, size: 14),
                    ),
                  ),
                ),
                if (i == 0)
                  Positioned(bottom: 0, left: 0, right: 0,
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 2),
                      decoration: const BoxDecoration(color: Colors.black54, borderRadius: BorderRadius.vertical(bottom: Radius.circular(10))),
                      alignment: Alignment.center,
                      child: const Text('Front', style: TextStyle(color: Colors.white, fontSize: 9, fontWeight: FontWeight.w600)),
                    ),
                  ),
              ]);
            },
          ),
        ),
        const SizedBox(height: 8),
      ] else ...[
        GestureDetector(
          onTap: _pickPhotos,
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 18),
            decoration: BoxDecoration(
              border: Border.all(color: AppColors.brandOrange, width: 1.5),
              borderRadius: BorderRadius.circular(10),
              color: Colors.orange.shade50,
            ),
            child: const Column(children: [
              Icon(Icons.add_photo_alternate_outlined, color: AppColors.brandOrange, size: 32),
              SizedBox(height: 6),
              Text('Add front photo of product', style: TextStyle(fontSize: 13, color: AppColors.brandOrange, fontWeight: FontWeight.w600)),
              SizedBox(height: 2),
              Text('Clear photo of product label helps us verify', style: TextStyle(fontSize: 11, color: Color(0xFF9CA3AF))),
            ]),
          ),
        ),
        const SizedBox(height: 8),
      ],

      // Variant
      const Text('Variant / Size (optional)', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
      const SizedBox(height: 6),
      TextField(
        controller: _variantCtrl,
        decoration: InputDecoration(
          hintText: 'e.g. 70g, 500ml, Family Pack',
          hintStyle: const TextStyle(fontSize: 13, color: Color(0xFF9CA3AF)),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          filled: true, fillColor: const Color(0xFFF9FAFB),
        ),
        style: const TextStyle(fontSize: 14),
      ),

      if (_error != null) ...[
        const SizedBox(height: 10),
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.red.shade200)),
          child: Text(_error!, style: TextStyle(fontSize: 12, color: Colors.red.shade700)),
        ),
      ],

      const SizedBox(height: 20),

      GestureDetector(
        onTap: _submitting ? null : (user == null ? _goToLogin : _submit),
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(vertical: 14),
          decoration: BoxDecoration(
            color: _submitting ? Colors.grey.shade300 : AppColors.brandOrange,
            borderRadius: BorderRadius.circular(12),
          ),
          alignment: Alignment.center,
          child: _submitting
              ? Row(mainAxisSize: MainAxisSize.min, children: [
                  const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)),
                  const SizedBox(width: 10),
                  Text(_uploading ? 'Uploading photos...' : 'Submitting...',
                      style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: Colors.white)),
                ])
              : Text(
                  user == null ? 'Log in to Submit' : 'Submit — Earn ₹1 on Approval',
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: Colors.white),
                ),
        ),
      ),
    ]);
  }
}
