# Non-functional system test for performance under load - Roope Kuossari

import time
import unittest
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
            cart = Cart()
            menu = RestaurantMenu()
            user = UserProfileStub(f"User {i} Address")
            payment = FakePaymentGateway()

            order = OrderPlacement(user=user, menu=menu, payment_method=payment)
            order.add_item(item_id=1, quantity=1)
            order.confirm_order()

        end_time = time.time()
        total_time = end_time - start_time

        # Performance criteria
        self.assertLess(total_time, 5.0)  # Example threshold: < 5 seconds
