from importlib import import_module

from flask import current_app

from merchant.conf import settings
from merchant.integration import Integration, IntegrationNotConfigured, IntegrationModuleNotFound

integration_cache = {}


def get_integration(integration, module_path="merchant.contrib.flask_merchant.integrations", *args, **kwargs):
    """Return a integration instance specified by `integration` name"""

    klass = integration_cache.get(integration, None)

    if not klass:
        integration_filename = "%s_integration" % integration
        integration_module = import_module("%s.%s" % (module_path, integration_filename))
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
