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

def test_confirm_calls_payment_gateway(mocker, sample_user, sample_menu):
    fake_payment = mocker.Mock()
    fake_payment.charge.return_value = {"status": "success", "tx": "abc"}
    order = OrderPlacement(user=sample_user, menu=sample_menu, payment_method=fake_payment)
    order.add_item(item_id=1, quantity=2)
    result = order.confirm_order()
    fake_payment.charge.assert_called_once()
    fake_payment.charge.assert_called_with(amount=19.0, currency="EUR", metadata={"user_id": 1})
    assert result["status"] == "success"

def test_fake_payment_success(sample_user, sample_menu):
    fake_gateway = FakePaymentGateway()
    order = OrderPlacement(user=sample_user, menu=sample_menu, payment_method=fake_gateway)
    order.add_item(item_id=1, quantity=1)
    res = order.confirm_order()
    assert res["status"] == "success"
    assert fake_gateway.charges[0]["amount"] == sample_menu.items[0]["price"]
