"""
Alternative style using monkeypatch to replace the browsing.search_by_filters method.
This verifies the forwarding of arguments and return value handling.
"""

from Restaurant_Browsing import RestaurantSearch

def test_search_forwards_args_to_search_by_filters(monkeypatch):
    captured = {}

    def fake_search_by_filters(cuisine_type=None, location=None, min_rating=None):
        captured['args'] = {
            "cuisine_type": cuisine_type,
            "location": location,
            "min_rating": min_rating
        }
        return [{"name": "Stub"}]

    class BrowsingHolder:
        pass

    holder = BrowsingHolder()
    monkeypatch.setattr(holder, "search_by_filters", fake_search_by_filters, raising=False)

    rs = RestaurantSearch(browsing=holder)
    result = rs.search_restaurants(cuisine="pizza", location="Helsinki", rating=3.5)

    assert result == [{"name": "Stub"}]
    assert captured['args'] == {"cuisine_type": "pizza", "location": "Helsinki", "min_rating": 3.5}
