from Order_Placement import Cart, CartItem, OrderPlacement, PaymentMethod, UserProfile, RestaurantMenu
import unittest
from unittest import mock  # Import the mock module for simulating payment failures in tests.
from fakes.FakePaymentGateway import FakePaymentGateway

class TestOrderPlacement(unittest.TestCase):
    def test_confirm_calls_payment_gateway(mocker, sample_user, sample_menu):
        """
        Test that confirming an order calls the payment gateway with correct parameters.
        """
        fake_payment = mocker.Mock()
        fake_payment.charge.return_value = {"status": "success", "tx": "abc"}
        order = OrderPlacement(user=sample_user, menu=sample_menu, payment_method=fake_payment)
        order.add_item(item_id=1, quantity=2)
        result = order.confirm_order()
        fake_payment.charge.assert_called_once()
        fake_payment.charge.assert_called_with(amount=19.0, currency="EUR", metadata={"user_id": 1})
        assert result["status"] == "success"

    def test_fake_payment_success(sample_user, sample_menu):
        """
        Test the FakePaymentGateway for a successful payment scenario.
        """
        fake_gateway = FakePaymentGateway()
        order = OrderPlacement(user=sample_user, menu=sample_menu, payment_method=fake_gateway)
        order.add_item(item_id=1, quantity=1)
        res = order.confirm_order()
        assert res["status"] == "success"
        assert fake_gateway.charges[0]["amount"] == sample_menu.items[0]["price"]
if __name__ == "__main__":
    unittest.main()  # Run the unit tests.