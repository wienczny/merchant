from merchant.integrations.stripe_integration import StripeIntegration as Integration
from flask.ext.merchant import Integration, get_gateway, IntegrationNotConfigured
from flask.ext.merchant.forms.stripe_forms import StripeForm
from flask import current_app

class StripeIntegration(Integration):
    display_name = "Stripe"
    template = "billing/stripe.html"

    def __init__(self):
        super(StripeIntegration, self).__init__()
        merchant_settings = current_app.config.get("MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("stripe"):
            raise IntegrationNotConfigured("The '%s' integration is not correctly "
                                           "configured." % self.display_name)
        stripe_settings = merchant_settings["stripe"]
        self.gateway = get_gateway("stripe")
        self.publishable_key = stripe_settings['PUBLISHABLE_KEY']

    def form_class(self):
        return StripeForm

    def transaction(self):
        # Subclasses must override this
        return NotImplementedError

    def register_urls(self):
        current_app.add_url_rule("/offline/stripe/transaction/",
                                 "stripe_transaction",
                                 self.transaction, methods=["GET", "POST"])
