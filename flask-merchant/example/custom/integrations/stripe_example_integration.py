from flask.ext.merchant.integrations.stripe_integration import StripeIntegration
from flask import current_app, request, render

class StripeExampleIntegration(StripeIntegration):
    def __init__(self, *args, **kwargs):
        super(StripeExampleIntegration, self).__init__(*args, **kwargs)
        self.register_urls()

    def transaction(self):
        charge = self.stripe.Charge.create(
            amount=1000, # amount in cents, again
            currency="usd",
            card=request.forms.get("token"),
            description="payinguser@example.com"
            )
        # TODO: Redirect to a success page
        return render("billing/main.html")

    def register_urls(self):
        current_app.add_url_rule("/offline/stripe/transaction/",
                                 "stripe_transaction",
                                 self.transaction, methods=["GET", "POST"])
