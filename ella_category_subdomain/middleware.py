'''
Created on 11.11.2011

@author: whit
'''
import logging

from urlparse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect

from ella_category_subdomain.models import CategorySubdomain
from ella_category_subdomain.monkeypatch import get_url
from ella_category_subdomain.util import get_domain_for_category


class CategorySubdomainMiddleware:

    def __init__(self):
        self.static_prefixes = [settings.MEDIA_URL,]

    def process_request(self, request):
        redirect = None
        if ((hasattr(settings, 'CATEGORY_SUBDOMAIN_REDIRECT_OLD')) and
            (settings.CATEGORY_SUBDOMAIN_REDIRECT_OLD)):
            redirect = self._get_redirect_if_old_url(request)
        if redirect is None:
            self._translate_path(request)
        return redirect

    def _get_category_subdomain_for_host(self, host):
        domain_parts = host.split('.')

        result = None

        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                category_subdomain = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                if category_subdomain.category.site.pk == settings.SITE_ID:
                    result = category_subdomain
            except CategorySubdomain.DoesNotExist:
                pass
        return result

    def _get_category_subdomain_for_path(self, path):
        tree_path = path.lstrip('/').split('/')[0]
        try:
            return CategorySubdomain.objects.get(category__tree_path=tree_path,
                                                 category__site__pk=settings.SITE_ID)
        except CategorySubdomain.DoesNotExist:
            return None

    def _translate_path(self, request):
        '''Change request.path and request.path_info if "necessary".'''
        # FIXME: What is the best method of proper static prefixes handling?
        for prefix in self.static_prefixes:
            # FIXME: Should we take request.path or request.path_info?
            if request.path_info.startswith(prefix):
                return

        category_subdomain = self._get_category_subdomain_for_host(request.get_host())
        if category_subdomain is not None:
            # FIXME: Should we really change both request.path and
            # request.path_info? "None of them" is not an acceptable answer
            # here ;-)
            request.path = request.path_info =\
                    '/%s%s' % (category_subdomain.category.path, request.path_info)
            logging.debug("Category subromain %s, new path: %s", category_subdomain, request.path)


    def _get_redirect_if_old_url(self, request):
        # get the site domain
        domain = get_domain_for_category(category=None, strip_www=False)
        # get the current request host
        host = request.get_host()

        # try to find a subdomain for a first category in the path if they match
        if host == domain:
            # search for a category subdomain matching the first path of the domain
            category_subdomain = self._get_category_subdomain_for_path(request.path)
            #
            if category_subdomain is not None:
                # get the absolute uri of the request
                request_absolute_uri = request.build_absolute_uri()
                # parse the uri
                parsed_url_list = list(urlparse(request_absolute_uri))
                # get domain name for the category subdomain
                new_domain = cs.get_subdomain()
                # cut off the first category part of the path
                new_path = request.path[len(category_subdomain.category.tree_path)+1:]
                # replace domain and path in uri
                parsed_url_list[1:3] = new_domain, new_path
                # redirect to the new uri
                return HttpResponseRedirect(urlunparse(parsed_url_list))

