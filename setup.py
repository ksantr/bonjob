#!/usr/bin/env python

try:
    from scripts.post_install import AppSetup
except ImportError as e:
    print e
else:
    AppSetup()
