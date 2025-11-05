# tests/fakes/FakePaymentGateway.py

# A fake payment gateway for testing purposes
from Order_Placement import OrderPlacement


class FakePaymentGateway:
    def __init__(self):
        self.charges = []

    def charge(self, amount, currency="EUR", metadata=None):
        """
        Record a charge and return a fake response.
        """
        self.charges.append({"amount": amount, "currency": currency, "metadata": metadata})
        if amount <= 0:
            return {"status": "failure", "reason": "invalid_amount"}
        return {"status": "success", "transaction_id": f"fake-{len(self.charges)}"}

    # Backwards-compatible alias if some code uses process_payment
    def process_payment(self, amount):
        return self.charge(amount)