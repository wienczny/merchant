from merchant import Integration


class StripeIntegration(Integration):

    display_name = "Stripe"
    template = "billing/stripe.html"

    def __init__(self, settings):
        self.publishable_key = settings['PUBLISHABLE_KEY']
