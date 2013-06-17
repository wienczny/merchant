from flask.ext.merchant import Integration, get_gateway, IntegrationNotConfigured
from flask.ext.merchant.forms.stripe_forms import StripeForm
from flask import current_app

from merchant.integrations.stripe_integration import StripeIntegration as Integration


class StripeIntegration(Integration):

    display_name = "Stripe"
    template = "billing/stripe.html"

    def __init__(self, settings):
        super(StripeIntegration, self).__init__(settings)
        self.gateway = get_gateway("stripe")

    def form_class(self):
        return StripeForm

    def transaction(self):
        # Subclasses must override this
        return NotImplementedError

    def register_urls(self):
        current_app.add_url_rule("/offline/stripe/transaction/",
                                 "stripe_transaction",
                                 self.transaction, methods=["GET", "POST"])
