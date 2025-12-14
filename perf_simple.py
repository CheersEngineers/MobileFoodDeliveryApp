# perf_simple.py
import csv
import time
import statistics
from Restaurant_Browsing import RestaurantDatabase, RestaurantBrowsing, RestaurantSearch

# Configure run
ITERATIONS = 200
OUT_CSV = "reports/perf_simple_results.csv"

# Prepare objects (use real in-memory DB from your app)
db = RestaurantDatabase()
browsing = RestaurantBrowsing(database=db)
rs = RestaurantSearch(browsing=browsing)

rows = []
for i in range(1, ITERATIONS + 1):
    start = time.perf_counter()
    try:
        # call the function under test
        results = rs.search_restaurants(cuisine="Italian", location="Downtown", rating=4.0)
        status = "OK"
    except Exception as e:
        results = None
        status = "ERR"
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    rows.append((i, status, round(elapsed_ms, 2), len(results) if results is not None else 0))

# Ensure reports folder exists and write CSV
import os
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["request", "status", "ms", "result_count"])
    writer.writerows(rows)

# Print a short summary to the terminal
times = [r[2] for r in rows if r[1] == "OK"]
ok_count = sum(1 for r in rows if r[1] == "OK")
err_count = len(rows) - ok_count
avg = statistics.mean(times) if times else float("nan")
p95 = statistics.quantiles(times, n=100)[94] if len(times) >= 20 else max(times) if times else float("nan")
print(f"Ran {ITERATIONS} iterations: OK={ok_count}, ERR={err_count}")
print(f"Average ms: {avg:.2f}, P95 ms: {p95:.2f}")
print(f"Wrote CSV: {OUT_CSV}")
