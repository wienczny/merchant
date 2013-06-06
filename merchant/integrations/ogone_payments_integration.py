# -*- coding: utf-8 *-*
from merchant import Integration
from merchant.utils.bunch import Bunch


class OgonePaymentsIntegration(Integration):

    display_name = "Ogone Payments Integration"
    template = "billing/ogone_payments.html"

    def __init__(self, settings, options=None):
        if not options:
            options = {}
        self.settings = Bunch(**settings)

    def add_fields(self, params):
        for (key, val) in params.iteritems():
            if isinstance(val, dict):
                new_params = {}
                for k in val:
                    new_params["%s__%s" % (key, k)] = val[k]
                self.add_fields(new_params)
            else:
                self.add_field(key, val)
