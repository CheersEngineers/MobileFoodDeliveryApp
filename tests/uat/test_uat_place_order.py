# UAT test for order placement - Roope Kuossari
# User story: As a user, I want to place an order so that I can receive food delivery.

import unittest
from Order_Placement import Cart, OrderPlacement, RestaurantMenu
from tests.fakes.FakePaymentGateway import FakePaymentGateway
from tests.stubs.RestaurantMenuStub import UserProfileStub

class TestUATPlaceOrder(unittest.TestCase):
    """
    UAT Test:
    User places an order and receives confirmation.
    """

    def test_user_places_order_successfully(self):
        cart = Cart()
        menu = RestaurantMenu()
        user = UserProfileStub("UAT Street 99")
        payment = FakePaymentGateway()

        order = OrderPlacement(user=user, menu=menu, payment_method=payment)
        order.add_item(item_id=1, quantity=2)

        result = order.confirm_order()

        self.assertEqual(result["status"], "success")
        self.assertEqual(len(payment.charges), 1)

if __name__ == "__main__":
    unittest.main()
