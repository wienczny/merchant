from importlib import import_module
from merchant.utils.credit_card import CardNotSupported
from flask import current_app
from merchant.gateway import Gateway, GatewayNotConfigured, GatewayModuleNotFound

gateway_cache = {}

def get_gateway(gateway, *args, **kwargs):
    """
    Return a gateway instance specified by `gateway` name.
    This caches gateway classes in a module-level dictionnary to avoid hitting
    the filesystem every time we require a gateway.

    Should the list of available gateways change at runtime, one should then
    invalidate the cache, the simplest of ways would be to:

    >>> gateway_cache = {}
    """
    # Is the class in the cache?
    clazz = gateway_cache.get(gateway, None)
    if not clazz:
        # Let's actually load it (it's not in the cache)
        gateway_filename = "%s_gateway" % gateway
        gateway_module = None
        lookup_path = ['flask.ext.merchant']
        lookup_path.extend(current_app.config.get('MERCHANT_LOOKUP_PATH', []))
        for pkg in lookup_path:
            try:
                gateway_module = import_module(".gateways.%s" % gateway_filename, package=pkg)
            except ImportError:
                pass
        if not gateway_module:
            raise GatewayModuleNotFound("Missing gateway: %s" % (gateway))
        gateway_class_name = "".join(gateway_filename.title().split("_"))
        try:
            clazz = getattr(gateway_module, gateway_class_name)
        except AttributeError:
            raise GatewayNotConfigured("Missing %s class in the gateway module." % gateway_class_name)
        gateway_cache[gateway] = clazz
    # We either hit the cache or load our class object, let's return an instance
    # of it.
    return clazz(*args, **kwargs)
