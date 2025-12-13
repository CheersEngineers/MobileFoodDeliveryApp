import unittest
import time
from Order_Placement import Cart, PaymentMethod, UserProfile, RestaurantMenu, OrderPlacement

# 1. Functional Bottom-Up Test Hanna
class TestBottomUpPaymentFlow(unittest.TestCase):

    def test_payment_confirmation_flow(self):
        cart = Cart()
        cart.add_item("Pizza", 10.0, 1)

        payment = PaymentMethod()  
        user_profile = UserProfile("Test Street 1")
        menu = RestaurantMenu(["Pizza"])

        order = OrderPlacement(cart, user_profile, menu)

        result = order.confirm_order(payment)

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")


# 2. Non-Functional Bottom-Up Test Hanna
class TestBottomUpPerformance(unittest.TestCase):

    def test_multiple_orders_processed_quickly(self):
        user_profile = UserProfile("Test Street 1")
        menu = RestaurantMenu(["Burger"])

        start = time.time()

        for _ in range(1000):  # simulating 1000 orders
            cart = Cart()
            cart.add_item("Burger", 5.0, 1)
            payment = PaymentMethod()

            order = OrderPlacement(cart, user_profile, menu)
            order.confirm_order(payment)

        duration = time.time() - start

        self.assertTrue(duration < 1.0, f"Too slow: {duration} seconds")


if __name__ == "__main__":
    unittest.main()