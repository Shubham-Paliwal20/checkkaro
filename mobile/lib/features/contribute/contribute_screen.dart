import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../core/auth/auth_provider.dart';
import '../../core/theme/app_theme.dart';

const _backendUrl = 'https://checkkaro.onrender.com';

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
                      builder: (_) => _SubmitProductSheet(userToken: user?.accessToken)),
                ),
                const SizedBox(height: 12),
                _ContributeCard(
                  icon: Icons.camera_alt_outlined,
                  title: 'Submit Product Photo',
                  subtitle: 'Upload a product label photo. Earn ₹1 per approved submission.',
                  color: AppColors.brandOrange,
                  onTap: () => showModalBottomSheet(context: context, isScrollControlled: true, backgroundColor: Colors.transparent,
                      builder: (_) => _PhotoSheet(userToken: user?.accessToken)),
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
                      builder: (_) => _BlogSheet(userToken: user?.accessToken)),
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
  const _SubmitProductSheet({this.userToken});

  @override
  State<_SubmitProductSheet> createState() => _SubmitProductSheetState();
}

class _SubmitProductSheetState extends State<_SubmitProductSheet> {
  final _name      = TextEditingController();
  final _brand     = TextEditingController();
  final _ingreds   = TextEditingController();
  final _category  = TextEditingController();
  bool  _loading   = false;
  String? _msg;
  bool  _success   = false;

  Future<void> _submit() async {
    if (_name.text.trim().isEmpty) { setState(() => _msg = 'Product name is required.'); return; }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/submit/product',
        data: {
          'product_name': _name.text.trim(),
          'brand':        _brand.text.trim(),
          'ingredients':  _ingreds.text.trim(),
          'category':     _category.text.trim(),
        },
        options: Options(headers: {
          if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}',
        }),
      );
      setState(() { _success = true; _msg = 'Submitted! We\'ll review it shortly.'; });
    } on DioException catch (e) {
      setState(() => _msg = (e.response?.data as Map?)?['detail']?.toString() ?? 'Submission failed. Please try again.');
    } catch (_) {
      setState(() => _msg = 'Submission failed. Please try again.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return _Sheet(
      title: '📦 Submit a Product',
      loading: _loading,
      msg: _msg,
      success: _success,
      onSubmit: _submit,
      fields: [
        _Field('Product name *', _name, 'e.g. Maggi 2-Minute Noodles Masala'),
        _Field('Brand', _brand, 'e.g. Nestlé'),
        _Field('Category', _category, 'e.g. Instant Noodles, Skincare'),
        _Field('Ingredients (paste from label)', _ingreds, 'e.g. Wheat flour, Palm oil...', maxLines: 4),
      ],
    );
  }
}

// ── Photo sheet ───────────────────────────────────────────────────────────────

class _PhotoSheet extends StatefulWidget {
  final String? userToken;
  const _PhotoSheet({this.userToken});

  @override
  State<_PhotoSheet> createState() => _PhotoSheetState();
}

class _PhotoSheetState extends State<_PhotoSheet> {
  final _productName = TextEditingController();
  final _photoUrl    = TextEditingController();
  bool  _loading     = false;
  String? _msg;
  bool  _success     = false;

  Future<void> _submit() async {
    if (_productName.text.trim().isEmpty) { setState(() => _msg = 'Product name is required.'); return; }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/submit/photo',
        data: {'product_name': _productName.text.trim(), 'photo_url': _photoUrl.text.trim()},
        options: Options(headers: {if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}'}),
      );
      setState(() { _success = true; _msg = 'Photo submitted! You\'ll earn ₹1 when it\'s approved.'; });
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
      title: '📷 Submit Product Photo',
      loading: _loading, msg: _msg, success: _success, onSubmit: _submit,
      fields: [
        _Field('Product name *', _productName, 'e.g. Dove Beauty Bar'),
        _Field('Photo URL (from your device or cloud)', _photoUrl, 'https://...'),
      ],
    );
  }
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
  final _issue   = TextEditingController();
  bool  _loading = false;
  String? _msg;
  bool  _success = false;

  Future<void> _submit() async {
    if (_product.text.trim().isEmpty || _issue.text.trim().isEmpty) {
      setState(() => _msg = 'Please fill in all fields.');
      return;
    }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/submit/report',
        data: {'product_name': _product.text.trim(), 'issue': _issue.text.trim()},
        options: Options(headers: {if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}'}),
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
        _Field('What\'s wrong? *', _issue, 'Describe the incorrect ingredient or information...', maxLines: 4),
      ],
    );
  }
}

// ── Blog sheet ────────────────────────────────────────────────────────────────

class _BlogSheet extends StatefulWidget {
  final String? userToken;
  const _BlogSheet({this.userToken});

  @override
  State<_BlogSheet> createState() => _BlogSheetState();
}

class _BlogSheetState extends State<_BlogSheet> {
  final _title   = TextEditingController();
  final _excerpt = TextEditingController();
  final _content = TextEditingController();
  final _category = TextEditingController();
  bool  _loading  = false;
  String? _msg;
  bool  _success  = false;

  Future<void> _submit() async {
    if (_title.text.trim().isEmpty || _content.text.trim().isEmpty) {
      setState(() => _msg = 'Title and content are required.');
      return;
    }
    setState(() { _loading = true; _msg = null; });
    try {
      final dio = Dio();
      await dio.post(
        '$_backendUrl/api/blog/submit',
        data: {
          'title':    _title.text.trim(),
          'excerpt':  _excerpt.text.trim(),
          'content':  _content.text.trim(),
          'category': _category.text.trim().isEmpty ? 'General' : _category.text.trim(),
        },
        options: Options(headers: {if (widget.userToken != null) 'Authorization': 'Bearer ${widget.userToken}'}),
      );
      setState(() { _success = true; _msg = 'Blog submitted for review! We\'ll publish it after approval.'; });
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
      title: '✍️ Write a Blog Post',
      loading: _loading, msg: _msg, success: _success, onSubmit: _submit,
      fields: [
        _Field('Title *', _title, 'e.g. Why I Check Every Label Now'),
        _Field('Category', _category, 'Food / Cosmetics / Health / Lifestyle'),
        _Field('Short summary', _excerpt, 'One or two sentence summary shown in the blog list...'),
        _Field('Content *', _content, 'Write your article here... Markdown supported.', maxLines: 8),
      ],
    );
  }
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
