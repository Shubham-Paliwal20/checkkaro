import requests, re, urllib.parse, time, json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml',
}

def ddg_image(query):
    s = requests.Session()
    s.headers.update(HEADERS)
    enc = urllib.parse.quote_plus(query)

    # Step 1: get vqd token
    r = s.get(f'https://duckduckgo.com/?q={enc}&ia=images', timeout=10)
    m = re.search(r'vqd=([^&"\s]+)', r.text)
    if not m:
        print('No VQD found')
        return None
    vqd = m.group(1)
    print(f'VQD: {vqd[:30]}...')

    time.sleep(0.8)

    # Step 2: image search API
    api_url = 'https://duckduckgo.com/i.js'
    params = {
        'l': 'wt-wt',
        'o': 'json',
        'q': query,
        'vqd': vqd,
        'f': ',,,,,',
        'p': '1',
    }
    r2 = s.get(api_url, params=params, timeout=10,
               headers={**HEADERS, 'Referer': f'https://duckduckgo.com/?q={enc}&ia=images'})
    print(f'API status: {r2.status_code}')
    print(f'API content length: {len(r2.text)}')
    print(f'First 300 chars: {r2.text[:300]}')

    if r2.status_code == 200 and r2.text.strip():
        try:
            data = r2.json()
            results = data.get('results', [])
            print(f'Results count: {len(results)}')
            if results:
                print(f'First image: {results[0].get("image", "N/A")}')
                return results[0].get('image')
        except Exception as e:
            print(f'JSON parse error: {e}')
    return None

url = ddg_image('KitKat 4 Finger chocolate bar India')
print(f'\nFinal URL: {url}')
