import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:go_router/go_router.dart';
import '../../core/api/api_client.dart';
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
                              decoration: BoxDecoration(color: AppColors.brandOrange, borderRadius: BorderRadius.circular(10)),
                              alignment: Alignment.center,
                              child: const Text('Add Product', style: TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.w600)),
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
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                      const Text('Could not connect. Check your internet.', textAlign: TextAlign.center, style: TextStyle(color: Colors.white, fontSize: 13)),
                      const SizedBox(height: 10),
                      GestureDetector(onTap: _retry, child: const Text('Try again', style: TextStyle(color: Colors.white, decoration: TextDecoration.underline, fontSize: 13))),
                    ]),
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
