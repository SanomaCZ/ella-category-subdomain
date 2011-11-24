'''
Created on 11.11.2011

@author: whit
'''

from django.conf import settings

from .models import CategorySubdomain
from .monkeypatch import do_monkeypatch

class CategorySubdomainMiddleware:

    def __init__(self):
        do_monkeypatch()

    def process_request(self, request):
        if request.path_info.startswith(settings.MEDIA_URL):
            return None
        sc = self._get_subdomain_category(request.get_host())
        if sc is not None:
            request.path_info = '/%s%s' % (sc.slug, request.path_info)
            request.path = '/%s%s' % (sc.slug, request.path)
        return None

    def process_response(self, request, response):
        return response


    def _get_subdomain_category(self, host):
        domain_parts = host.split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                cs = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                if cs.category.site.pk == settings.SITE_ID:
                    return cs.category
            except CategorySubdomain.DoesNotExist:
                return None

        return None
