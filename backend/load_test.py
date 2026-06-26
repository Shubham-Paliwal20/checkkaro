"""
CheckKaro Load Test
Tests API performance under concurrent traffic.
"""
import asyncio
import aiohttp
import time
import statistics
from datetime import datetime

BASE = "https://checkkaro.onrender.com"

ENDPOINTS = [
    ("Product Search",    f"{BASE}/api/product/search?name=maggi"),
    ("Product Search 2",  f"{BASE}/api/product/search?name=parle+g"),
    ("Product Search 3",  f"{BASE}/api/product/search?name=amul+butter"),
    ("Browse Biscuits",   f"{BASE}/api/product/browse?category=biscuits&limit=10"),
    ("Browse Snacks",     f"{BASE}/api/product/browse?category=snacks&limit=10"),
    ("Ingredient Check",  f"{BASE}/api/ingredient/check?name=sugar"),
    ("Ingredient Check2", f"{BASE}/api/ingredient/check?name=sodium+benzoate"),
    ("Suggestions",       f"{BASE}/api/product/suggestions?q=kit"),
]

results = {ep[0]: [] for ep in ENDPOINTS}
errors  = {ep[0]: 0   for ep in ENDPOINTS}

async def hit(session, name, url, semaphore):
    async with semaphore:
        t0 = time.monotonic()
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
                await r.read()
                ms = (time.monotonic() - t0) * 1000
                results[name].append((r.status, ms))
                return r.status, ms
        except Exception:
            ms = (time.monotonic() - t0) * 1000
            errors[name] += 1
            results[name].append((0, ms))
            return 0, ms

async def run_batch(concurrency, total_per_endpoint):
    sem = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for name, url in ENDPOINTS:
            for _ in range(total_per_endpoint):
                tasks.append(hit(session, name, url, sem))
        await asyncio.gather(*tasks)

def print_report():
    total_requests = sum(len(v) for v in results.values())
    total_errors   = sum(errors.values())

    print("\n" + "="*68)
    print(f"  CheckKaro Load Test Report  --  {datetime.now().strftime('%H:%M:%S')}")
    print("="*68)
    print(f"  Total requests : {total_requests}")
    print(f"  Total errors   : {total_errors}  ({100*total_errors/max(total_requests,1):.1f}% error rate)")
    print("="*68)

    print(f"\n{'Endpoint':<24} {'Reqs':>5} {'Err':>4} {'Min':>7} {'Avg':>7} {'p95':>7} {'Max':>7} {'OK%':>5}")
    print("-"*68)

    all_times = []
    for name, data in results.items():
        if not data:
            continue
        times    = [ms for _, ms in data]
        statuses = [s  for s, _ in data]
        ok       = sum(1 for s in statuses if 200 <= s < 300)
        err_cnt  = errors[name]
        mn  = min(times)
        avg = statistics.mean(times)
        p95 = sorted(times)[int(len(times) * 0.95)]
        mx  = max(times)
        ok_pct = 100 * ok / len(data)
        all_times.extend(times)
        print(f"{name:<24} {len(data):>5} {err_cnt:>4} {mn:>6.0f}ms {avg:>6.0f}ms {p95:>6.0f}ms {mx:>6.0f}ms {ok_pct:>4.0f}%")

    print("-"*68)

    if all_times:
        overall_avg = statistics.mean(all_times)
        overall_p95 = sorted(all_times)[int(len(all_times) * 0.95)]
        overall_p99 = sorted(all_times)[int(len(all_times) * 0.99)]
        print(f"\n  Overall avg : {overall_avg:.0f}ms")
        print(f"  Overall p95 : {overall_p95:.0f}ms   (95% of requests faster than this)")
        print(f"  Overall p99 : {overall_p99:.0f}ms   (99% of requests faster than this)")

        print("\n  --- Speed Rating ---")
        if overall_avg < 300:
            print("  [FAST]      avg under 300ms -- excellent for free tier")
        elif overall_avg < 800:
            print("  [OK]        avg under 800ms -- acceptable for free tier")
        elif overall_avg < 2000:
            print("  [SLOW]      avg under 2s -- backend likely cold starting")
        else:
            print("  [VERY SLOW] avg over 2s -- Render free tier sleep issue")

        print("\n  --- Reliability Rating ---")
        err_pct = 100 * total_errors / max(total_requests, 1)
        if err_pct == 0:
            print("  [EXCELLENT] 0% error rate -- rock solid under load")
        elif err_pct < 2:
            print(f"  [GOOD]      {err_pct:.1f}% error rate -- handles traffic well")
        elif err_pct < 10:
            print(f"  [OK]        {err_pct:.1f}% error rate -- some drops under heavy load")
        else:
            print(f"  [POOR]      {err_pct:.1f}% error rate -- unstable under load")

        print("\n  --- Verdict ---")
        if overall_avg < 800 and err_pct < 5:
            print("  Website handles traffic well for current user load.")
            print("  Render free tier is the bottleneck -- upgrade to paid")
            print("  tier if you expect 100+ concurrent users.")
        elif overall_avg >= 2000:
            print("  Backend is sleeping between requests (Render free tier).")
            print("  First request after idle takes 20-30s (cold start).")
            print("  Solution: upgrade Render plan or add a ping service.")
        else:
            print("  Performance is acceptable. Monitor as traffic grows.")

    print("="*68)

async def main():
    print("\nCheckKaro Load Test Starting...")
    print(f"Target: {BASE}")
    print("Sending ~500 requests across 8 endpoints in 3 phases\n")

    print("[1/3] Warm up -- waking Render backend from sleep...")
    t0 = time.monotonic()
    await run_batch(concurrency=2, total_per_endpoint=1)
    print(f"      Done in {time.monotonic()-t0:.1f}s")

    print("[2/3] Light load -- 80 requests, 10 concurrent...")
    t0 = time.monotonic()
    await run_batch(concurrency=10, total_per_endpoint=5)
    print(f"      Done in {time.monotonic()-t0:.1f}s")

    print("[3/3] Heavy load -- 480 requests, 50 concurrent...")
    t0 = time.monotonic()
    await run_batch(concurrency=50, total_per_endpoint=60)
    print(f"      Done in {time.monotonic()-t0:.1f}s")

    print_report()

if __name__ == "__main__":
    asyncio.run(main())
