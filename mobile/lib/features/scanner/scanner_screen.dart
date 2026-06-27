import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/theme/app_theme.dart';

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

  void _openLinkSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      backgroundColor: Colors.transparent,
      builder: (_) => _LinkBarcodeSheet(barcode: _barcode!),
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

          // Scan frame overlay
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
                        onTap: _openLinkSheet,
                        child: Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(vertical: 11),
                          decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(10)),
                          alignment: Alignment.center,
                          child: const Text('Link to Existing Product', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w700)),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(children: [
                        Expanded(
                          child: GestureDetector(
                            onTap: _retry,
                            child: Container(
                              padding: const EdgeInsets.symmetric(vertical: 10),
                              decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(10)),
                              alignment: Alignment.center,
                              child: const Text('Scan Again', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
                            ),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          child: GestureDetector(
                            onTap: () => context.push('/contribute'),
                            child: Container(
                              padding: const EdgeInsets.symmetric(vertical: 10),
                              decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(10), border: Border.all(color: Colors.white30)),
                              alignment: Alignment.center,
                              child: const Text('Add New Product', style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
                            ),
                          ),
                        ),
                      ]),
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


// ── Link Barcode Sheet ────────────────────────────────────────────────────────

class _LinkBarcodeSheet extends ConsumerStatefulWidget {
  final String barcode;
  const _LinkBarcodeSheet({required this.barcode});

  @override
  ConsumerState<_LinkBarcodeSheet> createState() => _LinkBarcodeSheetState();
}

class _LinkBarcodeSheetState extends ConsumerState<_LinkBarcodeSheet> {
  final _searchCtrl  = TextEditingController();
  final _variantCtrl = TextEditingController();
  Timer? _debounce;
  List<Map<String, dynamic>> _results = [];
  Map<String, dynamic>? _selected;
  bool _searching  = false;
  bool _submitting = false;
  String? _submitError;
  bool _submitted  = false;

  @override
  void dispose() {
    _searchCtrl.dispose();
    _variantCtrl.dispose();
    _debounce?.cancel();
    super.dispose();
  }

  void _onSearchChanged(String q) {
    _debounce?.cancel();
    if (q.trim().isEmpty) { setState(() { _results = []; }); return; }
    _debounce = Timer(const Duration(milliseconds: 400), () => _search(q.trim()));
  }

  Future<void> _search(String q) async {
    setState(() { _searching = true; });
    try {
      final results = await ApiClient.searchProducts(q);
      if (mounted) setState(() { _results = results; _searching = false; });
    } catch (_) {
      if (mounted) setState(() { _searching = false; });
    }
  }

  Future<void> _submit() async {
    final user = ref.read(authProvider);
    if (user == null) { setState(() { _submitError = 'Please log in first.'; }); return; }
    if (_selected == null) { setState(() { _submitError = 'Please select a product first.'; }); return; }

    setState(() { _submitting = true; _submitError = null; });
    try {
      await ApiClient.submitBarcode(
        barcode: widget.barcode,
        productId: _selected!['id']?.toString() ?? '',
        productName: _selected!['name']?.toString() ?? '',
        accessToken: user.accessToken,
        variantLabel: _variantCtrl.text.trim().isEmpty ? null : _variantCtrl.text.trim(),
      );
      if (mounted) setState(() { _submitted = true; _submitting = false; });
    } on Exception catch (e) {
      final raw = e.toString().replaceFirst('Exception: ', '');
      final msg = (raw.contains('already') || raw.contains('submitted')) ? raw : 'Submission failed. Please try again.';
      if (mounted) setState(() { _submitError = msg; _submitting = false; });
    }
  }

  void _goToLogin() {
    Navigator.of(context).pop();
    GoRouter.of(context).push('/login');
  }

  @override
  Widget build(BuildContext context) {
    final user = ref.watch(authProvider);
    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Container(width: 40, height: 4, margin: const EdgeInsets.symmetric(vertical: 12), decoration: BoxDecoration(color: Colors.grey.shade300, borderRadius: BorderRadius.circular(2))),
          Flexible(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 24),
              child: _submitted ? _buildSuccess() : _buildForm(user),
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
      const Text('Barcode Submitted!', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800, color: Color(0xFF0D1B2A))),
      const SizedBox(height: 8),
      Text(
        'Linked barcode ${widget.barcode}\nto ${_selected?['name'] ?? 'the product'}.\nYou\'ll earn ₹1 once it\'s approved.',
        textAlign: TextAlign.center,
        style: const TextStyle(fontSize: 13, color: Color(0xFF6B7280), height: 1.5),
      ),
      const SizedBox(height: 32),
    ]);
  }

  Widget _buildForm(AuthUser? user) {
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
      const Text('Link Barcode to Product', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800, color: Color(0xFF0D1B2A))),
      const SizedBox(height: 4),
      Text('Barcode: ${widget.barcode}', style: const TextStyle(fontSize: 12, color: Color(0xFF6B7280), fontFamily: 'monospace')),
      const SizedBox(height: 14),

      if (user == null) ...[
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.orange.shade50, borderRadius: BorderRadius.circular(10), border: Border.all(color: Colors.orange.shade200)),
          child: const Text('Log in to submit a barcode link and earn ₹1.', style: TextStyle(fontSize: 13, color: Color(0xFF92400E))),
        ),
        const SizedBox(height: 14),
      ],

      const Text('Search product by name', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
      const SizedBox(height: 6),
      TextField(
        controller: _searchCtrl,
        onChanged: _onSearchChanged,
        decoration: InputDecoration(
          hintText: 'e.g. Maggi Masala Noodles',
          hintStyle: const TextStyle(fontSize: 13, color: Color(0xFF9CA3AF)),
          prefixIcon: _searching
              ? const Padding(padding: EdgeInsets.all(12), child: SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Color(0xFF9CA3AF))))
              : const Icon(Icons.search, size: 20, color: Color(0xFF9CA3AF)),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          filled: true, fillColor: const Color(0xFFF9FAFB),
        ),
        style: const TextStyle(fontSize: 14),
      ),

      if (_results.isNotEmpty) ...[
        const SizedBox(height: 6),
        Container(
          constraints: const BoxConstraints(maxHeight: 200),
          decoration: BoxDecoration(border: Border.all(color: Colors.grey.shade200), borderRadius: BorderRadius.circular(10)),
          child: ListView.separated(
            shrinkWrap: true,
            itemCount: _results.length,
            separatorBuilder: (_, __) => Divider(height: 1, color: Colors.grey.shade100),
            itemBuilder: (ctx, i) {
              final p = _results[i];
              return InkWell(
                onTap: () => setState(() {
                  _selected = p;
                  _results = [];
                  _searchCtrl.text = p['name'] ?? '';
                }),
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                  child: Row(children: [
                    Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text(p['name'] ?? '', style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF0D1B2A))),
                      if ((p['brand'] ?? '').toString().isNotEmpty)
                        Text(p['brand'].toString(), style: const TextStyle(fontSize: 11, color: Color(0xFF6B7280))),
                    ])),
                  ]),
                ),
              );
            },
          ),
        ),
      ],

      if (_selected != null) ...[
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(10), border: Border.all(color: Colors.green.shade200)),
          child: Row(children: [
            Icon(Icons.check_circle, color: Colors.green.shade600, size: 18),
            const SizedBox(width: 8),
            Expanded(child: Text(_selected!['name']?.toString() ?? '', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Colors.green.shade800))),
          ]),
        ),
      ],

      const SizedBox(height: 14),

      const Text('Variant / Size (optional)', style: TextStyle(fontSize: 13, fontWeight: FontWeight.w600, color: Color(0xFF374151))),
      const SizedBox(height: 6),
      TextField(
        controller: _variantCtrl,
        decoration: InputDecoration(
          hintText: 'e.g. 70g Pack, 500ml Bottle',
          hintStyle: const TextStyle(fontSize: 13, color: Color(0xFF9CA3AF)),
          border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide(color: Colors.grey.shade300)),
          focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: const BorderSide(color: AppColors.brandOrange)),
          contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
          filled: true, fillColor: const Color(0xFFF9FAFB),
        ),
        style: const TextStyle(fontSize: 14),
      ),

      if (_submitError != null) ...[
        const SizedBox(height: 10),
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.red.shade200)),
          child: Text(_submitError!, style: TextStyle(fontSize: 12, color: Colors.red.shade700)),
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
              ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
              : Text(
                  user == null ? 'Log in to Submit' : 'Submit — Earn ₹1 on Approval',
                  style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700, color: Colors.white),
                ),
        ),
      ),
    ]);
  }
}
