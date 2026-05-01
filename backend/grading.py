"""
Shared grading utility — Clean% + Severity tiers
Grade A/B/C/D replaces the 0-100 awareness_score.

Classification tiers (unchanged):
  generally_recognised  → clean  (weight 1.0)
  worth_knowing         → clean  (weight 1.0)
  commonly_questioned   → heavy  (weight 0.0) | mild (weight 0.5)
  banned                → auto D regardless of counts

Severity split within commonly_questioned:
  CQ_HEAVY  — EU-restricted, banned in a major region, strong health evidence
  CQ_MILD   — Debated, permitted globally but commonly flagged
"""

# CQ_HEAVY: ingredients restricted/banned in EU or another major jurisdiction,
# or with strong regulatory health evidence
CQ_HEAVY_KEYWORDS = [
    # EU-banned synthetic food dyes
    'tartrazine', 'e102', 'sunset yellow', 'e110',
    'carmoisine', 'e122', 'allura red', 'e129', 'brilliant blue', 'e133',
    'e124',
    # Titanium dioxide — banned in EU food (2022)
    'titanium dioxide', 'e171',
    # Endocrine disruptors / reproductive toxins
    'phthalate', 'diethyl phthalate', 'dibutyl phthalate',
    # EU-restricted in cosmetics at high concentration
    'propylene glycol', 'polyethylene glycol', 'peg-',
    # Nitrosamines precursors
    'sodium nitrite', 'e250', 'sodium nitrate', 'e251',
    # Banned in EU/Canada bread improver
    'potassium bromate', 'e924', 'azodicarbonamide', 'e927',
    # Heavy metals
    'aluminum', 'aluminium',
    # Suspect carcinogen (IARC 2B)
    'nitrite', 'nitrate',
]

# CQ_MILD: globally permitted but commonly debated / flagged by health groups
CQ_MILD_KEYWORDS = [
    'sodium lauryl sulfate', 'sls',
    'sodium laureth sulfate', 'sles',
    'sodium benzoate', 'potassium sorbate',
    'tetrasodium edta', 'disodium edta', 'edta',
    'monosodium glutamate', 'msg',
    'disodium guanylate', 'disodium inosinate',
    'sucralose', 'acesulfame', 'aspartame', 'saccharin',
    'phenoxyethanol',
    'fragrance', 'parfum',
    'mineral oil',
    'caramel color', 'caramel colour', 'e150',
    'artificial color', 'artificial colour',
    'artificial flavor', 'artificial flavour',
    'nature identical flavor', 'nature identical flavour',
    'brominated vegetable oil',
]


def _is_heavy_cq(ingredient_name: str) -> bool:
    n = ingredient_name.lower()
    return any(kw in n for kw in CQ_HEAVY_KEYWORDS)


def calculate_grade(ingredient_objs: list) -> str:
    """
    Returns 'A', 'B', 'C', or 'D'.

    ingredient_objs: list of dicts with at least {'name': str, 'classification': str}

    Formula (Clean% with Severity):
      Each ingredient gets a clean weight:
        generally_recognised / worth_knowing  → 1.0
        commonly_questioned (mild)            → 0.5
        commonly_questioned (heavy)           → 0.0
        banned                                → 0.0 + forces grade D

    clean_pct = sum(weights) / total * 100
      >= 85  → A
      >= 70  → B
      >= 50  → C
      <  50  → D
    """
    if not ingredient_objs:
        return 'A'

    has_banned = any(
        i.get('classification') == 'banned' for i in ingredient_objs
    )
    if has_banned:
        return 'D'

    total = len(ingredient_objs)
    weighted_clean = 0.0

    for ing in ingredient_objs:
        cls = ing.get('classification', 'generally_recognised')
        if cls in ('generally_recognised', 'worth_knowing'):
            weighted_clean += 1.0
        elif cls == 'commonly_questioned':
            if _is_heavy_cq(ing.get('name', '')):
                weighted_clean += 0.0
            else:
                weighted_clean += 0.5
        # banned already handled above; anything else → 0.0

    clean_pct = (weighted_clean / total) * 100

    if clean_pct >= 85:
        return 'A'
    if clean_pct >= 70:
        return 'B'
    if clean_pct >= 50:
        return 'C'
    return 'D'


def grade_to_legacy_score(grade: str) -> int:
    """Map grade → numeric score for any legacy code that still reads awareness_score."""
    return {'A': 95, 'B': 80, 'C': 60, 'D': 30}.get(grade, 60)


def grade_meta(grade: str) -> dict:
    """Return display metadata for a grade."""
    return {
        'A': {'label': 'Excellent', 'color': '#16a34a', 'bg': '#f0fdf4',
              'desc': 'Minimal concern ingredients. Largely clean label.'},
        'B': {'label': 'Good',      'color': '#2563eb', 'bg': '#eff6ff',
              'desc': 'Mostly safe. Some commonly noted additives.'},
        'C': {'label': 'Average',   'color': '#d97706', 'bg': '#fffbeb',
              'desc': 'Mixed formulation. Several commonly questioned ingredients.'},
        'D': {'label': 'Poor',      'color': '#dc2626', 'bg': '#fef2f2',
              'desc': 'High proportion of questioned or banned ingredients.'},
    }.get(grade, {'label': 'Unknown', 'color': '#6b7280', 'bg': '#f9fafb', 'desc': ''})
