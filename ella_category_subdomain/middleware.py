'''
Created on 11.11.2011

@author: whit
'''

from urlparse import urlparse
import logging

from django.conf import settings

from .models import CategorySubdomain
from .monkeypatch import do_monkeypatch


class CategorySubdomainMiddleware:

    def __init__(self):
        self.static_prefixes = [settings.MEDIA_URL]
        do_monkeypatch()

    def process_request(self, request):
        # FIXME: Permanent redirect from old url.
        request.path = request.path_info =\
                self._translate_path(request.get_host(), request.path)
        return None

    def _get_category_subdomain(self, host):
        logging.warning("Getting CategorySubdomain for host %r" % host)
        domain_parts = host.split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                cs = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                if cs.category.site.pk == settings.SITE_ID:
                    return cs
            except CategorySubdomain.DoesNotExist:
                return None

        return None

    def _translate_path(self, host, path):
        for prefix in self.static_prefixes:
            if path.startswith(prefix):
                return path
        cs = self._get_category_subdomain(host)
        if cs is not None:
            new_path = '/%s%s' % (cs.category.path, path)
        else:
            new_path = path
        return new_path
