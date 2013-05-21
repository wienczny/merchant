from merchant import Integration, get_gateway, IntegrationNotConfigured


class StripeIntegration(Integration):
    display_name = "Stripe"
    template = "billing/stripe.html"

    def generate_form(self):
        initial_data = self.fields
        form = self.form_class()(initial=initial_data)
        return form

    def transaction(self, request):
        # Subclasses must override this
        raise NotImplementedError
