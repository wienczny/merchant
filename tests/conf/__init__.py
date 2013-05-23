import os
from importlib import import_module

settings = import_module("tests.conf.%s" % os.getenv("MERCHANT_TEST_SETTINGS", "local"))
