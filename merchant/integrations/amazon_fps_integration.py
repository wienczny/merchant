from merchant import Integration

from boto.fps.connection import FPSConnection


class AmazonFpsIntegration(Integration):
    """
    Fields required:
    transactionAmount: Amount to be charged/authorized
    paymentReason: Description of the transaction
    paymentPage: Page to direct the user on completion/failure of transaction
    """

    display_name = "Amazon Flexible Payment Service"
    template = "billing/amazon_fps.html"

    def __init__(self, settings, options=None):
        if not options:
            options = {}
        self.aws_access_key = options.get("aws_access_key", None) or settings['AWS_ACCESS_KEY']
        self.aws_secret_access_key = options.get("aws_secret_access_key", None) or settings['AWS_SECRET_ACCESS_KEY']
        super(AmazonFpsIntegration, self).__init__(options=options)
        options.setdefault('host', self.service_url)
        self.fps_connection = FPSConnection(self.aws_access_key, self.aws_secret_access_key, **options)
