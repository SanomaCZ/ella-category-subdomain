from urlparse import urlparse, urlunparse

from ella_category_subdomain.util import get_domain_for_category


def update_parsed_url_list(parsed_url_list):
    # If parsed_url has scheme attribute then preserve it,
    # else default to http.
    parsed_url_list[0] = parsed_url_list[0] or 'http'


def get_url_with_subdomain(parsed_url, category_subdomain):
    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    category_path = category_subdomain.category.tree_path

    # Strip category tree path (plus slash at the beginning).
    new_path = parsed_url.path[len(category_path) + 1:]

    # Get subdomain for given category.
    domain = category_subdomain.get_subdomain()

    # Change parsed_url_list.
    parsed_url_list[1:3] = domain, new_path

    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url_without_subdomain(parsed_url):
    # We will need mutable version of parsed_url.
    parsed_url_list = list(parsed_url)

    parsed_url_list[1] = get_domain_for_category(strip_www=False)
    update_parsed_url_list(parsed_url_list)

    # Construct and return new url.
    return urlunparse(parsed_url_list)


def get_url(url):
    from ella_category_subdomain.models import CategorySubdomain

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
        category_subdomain_list = CategorySubdomain.objects.filter(category__slug=first_path_item)
        # change the URL if found
        if (len(category_subdomain_list) == 1):
            url = get_url_with_subdomain(parsed_url, category_subdomain_list[0])

            return url

    # get the URL domain parts
    domain_items = parsed_url.netloc.split('.')
    # get the first domain part
    first_domain_item = domain_items[0]
    # search for the particular subdomain category
    category_subdomain_list = CategorySubdomain.objects.filter(subdomain_slug=first_domain_item)

    # the URL already modified if exists
    if (len(category_subdomain_list) > 0):
        return url
    # fill in the default subdomain otherwise
    else:
        url = get_url_without_subdomain(parsed_url)
        return url


def patch_reverse(reverse):
    def wrapper(*args, **kwargs):
        # Get url from a result of original Django reverse.
        return get_url(reverse(*args, **kwargs))
    wrapper._original_reverse = reverse
    return wrapper
