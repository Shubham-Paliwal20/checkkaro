import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';

class GradeBadge extends StatelessWidget {
  final String grade;
  final double size;

  const GradeBadge({super.key, required this.grade, this.size = 36});

  @override
  Widget build(BuildContext context) {
    final color = AppColors.forGrade(grade);
    final bg    = AppColors.bgForGrade(grade);
    return Container(
      width: size, height: size,
      decoration: BoxDecoration(color: bg, borderRadius: BorderRadius.circular(size * 0.25)),
      alignment: Alignment.center,
      child: Text(
        grade.toUpperCase(),
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.w900,
          fontSize: size * 0.45,
          fontFamily: 'Poppins',
        ),
      ),
    );
  }
}
