#!/usr/bin/env python

"""
Add merchant settings as encryped env vars to .travis.yml
"""

import os

from merchant.conf import settings

from formencode.variabledecode import variable_encode

env_dict = variable_encode(settings, prepend='MERCHANT', dict_char='__')
for k, v in env_dict.iteritems():
    print 'adding %s' % (k)
    os.system('travis encrypt %s="%s" --add env.global' % (k, v))
