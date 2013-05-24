from wepay import WePay
from wepay.exceptions import WePayError

from merchant import Gateway, GatewayNotConfigured
from merchant.utils.credit_card import (InvalidCard,
                                        Visa, MasterCard, CreditCard)


class WePayGateway(Gateway):

    display_name = "WePay"
    homepage_url = "https://www.wepay.com/"
    default_currency = "USD"
    supported_countries = ["US"]
    supported_cardtypes = [Visa, MasterCard]

    def __init__(self, settings):
        production = not self.test_mode
        self.we_pay = WePay(production)
        self.account_id = settings.get("ACCOUNT_ID", "")
        self.access_token = settings["ACCESS_TOKEN"]
        self.client_id = settings["CLIENT_ID"]
        self.client_secret = settings["CLIENT_SECRET"]

    def purchase(self, money, credit_card, options=None):
        options = options or {}
        params = {}
        params.update({
            'account_id': self.account_id,
            'short_description': options.pop("description", ""),
            'amount': money,
        })
        if credit_card and not isinstance(credit_card, CreditCard):
            params["payment_method_id"] = credit_card
            params["payment_method_type"] = "credit_card"
        params.update(options)
        try:
            response = self.we_pay.call('/checkout/create', params, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def authorize(self, money, credit_card, options=None):
        options = options or {}
        resp = self.store(credit_card, options)
        if resp["status"] == "FAILURE":
            return resp
        try:
            resp = self.we_pay.call('/credit_card/authorize', {
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'credit_card_id': resp['response']['credit_card_id']
                    }, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        params = {
            "auto_capture": False
            }
        params.update(options)
        response = self.purchase(money, resp["credit_card_id"], params)
        if response["status"] == "FAILURE":
            return response
        return response

    def capture(self, money, authorization, options=None):
        options = options or {}
        params = {
            'checkout_id': authorization,
            }
        try:
            response = self.we_pay.call('/checkout/capture', params, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def void(self, identification, options=None):
        options = options or {}
        params = {
            'checkout_id': identification,
            'cancel_reason': options.pop("description", "")
            }
        try:
            response = self.we_pay.call('/checkout/cancel', params, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def credit(self, money, identification, options=None):
        options = options or {}
        params = {
            'checkout_id': identification,
            'refund_reason': options.pop("description", ""),
            }
        if money:
            params.update({'amount': money})
        try:
            response = self.we_pay.call('/checkout/refund', params, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def recurring(self, money, credit_card, options=None):
        options = options or {}
        params = {
            'account_id': self.account_id,
            "short_description": options.pop("description", ""),
            "amount": money,
        }
        params.update(options)
        try:
            response = self.we_pay.call("/preapproval/create", params, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}

    def store(self, credit_card, options=None):
        options = options or {}
        if not self.validate_card(credit_card):
            raise InvalidCard("Invalid Card")
        try:
            response = self.we_pay.call('/credit_card/create', {
                    'client_id': self.client_id,
                    'user_name': credit_card.name,
                    'email': options.pop("customer")["email"],
                    'cc_number': credit_card.number,
                    'cvv': credit_card.verification_value,
                    'expiration_month': credit_card.month,
                    'expiration_year': credit_card.year,
                    'address': options.pop("billing_address")
                    }, token=self.access_token)
        except WePayError, error:
            return {'status': 'FAILURE', 'response': error}
        return {'status': 'SUCCESS', 'response': response}
