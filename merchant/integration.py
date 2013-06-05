import sys

from importlib import import_module

from .conf import settings

integration_cache = {}


class IntegrationModuleNotFound(Exception):
    pass


class IntegrationNotConfigured(Exception):
    pass


class Integration(object):
    """Base Integration class that needs to be subclassed by
    implementations"""
    # The mode of the gateway. Looks into the settings else
    # defaults to True
    test_mode = True

    # Name of the integration.
    display_name = ''

    # Template rendered by the templatetag 'billing'
    template = ''

    fields = {}

    urls = ()

    def __init__(self, options=None):
        if not options:
            options = {}
        # The form fields that will be rendered in the template
        self.fields = {}
        self.fields.update(options)

    def add_field(self, key, value):
        self.fields[key] = value

    def add_fields(self, params):
        for (key, val) in params.iteritems():
            self.add_field(key, val)

    @property
    def service_url(self):
        # Modified by subclasses
        raise NotImplementedError


def get_integration(integration, *args, **kwargs):
    """Return a integration instance specified by `integration` name"""

    klass = integration_cache.get(integration, None)

    if not klass:
        integration_filename = "%s_integration" % integration
        integration_module = import_module("merchant.integrations.%s" % integration_filename)
        if not integration_module:
            raise IntegrationModuleNotFound("Missing integration: %s" % (integration))
        integration_class_name = "".join(integration_filename.title().split("_"))
        try:
            klass = getattr(integration_module, integration_class_name)
        except AttributeError:
            raise IntegrationNotConfigured("Missing %s class in the integration module." % integration_class_name)
        integration_cache[integration] = klass
    kwargs.setdefault("settings", settings[integration])
    return klass(*args, **kwargs)
