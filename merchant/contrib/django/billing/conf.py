from django.conf import settings
settings = getattr(settings, "MERCHANT_SETTINGS", {})
