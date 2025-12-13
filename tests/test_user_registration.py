import unittest
from User_Registration import UserRegistration
from Order_Placement import Cart, OrderPlacement, RestaurantMenu
from stubs.RestaurantMenuStub import UserProfileStub

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        self.registration = UserRegistration()

    def test_successful_registration(self):
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Registration successful, confirmation email sent")

    def test_invalid_email(self):
        result = self.registration.register("userexample.com", "Password123", "Password123")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Invalid email format")

    def test_password_mismatch(self):
        result = self.registration.register("user@example.com", "Password123", "Password321")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Passwords do not match")

    def test_weak_password(self):
        result = self.registration.register("user@example.com", "pass", "pass")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Password is not strong enough")

    def test_email_already_registered(self):
        self.registration.register("user@example.com", "Password123", "Password123")
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result['success'])
        self.assertEqual(result['error'], "Email already registered")

# Standalone test
def test_proceed_to_checkout_returns_address():
    from Order_Placement import Cart, OrderPlacement, RestaurantMenu
    cart = Cart()
    menu_stub = RestaurantMenu()
    user_stub = UserProfileStub("Test Address 42")
    order = OrderPlacement(user=user_stub, menu=menu_stub, payment_method=None)
    checkout = order.proceed_to_checkout()
    assert checkout["delivery_address"] == "Test Address 42"

if __name__ == '__main__':
    unittest.main()
