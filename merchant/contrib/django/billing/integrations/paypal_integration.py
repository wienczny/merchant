from django.conf.urls import patterns, include

from paypal.standard.conf import POSTBACK_ENDPOINT, SANDBOX_POSTBACK_ENDPOINT
from paypal.standard.ipn.signals import (payment_was_flagged,
                                         payment_was_successful)

from merchant.integrations.paypal_integration import PaypalIntegration as Integration
from merchant.contrib.django.billing.forms.paypal_forms import (MerchantPayPalPaymentsForm,
                                        MerchantPayPalEncryptedPaymentsForm)
from merchant.contrib.django.billing.signals import (transaction_was_successful,
                             transaction_was_unsuccessful)


class PaypalIntegration(Integration):

    @property
    def service_url(self):
        if self.test_mode:
            return SANDBOX_POSTBACK_ENDPOINT
        return POSTBACK_ENDPOINT

    def form_class(self):
        if self.encrypted:
            return MerchantPayPalEncryptedPaymentsForm
        return MerchantPayPalPaymentsForm

    def generate_form(self):
        return self.form_class()(initial=self.fields)

    def get_urls(self):
        urlpatterns = patterns('', (r'^merchant/paypal/ipn', include('paypal.standard.ipn.urls')))
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()


def unsuccessful_txn_handler(sender, **kwargs):
    transaction_was_unsuccessful.send(sender=sender.__class__,
                                      type="purchase",
                                      response=sender)


def successful_txn_handler(sender, **kwargs):
    transaction_was_successful.send(sender=sender.__class__,
                                    type="purchase",
                                    response=sender)

payment_was_flagged.connect(unsuccessful_txn_handler)
payment_was_successful.connect(successful_txn_handler)
