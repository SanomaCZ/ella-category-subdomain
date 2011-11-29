from urlparse import urlparse, urlunparse

import logging

from django.conf import settings
from django.contrib.sites.models import Site
import django.conf.urls.defaults
import django.core.urlresolvers as urlresolvers

from .models import CategorySubdomain

from ella_category_subdomain.urlresolvers import CategorySubdomainURLPattern
from ella_category_subdomain.urlresolvers import CategorySubdomainURLResolver


def get_url_with_subdomain(parsed_url, category_subdomain):
    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)
    subdomain_slug = category_subdomain.subdomain_slug
    category_path = category_subdomain.category.tree_path
    # If parsed_url has scheme attribute then preserve it,
    # else default to http.
    new_scheme = parsed_url.scheme or 'http'
    # Strip category tree path (plus slash at the beginning).
    new_path = parsed_url.path[len(category_path)+1:]
    # Get lowest level domain for given category.
    new_netloc = category_subdomain.category.site.domain

    # If domain starts with 'www.' then replace it with subdomain slug,
    if new_netloc.startswith('www.'):
        new_netloc = new_netloc.replace('www.', subdomain_slug)
    else: # otherwise just prepend subdomain.
        new_netloc = '%s.%s' % (subdomain_slug, new_netloc)

    # Append defined server port if debugging.
    if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
        new_netloc += ':%s' % settings.DEVELOPMENT_SERVER_PORT

    # Change parsed_url_list.
    parsed_url_list[:3] = new_scheme, new_netloc, new_path
    logging.warning("parsed_url_list = %r" % parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url_without_subdomain(parsed_url):
    parts = parsed_url.netloc.split('.')
    logging.warning("get_url_without_subdomain.parts = %r" % parts)

    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    # Get all_sites domains.
    # FIXME: It desperately requires another approach.
    all_sites = [x.domain for x in Site.objects.all()]

    for i in range(2, len(parts)):
        # Construct domains up from the second level
        domain = '.'.join(parts[-i:])
        # and if one of them is in all_domains,
        if domain in all_domains:
            # pick this domain.
            parsed_url_list[1] = domain
            break
        # FIXME: What if domain of higher level is registered Site?

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def patch_reverse(reverse):
    def wrapper(*args, **kwargs):
        # Get a result of original Django reverse.
        # FIXME: We can get MatchResult, no basestring.
        # Parse url.
        parsed_url = urlparse(reverse(*args, **kwargs))
        logging.warning("Parsed unpatched reverse: %r\n" % (parsed_url,))

        # If a path of the original Django reverse starts with tree_path
        # of a category with subdomain, add the appropriate CategorySubdomain
        # to category_subdomain_list.
        category_subdomain_list = [x for x in CategorySubdomain.objects.all()
              if parsed_url.path.startswith('/%s/' % x.category.tree_path)]
        logging.warning("category_subdomain_list = %r\n" % (parsed_url,))

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

    wrapper.original_reverse = reverse
    return wrapper


def do_monkeypatch():
    # Replace django.core.urlresolvers.reverse.
    urlresolvers.reverse = patch_reverse(urlresolvers.reverse)

def undo_monkeypatch():
    if hasattr(urlresovers.reverse, 'original_reverse'):
        pass
