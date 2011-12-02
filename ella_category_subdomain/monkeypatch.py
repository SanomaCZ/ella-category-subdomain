from urlparse import urlparse, urlunparse

# JS: nepouzity import
import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models import get_models
#from django.db.models.base import ModelBase
#from django.db.models.loading import cache
import django.conf.urls.defaults
import django.core.urlresolvers as urlresolvers
from django.utils.functional import update_wrapper

# JS: import s teckou. Importy z projektu by mely byt az posledni
from .models import CategorySubdomain

from ella.core.models.main import Category
from ella.core.models.publishable import Publishable





# FIXME: Maybe should be defined somewhere else.
def get_domain(strip_www=False, with_development_server_port=True):
    """Return site domain with development server port (if DEBUG)."""
    domain = Site.objects.get(pk=settings.SITE_ID).domain
    if with_development_server_port:
        domain += CategorySubdomain._development_server_port()
    # JS: viz models.py
    return domain[4:] if domain.startswith('www.') and strip_www else domain


def update_parsed_url_list(parsed_url_list):
    # JS: tenhle nazev metody vubec nerika, co to dela
    # JS: mozna je i malicko zbytecna
    # If parsed_url has scheme attribute then preserve it,
    # else default to http.
    parsed_url_list[0] = parsed_url_list[0] or 'http'

    # # Append defined server port if debugging.
    # if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
    #     parsed_url_list[1] += ':%s' % settings.DEVELOPMENT_SERVER_PORT


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

    # get non-empty URL path items
    path_items = [item for item in parsed_url.path.split('/') if (len(item) > 0)]
    # if the path is not a root one check if the first item of path does not match category
    # subdomain and change the URL accordingly
    if (len(path_items) > 0):
        # get the first path item
        first_path_item = path_items[0]
        # search for the particular subdomain category
        category_subdomain_list = CategorySubdomain.objects.filter(category__slug = first_path_item)
        # change the URL if found
        if (len(category_subdomain_list) == 1):
             return get_url_with_subdomain(parsed_url, category_subdomain_list[0])

    # get the URL domain parts
    domain_items = parsed_url.netloc.split('.')
    # get the first domain part
    first_domain_item = domain_items[0]
    # search for the particular subdomain category
    category_subdomain_list = CategorySubdomain.objects.filter(subdomain_slug = first_domain_item)

    # the URL already modified if exists
    if (len(category_subdomain_list) > 0):
        return url
    # fill in the default subdomain otherwise
    else:
        return get_url_without_subdomain(parsed_url)



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

    # Replace get all the get_absolute_url methods in all the models
    for model in get_models():
        if hasattr(model, 'get_absolute_url'):
            model.get_absolute_url = patch_reverse(model.get_absolute_url)
