'''
Created on 11.11.2011

@author: whit
'''
from django.conf import settings
from ella_seocats.models import SeoCat

class SeoCatsMiddleware:
    """  """

    def process_request(self, request):

        sc = self._get_subdomain_category(request.get_host())
        if sc is not None:
            ""
            # DO THINGS


    def process_view(self):
        pass


    def process_response(self, request, response):
        pass


    def _get_subdomain_category(self, host):
        domain_parts = host.split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                sc = SeoCat.objects.get(subdomain=subdomain)
                if sc.site.pk == settings.SITE_ID:
                    return sc.category
            except SeoCat.DoesNotExist:
                return None

        return None
