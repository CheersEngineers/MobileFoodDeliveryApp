# UAT test for user registration - Roope Kuossari
# User story: As a new user, I want to register an account so that I can place orders.

import unittest
from User_Registration import UserRegistration

class TestUATUserRegistration(unittest.TestCase):
    """
    UAT Test:
    Validates user registration from an end-user perspective.
    """

    def test_user_can_register_successfully(self):
        registration = UserRegistration()
        result = registration.register(
            email="uatuser@example.com",
            password="Password123",
            confirm_password="Password123"
        )

        self.assertTrue(result["success"])
        self.assertIn("confirmation email sent", result["message"].lower())

if __name__ == "__main__":
    unittest.main()
