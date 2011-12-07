'''
Created on 11.11.2011

@author: whit
'''
import logging

from urlparse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect, Http404

from ella_category_subdomain.conf import ella_category_subdomain_settings
from ella_category_subdomain.models import CategorySubdomain
from ella_category_subdomain.util import get_domain_for_category


class CategorySubdomainMiddleware(object):
    """The middleware is requirement for the correct function of the application.
    It rewrites the request path to the original state for the normal django processing.
    """

    def __init__(self):
        super(CategorySubdomainMiddleware, self).__init__()
        self.static_prefixes = [settings.MEDIA_URL,]

    def process_request(self, request):
        host = request.get_host()
        category_subdomain = self._get_category_subdomain_for_host(host)

        path = request.path
        path_items = [path_item for path_item in path.split('/') if len(path_item)>0]

        if (len(path_items) > 0):
            path_category_subdomain = CategorySubdomain.objects.filter(category__slug = path_items[0])
            if ((len(path_category_subdomain) > 0) and
                (not ella_category_subdomain_settings.OLD_STYLE_URL)):
                raise Http404

        self.domain_category = category_subdomain.category.slug if category_subdomain is not None else None

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (self.domain_category is not None):
            logging.warning("process view: %s, %s, %s", view_func, view_args, view_kwargs)
            category = view_kwargs.get('category')
            if (category is None):
                view_kwargs['category'] = '%s' % (self.domain_category)
            else:
                view_kwargs['category'] = '%s/%s' % (self.domain_category, category,)
            logging.warning("process view modified: %s, %s, %s", view_func, view_args, view_kwargs)
        return None

    def _get_category_subdomain_for_host(self, host):
        """Searches for a CategorySubdomain instance matching the first part of the domain.
        """
        # split the domain into parts
        domain_parts = host.split('.')
        # prepare the default response
        result = None
        # process the domain if it is of the 3rd level or more
        if (len(domain_parts) > 2):
            # get the first part of the domain
            subdomain = domain_parts[0].lower()

            try:
                # get the category subdomain
                category_subdomain = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                # return the CategorySubdomain instance if the category matches the current site
                if category_subdomain.category.site.pk == settings.SITE_ID:
                    result = category_subdomain

            except CategorySubdomain.DoesNotExist:
                # category subdomain does not exists
                pass

        return result


class CategorySubdomainRedirectMiddleware(object):
    """The middleware allows to use original URL for the categories which are
    configured for subdomains. It redirect the old style URL of the subdomain
    category to the correct subdomain.
    """

    def process_request(self, request):
        redirect = self._get_redirect_if_old_url(request)
        return redirect

    def _get_redirect_if_old_url(self, request):
        """Returns a HttpResponseRedirect instance when the category configured for a
        subdomain is detected in the path (i.e. as if there was no subdomain) and redirects
        the request to correct subdomain URL.
        """
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
                new_domain = category_subdomain.get_subdomain()
                # cut off the first category part of the path
                new_path = request.path[len(category_subdomain.category.tree_path)+1:]
                # replace domain and path in uri
                parsed_url_list[1:3] = new_domain, new_path
                # redirect to the new uri
                return HttpResponseRedirect(urlunparse(parsed_url_list))

    def _get_category_subdomain_for_path(self, path):
        """Returns a CategorySubdomain instance for a first part of the path if present in
        the database.
        """
        tree_path = path.lstrip('/').split('/')[0]
        try:
            return CategorySubdomain.objects.get(category__tree_path=tree_path,
                                                 category__site__pk=settings.SITE_ID)
        except CategorySubdomain.DoesNotExist:
            return None
