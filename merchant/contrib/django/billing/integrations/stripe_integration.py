from django.conf import settings
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from merchant.integrations.stripe_integration import StripeIntegration as Integration
from merchant.contrib.django.billing.forms.stripe_forms import StripeForm
from merchant.contrib.django.billing.gateway import get_gateway


class StripeIntegration(Integration):

    def __init__(self, settings):
        super(StripeIntegration, self).__init__(settings)
        self.gateway = get_gateway("stripe")

    def form_class(self):
        return StripeForm

    def generate_form(self):
        initial_data = self.fields
        form = self.form_class()(initial=initial_data)
        return form

    def transaction(self, request):
        # Subclasses must override this
        raise NotImplementedError

    def get_urls(self):
        urlpatterns = patterns('',
           url('^merchant/stripe/$', self.transaction, name="merchant_stripe_transaction")
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    @property
    def url_name(self):
        return reverse_lazy("merchant_stripe_transaction")
