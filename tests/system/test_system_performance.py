# Non-functional system test for performance under load - Roope Kuossari

import sys
import os
import time
import unittest

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Order_Placement import Cart, OrderPlacement, RestaurantMenu
from tests.fakes.FakePaymentGateway import FakePaymentGateway
from tests.stubs.RestaurantMenuStub import UserProfileStub


class TestSystemPerformance(unittest.TestCase):
    """
    Non-functional system test:
    Measures system behavior under multiple order placements.
    """

    def test_multiple_orders_performance(self):
        start_time = time.time()
        orders_count = 20

        for i in range(orders_count):
            # Create cart and add item
            cart = Cart()
            cart.add_item("Pizza", 10.0, 1)

            # Menu must contain item NAMES for validation
            menu = RestaurantMenu(
                available_items=["Pizza"]
            )

            user = UserProfileStub(f"User {i} Address")
            payment = FakePaymentGateway()

            # Correct constructor usage
            order = OrderPlacement(cart, user, menu)

            # Correct payment flow
            result = order.confirm_order(payment)

            self.assertTrue(result["success"])

        total_time = time.time() - start_time

        # Performance criteria
        self.assertLess(total_time, 5.0)  # Must complete under 5 seconds
