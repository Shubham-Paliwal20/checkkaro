import sys
sys.path.insert(0, 'backend')
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS, _normalize_ins

TARGETS = [
    "Raising Agent 503(ii)",
    "Raising Agent 500(ii)",
    "Yeast",
    "Emulsifier 322",
    "Emulsifier 471",
    "Dough Conditioner (223)",
]

print("=== Normalize test ===")
for t in TARGETS:
    norm = _normalize_ins(t)
    print(f"  {t!r:40s} -> {norm!r}")

print("\n=== classify_ingredient test ===")
for t in TARGETS:
    result = classify_ingredient(t)
    in_desc = t.lower() in INGREDIENT_DESCRIPTIONS
    norm = _normalize_ins(t)
    norm_in_desc = norm in INGREDIENT_DESCRIPTIONS
    print(f"  {t!r}")
    print(f"    result      = {result!r}")
    print(f"    raw in DB   = {in_desc}")
    print(f"    norm in DB  = {norm_in_desc}  ({norm!r})")
    print()
