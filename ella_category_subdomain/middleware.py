import logging

from urlparse import urlparse, urlunparse

from django.conf import settings
from django.http import HttpResponseRedirect, Http404

from ella_category_subdomain.conf import ella_category_subdomain_settings
from ella_category_subdomain.models import CategorySubdomain
from ella_category_subdomain.util import get_domain_for_category


class CategorySubdomainMiddleware(object):
    """The middleware is requirement for the correct function of the
    application. It rewrites the request path to the original state for
     the normal django processing.
    """

    def __init__(self):
        super(CategorySubdomainMiddleware, self).__init__()
        self.static_prefixes = [settings.MEDIA_URL, ]
        self.static_prefixes.extend(ella_category_subdomain_settings.IGNORE_PATHS)
        self.log = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

    def process_request(self, request):
        host = request.get_host()
        self.log.debug("Path: %s", request.path)
        self.log.debug("Host: %s", host)
        path_subdomain = CategorySubdomain.objects.get_for_path(request.path)
        self.log.debug("Path subdomain: %s" % (path_subdomain))
        if ((path_subdomain is not None) and
            (not ella_category_subdomain_settings.OLD_STYLE_URL)):
            raise Http404

        self.category_subdomain = CategorySubdomain.objects.get_for_host(host)

        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (self.category_subdomain is not None):
            self.log.debug("process view: %s, %s, %s", view_func, view_args, view_kwargs)

            for prefix in self.static_prefixes:
                if request.path_info.startswith(prefix):
                    return

            view_kwargs['category'] = self.category_subdomain.category.tree_path
            self.log.debug("process view modified: %s, %s, %s", view_func, view_args, view_kwargs)

        return None


class CategorySubdomainRedirectMiddleware(object):
    """The middleware allows to use original URL for the categories which are
    configured for subdomains. It redirect the old style URL of the subdomain
    category to the correct subdomain.
    """

    def __init__(self):
        self.log = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))

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

        self.log.debug("Host: %s, domain: %s", host, domain)

        # try to find a subdomain for a first category in the path if they match
        if host == domain:
            # search for a category subdomain matching the first path of the domain
            category_subdomain = CategorySubdomain.objects.get_for_path(request.path)
            #
            if category_subdomain is not None:
                # get the absolute uri of the request
                request_absolute_uri = request.build_absolute_uri()
                # parse the uri
                parsed_url_list = list(urlparse(request_absolute_uri))
                # get domain name for the category subdomain
                new_domain = category_subdomain.get_subdomain()
                # cut off the first category part of the path
                new_path = request.path[len(category_subdomain.category.tree_path) + 1:]
                # replace domain and path in uri
                parsed_url_list[1:3] = new_domain, new_path
                # redirect to the new uri
                return HttpResponseRedirect(urlunparse(parsed_url_list))
