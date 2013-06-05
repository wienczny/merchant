from merchant import Integration


class PaypalIntegration(Integration):

    display_name = "PayPal IPN"
    template = "billing/paypal.html"

    def __init__(self, settings):
        self.encrypted = False
        if settings.get("ENCRYPTED"):
            self.encrypted = True
        # Required Fields. Just a template for the user
        self.fields = {
            "business": settings['RECEIVER_EMAIL'],
            "item_name": "",
            "invoice": "",
            "notify_url": "",
            "return_url": "",
            "cancel_return": "",
            "amount": 0,
        }
