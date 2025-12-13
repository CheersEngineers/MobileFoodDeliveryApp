# Functional system test for order placement - Roope Kuossari

import unittest
from Order_Placement import Cart, OrderPlacement, RestaurantMenu
from tests.fakes.FakePaymentGateway import FakePaymentGateway
from tests.stubs.RestaurantMenuStub import UserProfileStub

class TestSystemPlaceOrder(unittest.TestCase):
    """
    System-level functional test:
    Validates that a user can place an order successfully using
    Cart + OrderPlacement + Payment Gateway.
    """

    def setUp(self):
        self.cart = Cart()
        self.menu = RestaurantMenu()
        self.user = UserProfileStub("123 System Test Street")
        self.payment_gateway = FakePaymentGateway()

        self.order = OrderPlacement(
            user=self.user,
            menu=self.menu,
            payment_method=self.payment_gateway
        )

    def test_successful_order_flow(self):
        """
        End-to-end test:
        User adds item -> checks out -> payment succeeds -> order confirmed
        """
        self.order.add_item(item_id=1, quantity=1)
        result = self.order.confirm_order()

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(self.payment_gateway.charges), 1)
        self.assertGreater(self.payment_gateway.charges[0]["amount"], 0)

if __name__ == "__main__":
    unittest.main()
