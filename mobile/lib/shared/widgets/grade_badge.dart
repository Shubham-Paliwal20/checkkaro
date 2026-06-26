import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

const _gradeMeta = {
  'A': (label: 'Excellent', desc: 'Minimal concern ingredients. Largely clean label.',   color: Color(0xFF16a34a), bg: Color(0xFFf0fdf4), border: Color(0xFF86efac)),
  'B': (label: 'Good',      desc: 'Mostly safe. Some commonly noted additives.',          color: Color(0xFF2563eb), bg: Color(0xFFeff6ff), border: Color(0xFF93c5fd)),
  'C': (label: 'Average',   desc: 'Mixed formulation. Several commonly questioned ingredients.', color: Color(0xFFd97706), bg: Color(0xFFfffbeb), border: Color(0xFFfcd34d)),
  'D': (label: 'Poor',      desc: 'Proportion of questioned or banned ingredients.',      color: Color(0xFFdc2626), bg: Color(0xFFfef2f2), border: Color(0xFFfca5a5)),
};

class GradeBadge extends StatelessWidget {
  final String grade;
  final double size;
  final bool showLabel;

  const GradeBadge({super.key, required this.grade, this.size = 36, this.showLabel = false});

  @override
  Widget build(BuildContext context) {
    final meta  = _gradeMeta[grade.toUpperCase()] ?? _gradeMeta['C']!;
    final color  = meta.color;
    final bg     = meta.bg;
    final border = meta.border;

    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: size, height: size,
          decoration: BoxDecoration(
            color: bg,
            shape: BoxShape.circle,
            border: Border.all(color: color, width: size * 0.055),
            boxShadow: [BoxShadow(color: border, blurRadius: 0, spreadRadius: size * 0.04)],
          ),
          alignment: Alignment.center,
          child: Text(
            grade.toUpperCase(),
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.w800,
              fontSize: size * 0.45,
              fontFamily: 'Poppins',
              letterSpacing: -0.5,
            ),
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 8),
          Text(meta.label,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 14, fontWeight: FontWeight.w800, color: color)),
          const SizedBox(height: 3),
          SizedBox(
            width: 150,
            child: Text(meta.desc,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 11, color: AppColors.textMuted, height: 1.4)),
          ),
        ],
      ],
    );
  }
}

// Standalone label+desc for use in cards (no circle)
String gradeLabel(String grade) => _gradeMeta[grade.toUpperCase()]?.label ?? 'Average';
String gradeDesc(String grade)  => _gradeMeta[grade.toUpperCase()]?.desc  ?? '';
