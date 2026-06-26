import 'package:flutter/material.dart';

class AppColors {
  static const brandBlue      = Color(0xFF1B3F8A);
  static const brandOrange    = Color(0xFFFF9933);
  // Website `primary` = Indian flag green (#138808) — used for Cosmetic Analysis,
  // step-3 circle, "100% Free" stat, check-ingredient search button, etc.
  static const brandGreen     = Color(0xFF138808);
  static const brandGreenLight = Color(0xFFE8F5E9);
  static const gradeA         = Color(0xFF16a34a);
  static const gradeB         = Color(0xFF0891b2);
  static const gradeC         = Color(0xFFd97706);
  static const gradeD         = Color(0xFFdc2626);
  static const gradeBgA       = Color(0xFFdcfce7);
  static const gradeBgB       = Color(0xFFe0f2fe);
  static const gradeBgC       = Color(0xFFfef3c7);
  static const gradeBgD       = Color(0xFFfef2f2);
  static const surface        = Color(0xFFf9fafb);
  static const border         = Color(0xFFe5e7eb);
  static const textPrimary    = Color(0xFF0D1B2A);
  static const textMuted      = Color(0xFF6b7280);

  static Color forGrade(String grade) {
    switch (grade.toUpperCase()) {
      case 'A': return gradeA;
      case 'B': return gradeB;
      case 'C': return gradeC;
      default:  return gradeD;
    }
  }

  static Color bgForGrade(String grade) {
    switch (grade.toUpperCase()) {
      case 'A': return gradeBgA;
      case 'B': return gradeBgB;
      case 'C': return gradeBgC;
      default:  return gradeBgD;
    }
  }
}

class AppTheme {
  static ThemeData get light => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.brandBlue,
      primary: AppColors.brandBlue,
      secondary: AppColors.brandOrange,
      surface: Colors.white,
    ),
    fontFamily: 'Poppins',
    scaffoldBackgroundColor: AppColors.surface,
    appBarTheme: const AppBarTheme(
      backgroundColor: Colors.white,
      foregroundColor: AppColors.textPrimary,
      elevation: 0,
      centerTitle: false,
      titleTextStyle: TextStyle(
        fontFamily: 'Poppins',
        fontSize: 18,
        fontWeight: FontWeight.w700,
        color: AppColors.brandBlue,
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.white,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.border),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.brandBlue, width: 1.5),
      ),
    ),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.brandBlue,
        foregroundColor: Colors.white,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
        textStyle: const TextStyle(fontFamily: 'Poppins', fontWeight: FontWeight.w700),
      ),
    ),
    bottomNavigationBarTheme: const BottomNavigationBarThemeData(
      backgroundColor: Colors.white,
      selectedItemColor: AppColors.brandBlue,
      unselectedItemColor: AppColors.textMuted,
      type: BottomNavigationBarType.fixed,
      elevation: 8,
    ),
  );
}
