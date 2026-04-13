"""
Extract full ingredient lists from the SQL file
This script parses the indian_products_extended.sql file and extracts all ingredients
"""

import re

# Read the SQL file
with open('database/indian_products_extended.sql', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all INSERT statements
pattern = r"\('([^']+)',\s*'([^']+)',\s*'([^']+)',\s*'([^']+)',\s*ARRAY\[([^\]]+)\]"

matches = re.findall(pattern, content)

print(f"Found {len(matches)} products with ingredients")
print("\nSample:")
for i, match in enumerate(matches[:5]):
    name, brand, category, ingredients_text, ingredients_array = match
    print(f"\n{i+1}. {name} ({brand})")
    print(f"   Category: {category}")
    # Parse the array
    ingredients = re.findall(r"'([^']+)'", ingredients_array)
    print(f"   Ingredients ({len(ingredients)}): {', '.join(ingredients[:5])}...")
