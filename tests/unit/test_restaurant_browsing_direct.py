"""
Direct bottom-up tests for RestaurantBrowsing using a DummyDB.
These tests instantiate RestaurantBrowsing(database=DummyDB()) so no real DB or I/O is used.
"""

from Restaurant_Browsing import RestaurantBrowsing

class DummyDB:
    """Minimal test double that returns a controlled set of restaurants."""
    def __init__(self):
        self._restaurants = [
            {"name": "Italian Bistro", "cuisine": "Italian", "location": "Downtown", "rating": 4.5},
            {"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8},
            {"name": "Burger King", "cuisine": "Fast Food", "location": "Uptown", "rating": 4.0},
            {"name": "Taco Town", "cuisine": "Mexican", "location": "Downtown", "rating": 4.2},
            {"name": "Pizza Palace", "cuisine": "Italian", "location": "Uptown", "rating": 3.9},
        ]

    def get_restaurants(self):
        return list(self._restaurants)

def test_search_by_cuisine_returns_only_matching_cuisine():
    db = DummyDB()
    rb = RestaurantBrowsing(database=db)

    results = rb.search_by_cuisine("Italian")
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(r["cuisine"].lower() == "italian" for r in results)

def test_search_by_location_returns_only_matching_location():
    db = DummyDB()
    rb = RestaurantBrowsing(database=db)

    results = rb.search_by_location("Downtown")
    assert isinstance(results, list)
    assert len(results) == 2
    assert all(r["location"].lower() == "downtown" for r in results)

def test_search_by_rating_filters_minimum_rating():
    db = DummyDB()
    rb = RestaurantBrowsing(database=db)

    results = rb.search_by_rating(4.2)
    assert isinstance(results, list)
    expected_names = {"Sushi House", "Italian Bistro", "Taco Town"}
    assert set(r["name"] for r in results) == expected_names

def test_search_by_filters_combines_all_filters():
    db = DummyDB()
    rb = RestaurantBrowsing(database=db)

    results = rb.search_by_filters(cuisine_type="Italian", location="Downtown", min_rating=4.0)
    assert isinstance(results, list)
    assert len(results) == 1
    assert results[0]["name"] == "Italian Bistro"

def test_search_by_filters_handles_missing_filters_gracefully():
    db = DummyDB()
    rb = RestaurantBrowsing(database=db)

    results = rb.search_by_filters()
    assert isinstance(results, list)
    assert len(results) == len(db.get_restaurants())
