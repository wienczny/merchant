from merchant import Integration


class EwayAuIntegration(Integration):

    display_name = "eWAY"
    service_url = "https://au.ewaygateway.com/mh/payment"
    template = "billing/eway.html"

    def __init__(self, settings, access_code=None):
        super(EwayAuIntegration, self).__init__()
        self.customer_id = settings["CUSTOMER_ID"]
        self.username = settings["USERNAME"]
        self.password = settings["PASSWORD"]
        # Don't use X-Forwarded-For. It doesn't really matter if REMOTE_ADDR
        # isn't their *real* IP, we're only interested in what IP they're going
        # to use for their POST request to eWAY. If they're using a proxy to
        # connect to us, it's fair to assume they'll use the same proxy to
        # connect to eWAY.
        self.access_code = access_code
