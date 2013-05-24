import unittest

from merchant import get_gateway, CreditCard
from merchant.gateway import CardNotSupported
from merchant.utils.credit_card import Visa


class TestWePayGateway(unittest.TestCase):

    def setUp(self):
        self.merchant = get_gateway("we_pay")
        self.credit_card = CreditCard(
            first_name="Test",
            last_name="User",
            month=10, year=2020,
            number="4242424242424242",
            verification_value="100"
        )
        self.options = {
            "short_description": "Donation to Smith Cancer Fund",
            "long_description": "This is a donation to help Bob Smith get the treatment",
            "type": "DONATION",
            "reference_id": "abc123",
            "amount": "100.75",
            "app_fee": "5.5",
            "fee_payer": "payee",
            "redirect_uri": "http://www.example.com/callback/donation_success/1531",
            "callback_uri": "http://www.example.com/callback/status/1531",
            "mode": "iframe"
        }

    def test_card_type(self):
        self.credit_card.number = '4242424242424242'
        self.merchant.validate_card(self.credit_card)
        self.assertEquals(self.credit_card.card_type, Visa)

    def test_purchase(self):
        resp = self.merchant.purchase(1, self.credit_card, options=self.options)
        self.assertEquals(resp["status"], "SUCCESS")

    def test_purchase_decimal_amount(self):
        resp = self.merchant.purchase(1.99, self.credit_card, options=self.options)
        self.assertEquals(resp["status"], "SUCCESS")

    def test_authorize(self):
        options = self.options.copy()
        options.update({
            "customer": {"email": "test@example.com"},
            "billing_address": {
                "address1": "100 Main St",
                "address2": "",
                "city": "Toronto",
                "region": "ON",
                "postcode": "M4E 1Z5",
                "country": "CA"
            },
            "auto_capture": False
        })
        resp = self.merchant.authorize(100, self.credit_card, options=options)
        self.assertEquals(resp["status"], "SUCCESS")
        self.assertEquals(resp["response"]["state"], "authorized")
        self.assertIn("checkout_id", resp["response"])

    def test_void(self):
        resp = self.merchant.purchase(1, self.credit_card, options=self.options)

        self.assertEquals(resp["status"], "SUCCESS")
        self.assertIn("checkout_id", resp["response"])
        self.assertIn("checkout_uri", resp["response"])

        checkout_id = resp["response"]["checkout_id"]
        options = {"description": "Product was defective. Do not want."}
        resp = self.merchant.void(checkout_id, options=options)
        self.assertEquals(resp["status"], "SUCCESS")
