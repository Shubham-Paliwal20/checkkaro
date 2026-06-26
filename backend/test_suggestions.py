from routes.ingredient import _MASTER_LIST, _normalize_ins

def simulate(q, limit=8):
    q_lower = _normalize_ins(q.strip())
    if q.strip().lower().startswith('ins') and q_lower == q.strip().lower():
        q_lower = 'e'
    starts = [(k,d) for k,d in _MASTER_LIST if k.startswith(q_lower)]
    contains = [(k,d) for k,d in _MASTER_LIST if q_lower in k and not k.startswith(q_lower)]
    matched = (sorted(starts) + sorted(contains))[:limit]
    return [d for k,d in matched]

tests = ['e2', 'INS 2', 'ins', 'E102', 'sorb', 'suga', 'e4', 'e96', 'INS 960', 'datem']
for t in tests:
    print(f'  {t!r:12} -> {simulate(t)}')
