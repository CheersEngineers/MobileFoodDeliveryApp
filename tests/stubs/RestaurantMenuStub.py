# tests/stubs/RestaurantMenuStub.py
# A stub for RestaurantMenu used in testing OrderPlacement
import pytest
from Order_Placement import Cart, OrderPlacement, UserProfile


class MenuStub:
    def is_item_available(self, name): return False
order = OrderPlacement(Cart, UserProfile, MenuStub())
with pytest.raises(ValueError):
    order.validate_order()
