from billing.integrations.amazon_fps_integration import AmazonFpsIntegration as Integration
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class FpsIntegration(Integration):
    def transaction(self, request):
        """Ideally at this method, you will check the 
        caller reference against a user id or uniquely
        identifiable attribute (if you are already not 
        using it as the caller reference) and the type 
        of transaction (either pay, reserve etc). For
        the sake of the example, we assume all the users
        get charged $100"""
        request_url = request.build_absolute_uri()
        parsed_url = urlparse(request_url)
        query = parsed_url.query
        dd = dict([x.split("=") for x in query.split("&")])
        resp = self.purchase(100, dd)
        return HttpResponseRedirect("%s?status=%s" % (reverse("app_offsite_amazon_fps"),
                                                      resp["status"]))
