"""
Bottom-up tests for RestaurantSearch.search_restaurants.
We inject a FakeBrowsing object into RestaurantSearch so no real DB is used.
"""

from Restaurant_Browsing import RestaurantSearch

class FakeBrowsing:
    def __init__(self, return_value=None):
        self.return_value = return_value if return_value is not None else []
        self.last_called_with = None

    def search_by_filters(self, cuisine_type=None, location=None, min_rating=None):
        self.last_called_with = {
            "cuisine_type": cuisine_type,
            "location": location,
            "min_rating": min_rating
        }
        return self.return_value

def test_search_for_cuisine_and_rating_returns_results():
    fake_results = [{"name": "Sushi House", "cuisine": "Japanese", "location": "Midtown", "rating": 4.8}]
    fake = FakeBrowsing(return_value=fake_results)

    rs = RestaurantSearch(browsing=fake)

    res = rs.search_restaurants(cuisine="Japanese", location=None, rating=4.0)

    assert res == fake_results
    assert fake.last_called_with == {"cuisine_type": "Japanese", "location": None, "min_rating": 4.0}

def test_search_returns_empty_list_when_no_matches():
    fake = FakeBrowsing(return_value=[])
    rs = RestaurantSearch(browsing=fake)

    res = rs.search_restaurants(cuisine="unknown", location="nowhere", rating=5.0)

    assert res == []
    assert fake.last_called_with == {"cuisine_type": "unknown", "location": "nowhere", "min_rating": 5.0}
