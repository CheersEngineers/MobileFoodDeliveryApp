# Functional system test for order placement - Roope Kuossari

import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

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

        # Minimal valid menu
        self.menu = RestaurantMenu(
            available_items=["Pizza"]
        )

        self.user = UserProfileStub("123 System Test Street")
        self.payment_gateway = FakePaymentGateway()

        self.order = OrderPlacement(
            cart=self.cart,
            user_profile=self.user,
            restaurant_menu=self.menu
        )

    def test_successful_order_flow(self):
        """
        End-to-end system test:
        User adds item -> order validated -> payment succeeds -> order confirmed
        """
        # Add item to cart
        self.cart.add_item(name="Pizza", price=10.0, quantity=1)

        # Confirm order
        result = self.order.confirm_order(self.payment_gateway)

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")


if __name__ == "__main__":
    unittest.main()
