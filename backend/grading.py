"""
Ingredient grading — simple binary rules:

  banned / commonly_questioned present  → D (always)
  0 worth_knowing (all generally_recognised) → A
  worth_knowing ≤ 30% of total           → B
  worth_knowing > 30% of total           → C
"""


def calculate_grade(ingredient_objs: list) -> str:
    """
    Returns 'A', 'B', 'C', or 'D'.
    ingredient_objs: list of dicts with at least {'classification': str}
    """
    if not ingredient_objs:
        return 'A'

    for ing in ingredient_objs:
        cls = ing.get('classification', 'generally_recognised')
        if cls in ('banned', 'commonly_questioned'):
            return 'D'

    total = len(ingredient_objs)
    worth_count = sum(
        1 for ing in ingredient_objs
        if ing.get('classification') == 'worth_knowing'
    )

    if worth_count == 0:
        return 'A'

    worth_pct = (worth_count / total) * 100
    if worth_pct <= 30:
        return 'B'
    return 'C'


def grade_to_legacy_score(grade: str) -> int:
    """Map grade → numeric score for any legacy code that still reads awareness_score."""
    return {'A': 95, 'B': 80, 'C': 60, 'D': 30}.get(grade, 60)


def grade_meta(grade: str) -> dict:
    """Return display metadata for a grade."""
    return {
        'A': {'label': 'Excellent', 'color': '#16a34a', 'bg': '#f0fdf4',
              'desc': 'All ingredients are generally recognised as safe.'},
        'B': {'label': 'Good',      'color': '#2563eb', 'bg': '#eff6ff',
              'desc': 'Mostly clean — a few worth-knowing additives (≤30%).'},
        'C': {'label': 'Average',   'color': '#d97706', 'bg': '#fffbeb',
              'desc': 'Many worth-knowing additives (>30%). No banned/questioned ingredients.'},
        'D': {'label': 'Poor',      'color': '#dc2626', 'bg': '#fef2f2',
              'desc': 'Contains one or more commonly questioned or banned ingredients.'},
    }.get(grade, {'label': 'Unknown', 'color': '#6b7280', 'bg': '#f9fafb', 'desc': ''})
