import unittest
from merchant import get_gateway


TEST_AMOUNT = 0.01


class TestBitcoinGateway(unittest.TestCase):

    def setUp(self):
        self.merchant = get_gateway("bitcoin")
        self.address = self.merchant.get_new_address()

    def testPurchase(self):
        self.merchant.connection.sendtoaddress(self.address, TEST_AMOUNT)
        resp = self.merchant.purchase(TEST_AMOUNT, self.address)
        self.assertEquals(resp['status'], 'SUCCESS')
