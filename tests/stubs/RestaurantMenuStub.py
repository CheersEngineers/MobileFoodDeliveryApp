# tests/stubs/RestaurantMenuStub.py

class MenuStub:
    def is_item_available(self, name):
        return False

class PaymentStub:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed

    def process_payment(self, amount):
        return self.should_succeed

class UserProfileStub:
    def __init__(self, address="Test Address 42"):
        self.delivery_address = address
