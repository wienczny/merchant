from merchant.gateways.stripe_gateway import StripeGateway as Gateway
import stripe
from flask import current_app
from flask.ext.merchant import GatewayNotConfigured

class StripeGateway(Gateway):
    def __init__(self):
        merchant_settings = current_app.config.get("MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("stripe"):
            raise GatewayNotConfigured("The '%s' gateway is not correctly "
                                       "configured." % self.display_name)
        stripe_settings = merchant_settings["stripe"]
        stripe.api_key = stripe_settings['API_KEY']
        self.stripe = stripe
