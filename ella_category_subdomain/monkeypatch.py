from urlparse import urlparse, urlunparse

import logging

from django.conf import settings
from django.contrib.sites.models import Site
import django.conf.urls.defaults
import django.core.urlresolvers as urlresolvers

from .models import CategorySubdomain

from ella_category_subdomain.urlresolvers import CategorySubdomainURLPattern
from ella_category_subdomain.urlresolvers import CategorySubdomainURLResolver
from ella.core.models.main import Category
from ella.core.models.publishable import Publishable


def get_domain(strip_www=False):
    domain = Site.objects.get(pk=settings.SITE_ID).domain
    return domain[4:] if domain.startswith('www.') and strip_www else domain


def update_parsed_url_list(parsed_url_list):
    # If parsed_url has scheme attribute then preserve it,
    # else default to http.
    parsed_url_list[0] = parsed_url_list[0] or 'http'

    # Append defined server port if debugging.
    if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
        parsed_url_list[1] += ':%s' % settings.DEVELOPMENT_SERVER_PORT


def get_url_with_subdomain(parsed_url, category_subdomain):
    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    subdomain_slug = category_subdomain.subdomain_slug
    category_path = category_subdomain.category.tree_path

    # Strip category tree path (plus slash at the beginning).
    new_path = parsed_url.path[len(category_path)+1:]

    # Get subdomain for given category.
    domain = '%s.%s' % (subdomain_slug, get_domain(strip_www=True))

    # Change parsed_url_list.
    parsed_url_list[1:3] = domain, new_path
    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url_without_subdomain(parsed_url):
    parts = parsed_url.netloc.split('.')

    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    parsed_url_list[1] = get_domain(strip_www=False)
    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url(url):
    # Parse url.
    parsed_url = urlparse(url)

    # If a path of the original Django reverse starts with tree_path
    # of a category with subdomain, add the appropriate CategorySubdomain
    # to category_subdomain_list.
    # FIXME: It desperately requires another approach.
    category_subdomain_list = [x for x in CategorySubdomain.objects.all()
          if parsed_url.path.startswith('/%s/' % x.category.tree_path)]

    # If category_subdomain_list is empty, return url without sudomain (of
    # the lowest possible level).
    if not category_subdomain_list:
        return get_url_without_subdomain(parsed_url)

    # Now, category_subdomain_list should contain just one
    # CategorySubdomain instance (because of model validation).
    # Otherwise at least on of them would be double or more nested
    # category.
    assert len(category_subdomain_list) == 1, 'This should be always 1!'

    # Finally, return url with correct subdomain and path.
    return get_url_with_subdomain(parsed_url, category_subdomain_list[0])


def patch_reverse(reverse):
    def wrapper(*args, **kwargs):
        # Get url from a result of original Django reverse.
        return get_url(reverse(*args, **kwargs))
    wrapper._original_reverse = reverse
    return wrapper


def do_monkeypatch():
    # Replace django.core.urlresolvers.reverse and do it only once.
    if not hasattr(urlresolvers.reverse, '_original_reverse'):
        urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
    # Replace ella.core.models.main.Category.get_absolute_url
    if not hasattr(Category.get_absolute_url, '_original_reverse'):
        Category.get_absolute_url = patch_reverse(Category.get_absolute_url)
    # Replace ella.core.models.publishable.Publishable.get_absolute_url
    if not hasattr(Publishable.get_absolute_url, '_original_reverse'):
        Publishable.get_absolute_url = patch_reverse(Publishable.get_absolute_url)
