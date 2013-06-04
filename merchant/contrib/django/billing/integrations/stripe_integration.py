from django.conf import settings
from django.conf.urls import patterns, url

from merchant.integrations.stripe_integration import StripeIntegration as Integration
from merchant.contrib.django.billing.forms.stripe_forms import StripeForm


class StripeIntegration(Integration):
    display_name = "Stripe"
    template = "billing/stripe.html"

    def __init__(self, settings):
        self.publishable_key = settings['PUBLISHABLE_KEY']

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
           url('^stripe_token/$', self.transaction, name="stripe_transaction")
        )
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()
