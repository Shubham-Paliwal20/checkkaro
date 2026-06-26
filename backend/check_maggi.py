import sys
sys.path.insert(0, '.')
from routes.ingredient_database import classify_ingredient, INGREDIENT_DESCRIPTIONS

ingredients = [
    "Refined Wheat Flour",
    "Palm Oil",
    "Iodized Salt",
    "Wheat Gluten",
    "Potassium Chloride",
    "Guar Gum",
    "Potassium Carbonate",
    "Sodium Carbonate",
    "Pentasodium Triphosphate",
    "Onion Powder",
    "Coriander",
    "Turmeric",
    "Red Chilli",
    "Garlic",
    "Cumin",
    "Aniseed",
    "Ginger",
    "Fenugreek",
    "Black Pepper",
    "Clove",
    "Cardamom",
    "Nutmeg",
    "Sugar",
    "Hydrolysed Groundnut Protein",
    "Wheat Flour",
    "Starch",
    "Disodium 5'-Ribonucleotides",
    "Citric Acid",
    "Caramel IV",
    "Ferric Pyrophosphate",
    "Wheat Gluten",
]

print(f"{'Ingredient':<35} {'Classification':<25} {'In Descriptions?'}")
print("-" * 85)
for ing in ingredients:
    cls = classify_ingredient(ing)
    in_desc = any(k in ing.lower() or ing.lower() in k for k in INGREDIENT_DESCRIPTIONS)
    flag = "✓" if in_desc else "✗ MISSING"
    print(f"{ing:<35} {cls['classification']:<25} {flag}")
