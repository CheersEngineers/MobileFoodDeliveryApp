# tests/fakes/FakePaymentGateway.py

class FakePaymentGateway:
    def __init__(self):
        self.charges = []

    def charge(self, amount, currency="EUR", metadata=None):
        self.charges.append({"amount": amount, "currency": currency, "metadata": metadata})
        if amount <= 0:
            return {"status": "failure", "reason": "invalid_amount"}
        return {"status": "success", "transaction_id": f"fake-{len(self.charges)}"}

    def process_payment(self, amount):
        return self.charge(amount)
