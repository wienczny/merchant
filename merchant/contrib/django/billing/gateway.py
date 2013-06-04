from django.utils.importlib import import_module

from merchant.contrib.django.billing.conf import settings
from merchant.gateway import (
    GatewayModuleNotFound,
    GatewayNotConfigured,
    InvalidData,
    Gateway
)
from merchant.utils.credit_card import CardNotSupported

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
        gateway_module = import_module("merchant.contrib.django.billing.gateways.%s" % gateway_filename)
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
    kwargs.setdefault("settings", settings[gateway])
    return clazz(*args, **kwargs)
