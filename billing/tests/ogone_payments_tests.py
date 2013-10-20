from django.test import TestCase
from billing import get_integration


class OgonePaymentsTestCase(TestCase):
    def setUp(self):
        self.op = get_integration("ogone_payments")
        self.data = {
            'orderID': 21,
            'ownerstate': '',
            'cn': 'Venkata Ramana',
            'language': 'en_US',
            'ownertown': 'Hyderabad',
            'ownercty': 'IN',
            'exceptionurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'ownerzip': 'Postcode',
            'catalogurl': 'http://127.0.0.1:8000/',
            'currency': 'EUR',
            'amount': '579',
            'declineurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'homeurl': 'http://127.0.0.1:8000/',
            'cancelurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'accepturl': 'http://127.0.0.1:8000/offsite/ogone/success/',
            'owneraddress': 'Near Madapur PS',
            'com': 'Order #21: Venkata Ramana',
            'email': 'ramana@agiliq.com'
        }
        self.op.add_fields(self.data)

    def testFormFields(self):
        self.assertEquals(self.op.fields, {
            'orderID': 21,
            'ownerstate': '',
            'cn': 'Venkata Ramana',
            'language': 'en_US',
            'ownertown': 'Hyderabad',
            'ownercty': 'IN',
            'exceptionurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'ownerzip': 'Postcode',
            'catalogurl': 'http://127.0.0.1:8000/',
            'currency': 'EUR',
            'amount': '579',
            'declineurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'homeurl': 'http://127.0.0.1:8000/',
            'cancelurl': 'http://127.0.0.1:8000/offsite/ogone/failure/',
            'accepturl': 'http://127.0.0.1:8000/offsite/ogone/success/',
            'owneraddress': 'Near Madapur PS',
            'com': 'Order #21: Venkata Ramana',
            'email': 'ramana@agiliq.com'
        })
