import unittest
from unittest import mock  # Import the mock module to simulate payment gateway responses.
from Payment_Processing  import PaymentProcessing
from stubs.RestaurantMenuStub import PaymentStub

# Unit tests for PaymentProcessing class
class TestPaymentProcessing(unittest.TestCase):
    """
    Unit tests for the PaymentProcessing class to ensure payment validation and processing work correctly.
    """
    def setUp(self):
        """
        Sets up the test environment by creating an instance of PaymentProcessing.
        """
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        """
        Test case for successful validation of a valid payment method ('credit_card') with valid details.
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertTrue(result)

    def test_validate_payment_method_invalid_gateway(self):
        """
        Test case for validation failure due to an unsupported payment method ('bitcoin').
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method("bitcoin", payment_details)
        self.assertEqual(str(context.exception), "Invalid payment method")

    def test_validate_credit_card_invalid_details(self):
        """
        Test case for validation failure due to invalid credit card details (invalid card number and CVV).
        """
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}  # Invalid card number and CVV.
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)

    def test_process_payment_success(self):
        """
        Test case for successful payment processing with a valid credit card.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}) as mocked_gateway:
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            
            # Behavior assertions
            self.assertEqual(result, "Payment successful, Order confirmed")
            mocked_gateway.assert_called_once_with("credit_card", payment_details, order["total_amount"])

    def test_process_payment_failure(self):
        """
        Test case for payment failure due to a declined credit card.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}

        # Patch the gateway to simulate a declined payment
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}) as mocked_gateway:
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)

        # Assertions
        self.assertEqual(result, "Payment failed, please try again")
        # Ensure the mocked gateway was called with (payment_method, payment_details, amount)
        mocked_gateway.assert_called_once_with("credit_card", payment_details, order["total_amount"])

        # Check that the order was not marked confirmed or paid
        self.assertNotIn("confirmation_id", order)
        self.assertNotEqual(order.get("status"), "confirmed")

    def test_process_payment_invalid_method(self):
        """
        Test case for payment processing failure due to an invalid payment method ('bitcoin').
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # No need for mocking, the method will raise an error directly.
        result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
        self.assertIn("Error: Invalid payment method", result)

    def test_validate_paypal_success(self):
        payment_details = {"email": "user@example.com"}
        result = self.payment_processing.validate_payment_method("paypal", payment_details)
        self.assertTrue(result)

    def test_confirm_order_success_with_stub(self):
        """
        Test confirming an order with a successful payment using PaymentStub.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_stub = PaymentStub(should_succeed=True)

        result = self.order.confirm_order(payment_stub)

        self.assertTrue(result["success"])
        self.assertEqual(result["message"], "Order confirmed")

    def test_confirm_order_failure_with_stub(self):
        """
        Test confirming an order with a failed payment using PaymentStub.
        """
        self.cart.add_item("Pizza", 12.99, 1)
        payment_stub = PaymentStub(should_succeed=False)

        result = self.order.confirm_order(payment_stub)

        self.assertFalse(result["success"])
        self.assertEqual(result["message"], "Payment failed")


if __name__ == "__main__":
    unittest.main()  # Run the unit tests.
