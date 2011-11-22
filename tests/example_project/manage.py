#!/usr/bin/env python
from os.path import pardir, abspath, dirname, join
import sys

from django.core.management import execute_manager

# pythonpath dirs
PYTHONPATH = [
    abspath(join( dirname(__file__), pardir)),
    abspath(join( dirname(__file__), pardir, pardir)),
]

# inject few paths to pythonpath
for p in PYTHONPATH:
    if p not in sys.path:
        sys.path.insert(0, p)

import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
