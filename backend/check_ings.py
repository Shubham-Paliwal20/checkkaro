import sys; sys.path.insert(0,'.')
from routes.ingredient_database import INGREDIENT_DESCRIPTIONS, classify_ingredient, _normalize_ins

print("=== Normalization ===")
for t in ['ins 1101', 'ins 1101(i)', 'ins 516', 'ins 500(ii)', 'ins 442', 'ins 322', 'ins 476']:
    print('  %r -> %r' % (t, _normalize_ins(t)))

print("\n=== Classifications ===")
tests = [
    ('ins 1101', 'Food'), ('ins 1101(i)', 'Food'), ('ins 516', 'Food'), ('ins 500(ii)', 'Food'),
    ('emulsifier 442', 'Food'), ('ins 442', 'Food'), ('ins 322', 'Food'),
    ('pgpr', 'Food'), ('liquid glucose', 'Food'),
    ('emulsifiers', 'Food'), ('stabilizers', 'Food'), ('stabilisers', 'Food'),
    ('cheesecake flavor', 'Food'), ('cheesecake flavour', 'Food'),
    ('refined wheat flour', 'Food'), ('maida', 'Food'),
    ('whole wheat flour', 'Food'), ('wheat flour', 'Food'),
    ('flour treatment agent', 'Food'), ('fungal alpha amylase', 'Food'),
    ('calcium sulphate', 'Food'),
]
for name, cat in tests:
    cls = classify_ingredient(name, cat)
    desc = INGREDIENT_DESCRIPTIONS.get(_normalize_ins(name.lower()), INGREDIENT_DESCRIPTIONS.get(name.lower(), None))
    print('  %-30s -> %-25s  desc=%s' % (name, cls['classification'], 'YES' if desc else 'no'))
