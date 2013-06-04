from merchant.integrations.stripe_integration import StripeIntegration as Integration
from flask.ext.merchant import Integration, get_gateway, IntegrationNotConfigured
from flask.ext.merchant.forms.stripe_forms import StripeForm
from flask import current_app

class StripeIntegration(Integration):
    display_name = "Stripe"
    template = "billing/stripe.html"

    def form_class(self):
        return StripeForm

    def transaction(self):
        # Subclasses must override this
        return NotImplementedError

    def register_urls(self):
        current_app.add_url_rule("/offline/stripe/transaction/",
                                 "stripe_transaction",
                                 self.transaction, methods=["GET", "POST"])
