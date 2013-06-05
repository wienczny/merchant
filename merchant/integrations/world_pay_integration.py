from merchant import Integration


class WorldPayIntegration(Integration):
    """
    Fields required:
    instId: Installation ID provided by WorldPay
    cartId: Merchant specified unique id to identify user
    amount: Amount to be charged
    currency: ISO 3-character currency
    """
    display_name = "RBS World Pay"
    template = "billing/world_pay.html"

    def __init__(self, settings, options=None):
        if not options:
            options = {}
        super(WorldPayIntegration, self).__init__(options=options)
        if self.test_mode:
            self.fields.update({"testMode": 100})
