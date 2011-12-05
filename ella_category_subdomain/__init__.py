__version__ = (0, 1)
__versionstr__ = '.'.join(map(str, __version__))

#from ella_category_subdomain.monkeypatch import patchmodel
import importlib
import inspect
import logging
from django.conf import settings

from ella_category_subdomain.monkeypatch import patch_reverse, patch_resolve
import django.core.urlresolvers as urlresolvers

patched = {}

for app in settings.INSTALLED_APPS:
    if app.startswith('ella'):

        logging.warning("importing models for app: %s" % (app,))
        if (app == 'ella_category_subdomain'):
            continue
        module = importlib.import_module('%s.models' % (app,))
        module_members = inspect.getmembers(module)
        for name, member in module_members:
            if ((inspect.isclass(member)) and
                (patched.get(name, None) is None)):
                patched[name] = 1
                if hasattr(member, 'get_absolute_url'):

                    logging.warning(name)
                    member.get_absolute_url = patch_reverse(member.get_absolute_url)

urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
urlresolvers.resolve = patch_resolve(urlresolvers.resolve)
