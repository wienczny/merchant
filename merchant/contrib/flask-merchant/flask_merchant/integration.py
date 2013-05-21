from importlib import import_module
from flask import current_app
from merchant.integration import Integration, IntegrationNotConfigured, IntegrationModuleNotFound

integration_cache = {}

def get_integration(integration, *args, **kwargs):
    """Return a integration instance specified by `integration` name"""

    klass = integration_cache.get(integration, None)

    if not klass:
        integration_filename = "%s_integration" % integration
        integration_module = None
        lookup_path = ['flask.ext.merchant']
        lookup_path.extend(current_app.config.get('MERCHANT_LOOKUP_PATH', []))
        for pkg in lookup_path:
            try:
                integration_module = import_module(".integrations.%s" % integration_filename, package=pkg)
            except ImportError:
                pass
        if not integration_module:
            raise IntegrationModuleNotFound("Missing integration: %s" % (integration))
        integration_class_name = "".join(integration_filename.title().split("_"))
        try:
            klass = getattr(integration_module, integration_class_name)
        except AttributeError:
            raise IntegrationNotConfigured("Missing %s class in the integration module." % integration_class_name)
        integration_cache[integration] = klass
    return klass(*args, **kwargs)
