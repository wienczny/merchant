import unittest

from merchant import get_gateway, CreditCard
from merchant.gateway import CardNotSupported
from merchant.utils.credit_card import Visa

fake_options = {
    "email": "testuser@fakedomain.com",
    "billing_address": {
        "name": "PayPal User",
        "address1": "Street 1",
        "city": "Mountain View",
        "state": "CA",
        "country": "US",
        "zip": "94043",
        "fax": "1234567890",
        "email": "testuser@fakedomain.com",
        "phone": "1234567890",
        "mobile": "1234567890",
        "customer_ref": "Blah",
        "job_desc": "Job",
        "comments": "comments",
        "url": "http://google.com.au/",
        },
    "invoice": "1234",
    "description": "Blah Blah!",
}


class TestEWayGateway(unittest.TestCase):
    def setUp(self):
        self.merchant = get_gateway("eway")
        self.merchant.test_mode = True
        self.credit_card = CreditCard(first_name="Test", last_name="User",
                                      month=10, year=2020,
                                      number="4444333322221111",
                                      verification_value="100")

    def testCardSupported(self):
        self.credit_card.number = "5019222222222222"
        self.assertRaises(CardNotSupported,
                          lambda: self.merchant.purchase(1000, self.credit_card))

    def testCardValidated(self):
        self.merchant.test_mode = False
        self.credit_card.number = "4222222222222123"
        self.assertFalse(self.merchant.validate_card(self.credit_card))

    def testCardType(self):
        self.merchant.validate_card(self.credit_card)
        self.assertEquals(self.credit_card.card_type, Visa)

    def testPurchase(self):
        resp = self.merchant.purchase(1, self.credit_card,
                                      options=fake_options)
        # Eway test gateway sets the transaction status as failure
        # in test mode
        self.assertEquals(resp["status"], "FAILURE")
        self.assertEquals(resp["response"].ewayTrxnError,
                          "1,Do Not Honour(Test Gateway)")
        self.assertNotEquals(resp["response"].ewayTrxnNumber, "0")
        self.assertTrue(resp["response"].ewayReturnAmount, "1")

    def testCreditCardExpired(self):
        resp = self.merchant.purchase(8, self.credit_card,
                                      options=fake_options)
        self.assertNotEquals(resp["status"], "SUCCESS")
