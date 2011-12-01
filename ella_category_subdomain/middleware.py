'''
Created on 11.11.2011

@author: whit
'''

from urlparse import urlparse, urlunparse
# JS: Zbytecne, nepouziva se
import logging

from django.conf import settings
from django.http import HttpResponseRedirect

# JS: tyhle importy s teckou jsou divne, nic nam nebrani v tom napsat to tam cele
from .models import CategorySubdomain
from .monkeypatch import do_monkeypatch, get_domain, get_url


class CategorySubdomainMiddleware:

    def __init__(self):
        self.static_prefixes = [settings.MEDIA_URL,]

    def process_request(self, request):
        # FIXME: Permanent redirect from old url.
        redirect = self._get_redirect_if_old_location(request)
        # JS: tahle konstrukce se podivna, pokud uz tam ta podminka je, tak at se na ni vola to _translate_path() a ne return a jeden return na konci vrati redirect
        if redirect is None:
            self._translate_path(request)
        return redirect

    def _get_category_subdomain_for_host(self, host):
        domain_parts = host.split('.')
        # tuhle metodu jsem upravil, aby pouzial ten result
        result = None

        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                cs = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                if cs.category.site.pk == settings.SITE_ID:
                    result = cs
            except CategorySubdomain.DoesNotExist:
                pass
        return result

    def _get_category_subdomain_for_path(self, path):
        tree_path = path.lstrip('/').split('/')[0]
        try:
            return CategorySubdomain.objects.get(category__tree_path=tree_path,
                                                 category__site__pk=settings.SITE_ID)
        except CategorySubdomain.DoesNotExist:
            # tohle nejde, nemuze tam byt v jedne vetvi return a v druhe nic..
            pass

    def _translate_path(self, request):
        '''Change request.path and request.path_info if "necessary".'''
        # FIXME: What is the best method of proper static prefixes handling?
        for prefix in self.static_prefixes:
            # FIXME: Should we take request.path or request.path_info?
            if request.path_info.startswith(prefix):
                return

        cs = self._get_category_subdomain_for_host(request.get_host())
        if cs is not None:
            # FIXME: Should we really change both request.path and
            # request.path_info? "None of them" is not an acceptable answer
            # here ;-)
            request.path = request.path_info =\
                    '/%s%s' % (cs.category.path, request.path_info)
        # JS: tahle vetev by mela explicine vracet None

    # JS: bylo by hezci, kdyby ten test by o uroven vys a tady ta metoda se jmenovala jen _get_redirect
    def _get_redirect_if_old_location(self, request):
        # TODO
        domain = get_domain(strip_www=False)
        # JS: to volani v ifu bych vyhodil pred a pak porovnal promenne
        if request.get_host() == domain:
            cs = self._get_category_subdomain_for_path(request.path)
        else:
            # JS: tahle vetev je zbytecna a
            cs = None
        if cs is not None:
            # JS: tohle je hrozne necitelny. urlparse ma vracet ParseResult, proc z toho delas list?
            # JS: ok, uz to vim :)
            parsed_url_list = list(urlparse(request.build_absolute_uri()))
            # JS: zase dve volani funkci takhle na jednom radku...
            netloc = cs.get_subdomain() + cs._development_server_port()
            # JS: proc je tam to +1? Kvuli nejakemu dalsimu lomitku?
            path = request.path[len(cs.category.tree_path)+1:]
            parsed_url_list[1:3] = netloc, path
            return HttpResponseRedirect(urlunparse(parsed_url_list))

