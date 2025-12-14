# repro_tc_a1.py
"""
Reproduction script for TC-A1 (Search returns only 1 matching restaurant).
- Ensures at least two matching restaurants exist (seeds if needed).
- Runs the search query used in TC-A1.
- Writes CSV, a detailed log, and an optional PNG "screenshot" to reports/.
- Designed to be robust to small API differences in your RestaurantDatabase class.
"""

import os
import csv
import time
from datetime import datetime, timezone

from Restaurant_Browsing import RestaurantDatabase, RestaurantBrowsing, RestaurantSearch

OUT_DIR = "reports"
CSV_OUT = os.path.join(OUT_DIR, "TC-A1_results.csv")
LOG_OUT = os.path.join(OUT_DIR, "TC-A1_log.txt")

os.makedirs(OUT_DIR, exist_ok=True)


def list_restaurants_flexible(db):
    """Return a list of restaurant dicts using several possible APIs/attributes."""
    for name in ("list_all_restaurants", "list_restaurants", "get_all", "all_restaurants", "all"):
        fn = getattr(db, name, None)
        if callable(fn):
            try:
                return fn()
            except Exception:
                pass

    for attr in ("restaurants", "_restaurants", "data", "_data"):
        if hasattr(db, attr):
            val = getattr(db, attr)
            if callable(val):
                try:
                    return val()
                except Exception:
                    pass
            if isinstance(val, (list, tuple)):
                return list(val)
            if isinstance(val, dict):
                return list(val.values())

    try:
        browsing = RestaurantBrowsing(database=db)
        if hasattr(browsing, "list_restaurants") and callable(getattr(browsing, "list_restaurants")):
            return browsing.list_restaurants()
        if hasattr(browsing, "search_by_filters") and callable(getattr(browsing, "search_by_filters")):
            try:
                return browsing.search_by_filters(None, None, None)
            except Exception:
                pass
    except Exception:
        pass

    raise AttributeError("Could not find a method or attribute to list restaurants on RestaurantDatabase")


def create_restaurant_flexible(db, entry):
    """Create a restaurant using common create APIs on db or browsing layer."""
    for name in ("create_restaurant", "add_restaurant", "insert_restaurant", "save_restaurant"):
        fn = getattr(db, name, None)
        if callable(fn):
            try:
                return fn(entry)
            except Exception:
                pass

    try:
        browsing = RestaurantBrowsing(database=db)
        if hasattr(browsing, "create_restaurant") and callable(getattr(browsing, "create_restaurant")):
            return browsing.create_restaurant(entry)
    except Exception:
        pass

    raise AttributeError("Could not find a method to create a restaurant on RestaurantDatabase")


def seed_two_japanese_downtown(db):
    """
    Ensure there are at least two Japanese restaurants in Downtown with rating >= 4.0.
    Returns (pre_existing_matches, created_entries)
    """
    existing = list_restaurants_flexible(db)
    matches = [
        r for r in existing
        if (r.get("cuisine") == "Japanese" or r.get("cuisine_type") == "Japanese")
        and (r.get("location") == "Downtown" or r.get("area") == "Downtown")
        and float(r.get("rating", 0)) >= 4.0
    ]

    created = []
    if len(matches) < 2:
        needed = 2 - len(matches)
        for i in range(needed):
            new = {
                "name": f"UAT Japanese Downtown {int(time.time()) % 10000}-{i}",
                "cuisine": "Japanese",
                "location": "Downtown",
                "rating": 4.5,
                "menu": []
            }
            try:
                create_restaurant_flexible(db, new)
                created.append(new)
            except Exception as e:
                with open(LOG_OUT, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now(timezone.utc).isoformat()}] Create failed: {e}\n")
    return matches, created


def run_tc_a1():
    db = RestaurantDatabase()
    browsing = RestaurantBrowsing(database=db)
    rs = RestaurantSearch(browsing=browsing)

    pre_matches, created = seed_two_japanese_downtown(db)

    try:
        matches_after = list_restaurants_flexible(db)
    except Exception as e:
        matches_after = []
        with open(LOG_OUT, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now(timezone.utc).isoformat()}] ERROR listing restaurants after seeding: {e}\n")

    matching_rows = [
        r for r in matches_after
        if (r.get("cuisine") == "Japanese" or r.get("cuisine_type") == "Japanese")
        and (r.get("location") == "Downtown" or r.get("area") == "Downtown")
        and float(r.get("rating", 0)) >= 4.0
    ]

    with open(LOG_OUT, "a", encoding="utf-8") as f:
        f.write("\n--- DB check after seeding ---\n")
        f.write(f"Checked at: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"Pre-seed matches: {len(pre_matches)}\n")
        f.write(f"Created entries: {len(created)}\n")
        f.write(f"Matching rows after seeding: {len(matching_rows)}\n")
        for r in matching_rows:
            f.write(f" - {r.get('name')} id={r.get('id', 'n/a')} rating={r.get('rating')}\n")

    query = {"cuisine": "Japanese", "location": "Downtown", "rating": 4.0}
    start = time.perf_counter()
    try:
        results = rs.search_restaurants(cuisine=query["cuisine"], location=query["location"], rating=query["rating"])
        status = "OK"
    except Exception as e:
        results = []
        status = f"ERR: {e}"
    elapsed_ms = (time.perf_counter() - start) * 1000.0

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "query_cuisine", "query_location", "query_rating", "status", "elapsed_ms", "result_count"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), query["cuisine"], query["location"], query["rating"], status, f"{elapsed_ms:.3f}", len(results)])

    with open(LOG_OUT, "a", encoding="utf-8") as f:
        f.write("\n--- Query run ---\n")
        f.write(f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n")
        f.write(f"Query: cuisine={query['cuisine']}, location={query['location']}, rating={query['rating']}\n")
        f.write(f"Status: {status}\n")
        f.write(f"Elapsed ms: {elapsed_ms:.3f}\n")
        f.write(f"Result count: {len(results)}\n")
        f.write("\nResults detail (first 50):\n")
        for r in results[:50]:
            if isinstance(r, dict):
                name = r.get("name", "<no-name>")
                rid = r.get("id", "n/a")
                rating = r.get("rating", "n/a")
                f.write(f" - {name} id={rid} rating={rating}\n")
            else:
                f.write(f" - {r}\n")

    print("Reproduction run complete.")
    print(f"CSV: {CSV_OUT}")
    print(f"Log: {LOG_OUT}")
    print(f"Result count: {len(results)}")


if __name__ == "__main__":
    run_tc_a1()
