import unittest
from unittest import mock
from Payment_Processing import PaymentProcessing
from stubs.RestaurantMenuStub import PaymentStub, UserProfileStub
from Order_Placement import Cart, OrderPlacement, RestaurantMenu

class TestPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()
        self.cart = Cart()
        self.user = UserProfileStub()
        self.menu = RestaurantMenu()
        self.order = OrderPlacement(user=self.user, menu=self.menu, payment_method=None)

    def test_validate_payment_method_success(self):
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertTrue(result)

    def test_validate_payment_method_invalid_gateway(self):
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method("bitcoin", payment_details)
        self.assertEqual(str(context.exception), "Invalid payment method")

    def test_validate_credit_card_invalid_details(self):
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)

    def test_process_payment_success(self):
        order = {"total_amount": 100.0}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}) as mocked_gateway:
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")
            mocked_gateway.assert_called_once_with("credit_card", payment_details, order["total_amount"])

    def test_process_payment_failure(self):
        order = {"total_amount": 100.0}
        payment_details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}

        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}) as mocked_gateway:
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment failed, please try again")
            mocked_gateway.assert_called_once_with("credit_card", payment_details, order["total_amount"])
            self.assertNotIn("confirmation_id", order)
            self.assertNotEqual(order.get("status"), "confirmed")

    def test_process_payment_invalid_method(self):
        order = {"total_amount": 100.0}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
        self.assertIn("Error: Invalid payment method", result)

    def test_validate_paypal_success(self):
        payment_details = {"email": "user@example.com"}
        result = self.payment_processing.validate_payment_method("paypal", payment_details)
        self.assertTrue(result)

    def test_confirm_order_success_with_stub(self):
        self.cart.add_item("Pizza", 12.99, 1)
        payment_stub = PaymentStub(should_succeed=True)
        self.orde
