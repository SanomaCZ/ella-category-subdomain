from urlparse import urlparse, urlunparse

import logging

from django.conf import settings
import django.conf.urls.defaults
import django.core.urlresolvers as urlresolvers
# from django.core.urlresolvers import RegexURLResolver
# from django.core.urlresolvers import RegexURLPattern

from .models import CategorySubdomain
# from ella.core.models import Category, Placement
# from ella.core.cache import get_cached_object

from ella_category_subdomain.urlresolvers import CategorySubdomainURLPattern
from ella_category_subdomain.urlresolvers import CategorySubdomainURLResolver
#from ella_category_subdomain.urlresolvers import CategorySubdomainLocaleURLResolver


def get_url_with_subdomain(parsed_url, category_subdomain):
    parsed_url_list = list(parsed_url)
    subdomain_slug = category_subdomain.subdomain_slug
    category_path = category_subdomain.category.tree_path
    new_scheme = parsed_url.scheme or 'http'
    new_path = parsed_url.path[len(category_path)+1:]
    new_netloc = category_subdomain.category.site.domain
    if new_netloc.startswith('www.'):
        new_netloc = new_netloc.replace('www.', subdomain_slug)
    else:
        new_netloc = '%s.%s' % (subdomain_slug, new_netloc)
    if settings.DEBUG and settings.DEVELOPMENT_SERVER_PORT:
        new_netloc += ':%s' % settings.DEVELOPMENT_SERVER_PORT
    parsed_url_list[:3] = new_scheme, new_netloc, new_path
    logging.warning("parsed_url_list = %r" % parsed_url_list)
    return urlunparse(parsed_url_list)


def patch_reverse(reverse):
    def wrapper(*args, **kwargs):
        url = reverse(*args, **kwargs)
        logging.warning("Unpatched reverse: %r\n" % url)

        parsed_url = urlparse(reverse(*args, **kwargs))
        logging.warning("Parsed unpatched reverse: %r\n" % (parsed_url,))

        category_subdomain_list = [x for x in CategorySubdomain.objects.all()
              if parsed_url.path.startswith('/%s/' % x.category.tree_path)]

        if not category_subdomain_list:
            return url

        assert len(category_subdomain_list) == 1, 'This should be always 1!'
        return get_url_with_subdomain(parsed_url, category_subdomain_list[0])
    return wrapper


original_url = django.conf.urls.defaults.url

def url(regex, view, kwargs=None, name=None, prefix=''):
    regex_url = original_url(regex, view, kwargs, name, prefix)
    if isinstance(regex_url, django.core.urlresolvers.RegexURLPattern):
        regex_url = CategorySubdomainURLPattern(regex, regex_url)
    if isinstance(regex_url, django.core.urlresolvers.RegexURLResolver):
        regex_url = CategorySubdomainURLResolver(regex, regex_url)
    return regex_url


def do_monkeypatch():
    urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
