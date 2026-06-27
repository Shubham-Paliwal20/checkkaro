import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import '../../core/config/app_config.dart';
import '../../core/theme/app_theme.dart';

const _questions = [
  _Question(id: 'age_group',       text: 'What is your age group?',                     options: ['Under 18', '18–25', '26–35', '36–45', '46+'],                                                              single: true),
  _Question(id: 'health_concern',  text: 'Which area matters most to you?',              options: ['Fitness', 'Nutrition', 'Skincare', 'Haircare', 'Overall wellness'],                                          single: false),
  _Question(id: 'diet_type',       text: 'Do you follow a specific diet?',               options: ['Vegan', 'Vegetarian', 'Non-vegetarian', 'Keto / Low-carb', 'Jain', 'No specific diet'],                    single: false),
  _Question(id: 'check_frequency', text: 'How often do you check product ingredients?',  options: ['Always – before every purchase', 'Sometimes', 'Rarely', 'This is my first time'],                           single: false),
  _Question(id: 'product_category',text: 'Which products do you check most?',            options: ['Packaged snacks / Food', 'Beverages', 'Cosmetics / Skincare', 'Baby products', 'Health supplements'],       single: false),
];

class _Question {
  final String id, text;
  final List<String> options;
  final bool single;
  const _Question({required this.id, required this.text, required this.options, required this.single});
}

class OnboardingQuizScreen extends StatefulWidget {
  final String userId;
  final String accessToken;
  const OnboardingQuizScreen({super.key, required this.userId, required this.accessToken});

  @override
  State<OnboardingQuizScreen> createState() => _OnboardingQuizScreenState();
}

class _OnboardingQuizScreenState extends State<OnboardingQuizScreen> {
  final Map<String, dynamic> _answers = {};
  bool _loading = false;

  bool _isSelected(String id, String opt) {
    final v = _answers[id];
    if (v == null) return false;
    if (v is List) return v.contains(opt);
    return v == opt;
  }

  void _toggle(String id, String opt, bool single) {
    setState(() {
      if (single) {
        _answers[id] = opt;
      } else {
        final cur = List<String>.from(_answers[id] as List? ?? []);
        if (cur.contains(opt)) {
          cur.remove(opt);
        } else {
          cur.add(opt);
        }
        _answers[id] = cur;
      }
    });
  }

  Future<void> _submit({bool skip = false}) async {
    setState(() => _loading = true);
    try {
      final dio = Dio();
      final headers = {
        'apikey': supabaseAnonKey,
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
        'Prefer': 'resolution=merge-duplicates',
      };
      final body = <String, dynamic>{'id': widget.userId, 'quiz_completed': true};
      if (!skip) {
        for (final q in _questions) {
          final v = _answers[q.id];
          if (v != null && (v is! List || (v as List).isNotEmpty)) {
            body[q.id] = v;
          }
        }
      }
      await dio.post(
        '$supabaseUrl/rest/v1/user_profiles',
        data: body,
        options: Options(headers: headers),
      );
    } catch (_) {}
    if (mounted) {
      setState(() => _loading = false);
      Navigator.of(context).pop();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        children: [
          // Dark header
          Container(
            width: double.infinity,
            padding: EdgeInsets.fromLTRB(20, MediaQuery.of(context).padding.top + 24, 20, 28),
            decoration: const BoxDecoration(color: AppColors.textPrimary),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: AppColors.brandOrange.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: AppColors.brandOrange.withOpacity(0.4)),
                  ),
                  child: const Text('Quick Setup',
                      style: TextStyle(fontSize: 12, fontWeight: FontWeight.w700, color: AppColors.brandOrange)),
                ),
                const SizedBox(height: 12),
                const Text('Personalise your\nexperience',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: Colors.white,
                        fontFamily: 'Poppins', height: 1.2)),
                const SizedBox(height: 8),
                const Text('Answer a few quick questions so we can tailor your experience. All optional.',
                    style: TextStyle(fontSize: 13, color: Color(0xFFD1D5DB), height: 1.5)),
              ],
            ),
          ),

          // Questions
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.fromLTRB(20, 24, 20, 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  ..._questions.map((q) => _QuestionBlock(
                    question: q,
                    isSelected: (opt) => _isSelected(q.id, opt),
                    onToggle: (opt) => _toggle(q.id, opt, q.single),
                  )),
                  const SizedBox(height: 8),
                ],
              ),
            ),
          ),

          // Bottom action bar
          Container(
            padding: EdgeInsets.fromLTRB(20, 12, 20, MediaQuery.of(context).padding.bottom + 12),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border(top: BorderSide(color: AppColors.border)),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 8, offset: const Offset(0, -2))],
            ),
            child: Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: _loading ? null : () => _submit(skip: true),
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      side: const BorderSide(color: AppColors.border),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: const Text('Skip',
                        style: TextStyle(color: AppColors.textMuted, fontWeight: FontWeight.w600, fontSize: 14)),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  flex: 2,
                  child: ElevatedButton(
                    onPressed: _loading ? null : () => _submit(),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.brandGreen,
                      foregroundColor: Colors.white,
                      elevation: 0,
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: _loading
                        ? const SizedBox(width: 20, height: 20,
                            child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2.5))
                        : const Text('Submit & Continue',
                            style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14)),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _QuestionBlock extends StatelessWidget {
  final _Question question;
  final bool Function(String) isSelected;
  final void Function(String) onToggle;
  const _QuestionBlock({required this.question, required this.isSelected, required this.onToggle});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Text(question.text,
                    style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w700, color: AppColors.textPrimary)),
              ),
              const SizedBox(width: 8),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: question.single ? AppColors.surface : const Color(0xFFFFF7ED),
                  borderRadius: BorderRadius.circular(99),
                ),
                child: Text(
                  question.single ? 'Pick one' : 'Multiple',
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w700,
                    color: question.single ? AppColors.textMuted : AppColors.brandOrange,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: question.options.map((opt) {
              final sel = isSelected(opt);
              return GestureDetector(
                onTap: () => onToggle(opt),
                child: AnimatedContainer(
                  duration: const Duration(milliseconds: 150),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                  decoration: BoxDecoration(
                    color: sel ? AppColors.brandOrange : Colors.white,
                    borderRadius: BorderRadius.circular(999),
                    border: Border.all(color: sel ? AppColors.brandOrange : AppColors.border),
                    boxShadow: sel
                        ? [BoxShadow(color: AppColors.brandOrange.withOpacity(0.25), blurRadius: 6, offset: const Offset(0, 2))]
                        : [],
                  ),
                  child: Text(opt,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: FontWeight.w500,
                        color: sel ? Colors.white : AppColors.textPrimary,
                      )),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }
}
