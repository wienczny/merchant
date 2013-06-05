from merchant import Integration


class AuthorizeNetDpmIntegration(Integration):

    display_name = "Authorize.Net Direct Post Method"
    template = "billing/authorize_net_dpm.html"

    def __init__(self, settings):
        self.settings = settings
