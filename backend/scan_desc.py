import sys
sys.path.insert(0, '.')
from routes.ingredient_database import INGREDIENT_DESCRIPTIONS

short = []
for name, desc in INGREDIENT_DESCRIPTIONS.items():
    if len(desc.strip()) < 350:
        short.append((name, len(desc.strip()), desc.strip()[:100]))

print(f"Total entries: {len(INGREDIENT_DESCRIPTIONS)}")
print(f"Entries under 350 chars: {len(short)}")
print()
for name, length, preview in sorted(short, key=lambda x: x[1]):
    print(f"[{length:3d}] {name}")
    print(f"     {preview}")
    print()
