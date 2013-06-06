import braintree

from merchant import Integration


class BraintreePaymentsIntegration(Integration):

    display_name = "Braintree Transparent Redirect"
    template = "billing/braintree_payments.html"

    def __init__(self, settings, options=None):
        if not options:
            options = {}
        super(BraintreePaymentsIntegration, self).__init__(options=options)

        if self.test_mode:
            env = braintree.Environment.Sandbox
        else:
            env = braintree.Environment.Production
        braintree.Configuration.configure(
            env,
            settings['MERCHANT_ACCOUNT_ID'],
            settings['PUBLIC_KEY'],
            settings['PRIVATE_KEY']
        )

    @property
    def service_url(self):
        return braintree.TransparentRedirect.url()
