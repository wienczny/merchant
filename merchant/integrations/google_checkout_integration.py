from merchant import Integration


class GoogleCheckoutIntegration(Integration):

    display_name = 'Google Checkout'
    template = "billing/google_checkout.html"

    def __init__(self, settings, options=None):
        if not options:
            options = {}
        super(GoogleCheckoutIntegration, self).__init__(options=options)
        self.merchant_id = settings['MERCHANT_ID']
        self.merchant_key = settings['MERCHANT_KEY']
        self._signature = None
