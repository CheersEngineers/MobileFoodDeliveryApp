# tests/stubs/RestaurantMenuStub.py
# A stub for RestaurantMenu used in testing OrderPlacement
import pytest
from Order_Placement import Cart, OrderPlacement, UserProfile


class MenuStub:
    def is_item_available(self, name): return False
order = OrderPlacement(Cart, UserProfile, MenuStub())
with pytest.raises(ValueError):
    order.validate_order()

class PaymentStub:
    def init(self, should_succeed=True):
        self.should_succeed = should_succeed

    def process_payment(self, amount):
        # Simulate the behavior of the real PaymentMethod, but simplified
        return self.should_succeed
    
class UserProfileStub:
    def init(self, address="Test Address 42"):
        self.delivery_address = address