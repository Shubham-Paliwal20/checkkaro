import sys
sys.path.insert(0, 'backend')
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

# Test with clean INS numbers
raw_ins = ["e503ii", "e500ii", "e322", "e471", "e223", "yeast",
           "ammonium bicarbonate", "sodium bicarbonate",
           "lecithin", "soy lecithin",
           "mono and diglycerides", "sodium metabisulphite"]

for key in raw_ins:
    in_desc = key in INGREDIENT_DESCRIPTIONS
    result = classify_ingredient(key)
    cls = result.get('classification', '?') if isinstance(result, dict) else result
    wi = result.get('what_it_is', '') if isinstance(result, dict) else ''
    print(f"  {key:35s}  in_db={in_desc}  cls={cls}  what={wi[:30]}")
