import os
from formencode.variabledecode import variable_decode


def get_merchant_settings():
    env_dict = dict(filter(lambda x: x[0].startswith('MERCHANT'), os.environ.items()))
    return variable_decode(env_dict, dict_char='__')['MERCHANT']

# MERCHANT SETTINGS
MERCHANT_TEST_MODE = True
MERCHANT_SETTINGS = get_merchant_settings()
