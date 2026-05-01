"""Quick test of the grading system on representative products."""
from grading import calculate_grade, grade_to_legacy_score, grade_meta

tests = [
    ('Haagen-Dazs Vanilla (clean)',
     [{'name':'Fresh Cream','classification':'generally_recognised'},
      {'name':'Condensed Skimmed Milk','classification':'generally_recognised'},
      {'name':'Sugar','classification':'generally_recognised'},
      {'name':'Egg Yolk','classification':'generally_recognised'}]),
    ('Havmor Vanilla (emulsifiers)',
     [{'name':'Milk Solids','classification':'generally_recognised'},
      {'name':'Sugar','classification':'generally_recognised'},
      {'name':'Emulsifier E471','classification':'commonly_questioned'},
      {'name':'Stabilizer E412','classification':'commonly_questioned'},
      {'name':'Stabilizer E407','classification':'commonly_questioned'}]),
    ('Lays Chips (moderate)',
     [{'name':'Potato','classification':'generally_recognised'},
      {'name':'Palmolein Oil','classification':'worth_knowing'},
      {'name':'Salt','classification':'generally_recognised'},
      {'name':'Monosodium Glutamate','classification':'commonly_questioned'},
      {'name':'Artificial Colour','classification':'commonly_questioned'}]),
    ('Synthetic dyes (heavy CQ)',
     [{'name':'Tartrazine E102','classification':'commonly_questioned'},
      {'name':'Sunset Yellow E110','classification':'commonly_questioned'},
      {'name':'Allura Red E129','classification':'commonly_questioned'},
      {'name':'Sugar','classification':'generally_recognised'},
      {'name':'Titanium Dioxide E171','classification':'commonly_questioned'}]),
    ('Himalaya Neem Face Wash',
     [{'name':'Aqua','classification':'generally_recognised'},
      {'name':'Neem Extract','classification':'worth_knowing'},
      {'name':'Cocamidopropyl Betaine','classification':'generally_recognised'},
      {'name':'Glycerin','classification':'generally_recognised'},
      {'name':'Phenoxyethanol','classification':'commonly_questioned'},
      {'name':'Turmeric Extract','classification':'worth_knowing'}]),
    ('Product with banned ingredient',
     [{'name':'Triclosan','classification':'banned'},
      {'name':'Water','classification':'generally_recognised'},
      {'name':'Glycerin','classification':'generally_recognised'}]),
    ('Parle-G Biscuit',
     [{'name':'Wheat Flour','classification':'generally_recognised'},
      {'name':'Sugar','classification':'generally_recognised'},
      {'name':'Palm Oil','classification':'worth_knowing'},
      {'name':'Invert Sugar Syrup','classification':'worth_knowing'},
      {'name':'Milk Solids','classification':'generally_recognised'},
      {'name':'Salt','classification':'generally_recognised'},
      {'name':'Soy Lecithin','classification':'generally_recognised'}]),
]

print("\n" + "="*80)
print("GRADING SYSTEM TEST RESULTS".center(80))
print("="*80)
print(f"{'Product Name':<35} Grade  Score  Label".ljust(80))
print("-"*80)

for name, ings in tests:
    grade = calculate_grade(ings)
    score = grade_to_legacy_score(grade)
    label = grade_meta(grade)['label']
    cq_count = sum(1 for i in ings if i['classification']=='commonly_questioned')
    total = len(ings)

    print(f"{name:<35} {grade:>5}  {score:>4}   {label:<12} [{cq_count}/{total} CQ]")

print("="*80)
print("\nGrading Formula:")
print("  >= 85% clean → Grade A (Excellent)")
print("  >= 70% clean → Grade B (Good)")
print("  >= 50% clean → Grade C (Average)")
print("  <  50% clean → Grade D (Poor)")
print("\nClean weight calculation:")
print("  generally_recognised  → 1.0")
print("  worth_knowing         → 1.0")
print("  commonly_questioned (mild)  → 0.5")
print("  commonly_questioned (heavy) → 0.0")
print("  banned → auto Grade D")
print("="*80 + "\n")
