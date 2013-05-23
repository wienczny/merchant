import mock
import urllib2
import unittest

from merchant import get_gateway, CreditCard
from merchant.gateway import CardNotSupported
from merchant.gateways.authorize_net_gateway import (
    AuthorizeAIMResponse, MockAuthorizeAIMResponse
)
from merchant.utils.credit_card import Visa


class TestAuthorizeNetAIMGateway(unittest.TestCase):

    def setUp(self):
        self.merchant = get_gateway("authorize_net")
        self.merchant.test_mode = True
        self.credit_card = CreditCard(first_name="Test", last_name="User",
                                      month=10, year=2020,
                                      number="4222222222222",
                                      verification_value="100")

    def test_card_supported(self):
        self.credit_card.number = "5019222222222222"
        self.assertRaises(CardNotSupported,
                          lambda: self.merchant.purchase(1000, self.credit_card))

    def test_card_validated(self):
        self.merchant.test_mode = False
        self.credit_card.number = "4222222222222123"
        self.assertFalse(self.merchant.validate_card(self.credit_card))

    def test_card_type(self):
        self.merchant.validate_card(self.credit_card)
        self.assertEquals(self.credit_card.card_type, Visa)

    def test_purchase(self):
        resp = self.merchant.purchase(1, self.credit_card)
        self.assertEquals(resp["status"], "SUCCESS")
        # In test mode, the transaction ID from Authorize.net is 0
        self.assertEquals(resp["response"].transaction_id, "0")
        self.assertTrue(isinstance(resp["response"], AuthorizeAIMResponse))

    def test_credit_card_expired(self):
        resp = self.merchant.purchase(8, self.credit_card)
        self.assertNotEquals(resp["status"], "SUCCESS")

    def test_purchase_url_error(self):
        with mock.patch('billing.gateways.authorize_net_gateway.urllib2.urlopen') as mock_urlopen:
            error_text = "Something bad happened :("
            mock_urlopen.side_effect = urllib2.URLError(error_text)
            resp = self.merchant.purchase(1, self.credit_card)
            self.assertEquals(resp["status"], "FAILURE")
            self.assertEquals(resp["response"].response_code, 5)
            self.assertEquals(resp["response"].response_reason_code, '1')
            self.assertTrue(error_text in resp["response"].response_reason_text)
            self.assertTrue(isinstance(resp["response"], MockAuthorizeAIMResponse))
