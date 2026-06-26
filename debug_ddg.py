import requests, re, urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml',
}

query = 'KitKat 4 Finger chocolate bar India'
enc = urllib.parse.quote_plus(query)
s = requests.Session()
s.headers.update(HEADERS)

r = s.get(f'https://duckduckgo.com/?q={enc}&ia=images', timeout=10)
print('Status:', r.status_code)
print('Content length:', len(r.text))
print()

# Try various vqd patterns
patterns = [
    r'vqd=([\"\'])([^\"\']+)\1',
    r'"vqd":"([^"]+)"',
    r"vqd='([^']+)'",
    r'vqd=([^&"\s]+)',
    r'"vqd_3":"([^"]+)"',
]
for p in patterns:
    m = re.search(p, r.text)
    if m:
        print(f'Pattern {p!r} matched: {m.group(1 if m.lastindex == 1 else 2)!r}')
    else:
        print(f'Pattern {p!r}: no match')

print('\nFirst 800 chars:')
print(r.text[:800])
