from merchant import GatewayNotConfigured
from merchant.gateways.stripe_gateway import StripeGateway as Gateway
from billing.signals import transaction_was_successful, transaction_was_unsuccessful
from billing.utils.credit_card import InvalidCard, Visa, MasterCard, \
     AmericanExpress, Discover, CreditCard
import stripe
from django.conf import settings


class StripeGateway(Gateway):
    supported_cardtypes = [Visa, MasterCard, AmericanExpress, Discover]
    supported_countries = ['US']
    default_currency = "USD"
    homepage_url = "https://stripe.com/"
    display_name = "Stripe"

    def __init__(self):
        merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("stripe"):
            raise GatewayNotConfigured("The '%s' gateway is not correctly "
                                       "configured." % self.display_name)
        stripe_settings = merchant_settings["stripe"]
        stripe.api_key = stripe_settings['API_KEY']
        self.stripe = stripe

    def purchase(self, amount, credit_card, options=None):
        response = super(StripeGateway, self).purchase(amount,
                                                       credit_card,
                                                       options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="purchase",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="purchase",
                                            response=response["response"])
        return response

    def store(self, credit_card, options=None):
        response = super(StripeGateway, self).store(credit_card,
                                                    options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="store",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="store",
                                            response=response["response"])
        return response

    def recurring(self, credit_card, options=None):
        response = super(StripeGateway, self).recurring(credit_card,
                                                    options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="recurring",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="recurring",
                                            response=response["response"])
        return response

    def unstore(self, identification, options=None):
        response = super(StripeGateway, self).unstore(identification,
                                                      options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="unstore",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="unstore",
                                            response=response["response"])
        return response

    def credit(self, identification, money=None, options=None):
        response = super(StripeGateway, self).credit(identification,
                                                     money=money,
                                                     options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="credit",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="credit",
                                            response=response["response"])
        return response

    def authorize(self, money, credit_card, options=None):
        response = super(StripeGateway, self).authorize(money,
                                                        credit_card,
                                                        options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="authorize",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="authorize",
                                            response=response["response"])
        return response

    def capture(self, money, authorization, options=None):
        response = super(StripeGateway, self).capture(money,
                                                      authorization,
                                                      options=options)
        if response['status'] == 'FAILURE':
            transaction_was_unsuccessful.send(sender=self,
                                              type="capture",
                                              response=response["response"])
        else:
            transaction_was_successful.send(sender=self,
                                            type="capture",
                                            response=response["response"])
        return response
