from urlparse import urlparse, urlunparse

# JS: nepouzity import
import logging

from django.db.models import get_models
from django.db.models.signals import class_prepared
import django.conf.urls.defaults
import django.core.urlresolvers as urlresolvers
from django.dispatch import receiver

from django.conf import settings

from ella_category_subdomain.util import get_domain_for_category

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
    # JS: myslim, ze doporuceni je psat mala pismena a bez tecky na konci, pokud jde o jednu vetu
    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    category_path = category_subdomain.category.tree_path

    # Strip category tree path (plus slash at the beginning).
    new_path = parsed_url.path[len(category_path)+1:]

    # Get subdomain for given category.
    domain = category_subdomain.get_subdomain()

    # Change parsed_url_list.
    parsed_url_list[1:3] = domain, new_path

    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url_without_subdomain(parsed_url):
    parts = parsed_url.netloc.split('.')

    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    parsed_url_list[1] = get_domain_for_category(strip_www = False)
    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url(url):
    from ella_category_subdomain.models import CategorySubdomain

    logging.warning("Parsing URL: %s" % (url,))
    # parse url
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
            url = get_url_with_subdomain(parsed_url, category_subdomain_list[0])
            logging.warning("Result with subdomain URL: %s" % (url,))

            return url

    # get the URL domain parts
    domain_items = parsed_url.netloc.split('.')
    # get the first domain part
    first_domain_item = domain_items[0]
    # search for the particular subdomain category
    category_subdomain_list = CategorySubdomain.objects.filter(subdomain_slug = first_domain_item)

    # the URL already modified if exists
    if (len(category_subdomain_list) > 0):
        logging.warning("Result unchanged")
        return url
    # fill in the default subdomain otherwise
    else:
        url = get_url_without_subdomain(parsed_url)
        logging.warning("Result URL: %s" % (url,))
        return url

def new_resolve(path):
    logging.warning("Patched resolv: %s" % (path))
    return path

def patch_resolve(resolve):
    def wrapper(*args, **kwargs):
        # Get url from a result of original Django reverse.
        return new_resolve(resolve(*args, **kwargs))
    wrapper._original_resolve = resolve
    return wrapper


def patch_reverse(reverse):
    def wrapper(*args, **kwargs):
        # Get url from a result of original Django reverse.
        return get_url(reverse(*args, **kwargs))
    wrapper._original_reverse = reverse
    return wrapper


#@receiver(class_prepared)
#def patchmodel(sender, **kwargs):
#    if hasattr(sender, 'get_absolute_url'):
#        logging.warning("patching model: %s" % (sender))
#        sender.get_absolute_url = patch_reverse(sender.get_absolute_url)
#    else:
#        logging.warning("not patching model: %s" % (sender))
#
#    if not hasattr(urlresolvers.reverse, '_original_reverse'):
#        logging.warning("patching reverse")
#        urlresolvers.reverse = patch_reverse(urlresolvers.reverse)


#def do_monkeypatch():
#    # Replace django.core.urlresolvers.reverse and do it only once.
#    if not hasattr(urlresolvers.reverse, '_original_reverse'):
#        urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
#
#    # Replace get all the get_absolute_url methods in all the models
#    for model in get_models():
#        if hasattr(model, 'get_absolute_url'):
#            model.get_absolute_url = patch_reverse(model.get_absolute_url)
