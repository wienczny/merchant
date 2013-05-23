import os

from importlib import import_module


settings_module = os.getenv("MERCHANT_SETTINGS", None)
settings = None
if settings_module:
    settings = getattr(import_module(settings_module), "MERCHANT_SETTINGS", {})
