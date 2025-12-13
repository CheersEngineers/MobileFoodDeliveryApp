# tests/test_order_placement.py
import unittest
from unittest import mock
from Order_Placement import Cart, CartItem, OrderPlacement, PaymentMethod, UserProfile, RestaurantMenu
from fakes.FakePaymentGateway import FakePaymentGateway

class SampleUser(UserProfile):
    def __init__(self):
        self.id = 1
        self.delivery_address = "123 Test Street"

class SampleMenu(RestaurantMenu):
    def __init__(self):
        super().__init__()
        self.items = [{"id": 1, "name": "Pizza", "price": 9.5}]

class TestOrderPlacement(unittest.TestCase):
    def test_confirm_calls_payment_gateway(self):
        """
        Test that confirming an order calls the payment gateway with correct parameters.
        """
        fake_payment = mock.Mock()
        fake_payment.charge.return_value = {"status": "success", "tx": "abc"}
        
        user = SampleUser()
        menu = SampleMenu()
        order = OrderPlacement(user=user, menu=menu, payment_method=fake_payment)
        order.add_item(item_id=1, quantity=2)
        
        result = order.confirm_order()
        
        fake_payment.charge.assert_called_once()
        fake_payment.charge.assert_called_with(amount=19.0, currency="EUR", metadata={"user_id": 1})
        self.assertEqual(result["status"], "success")

    def test_fake_payment_success(self):
        """
        Test the FakePaymentGateway for a successful payment scenario.
        """
        user = SampleUser()
        menu = SampleMenu()
        fake_gateway = FakePaymentGateway()
        order = OrderPlacement(user=user, menu=menu, payment_method=fake_gateway)
        order.add_item(item_id=1, quantity=1)
        
        res = order.confirm_order()
        
        self.assertEqual(res["status"], "success")
        self.assertEqual(fake_gateway.charges[0]["amount"], menu.items[0]["price"])

if __name__ == "__main__":
    unittest.main()
