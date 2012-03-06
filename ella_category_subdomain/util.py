from django.contrib.sites.models import Site
from django.conf import settings

from ella_category_subdomain.conf import ella_category_subdomain_settings


def get_domain_for_category(category=None, strip_www=False):
    """Return site domain with development server port (if DEBUG)."""

    if category is not None:
        domain = category.site.domain
    # get the site domain otherwise
    else:
        domain = Site.objects.get_current().domain

    # append the port to the domain when neccessary
    if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
        domain = '%s:%s' % (domain, settings.DEVELOPMENT_SERVER_PORT,)

    www = 'www.'
    domain = domain[len(www):] if domain.startswith(www) and strip_www else domain
    return domain


def is_path_ignored(path):
    """Returns True if the path is being ignored by the application"""
    for prefix in ella_category_subdomain_settings.IGNORE_PATHS:
        if path.startswith(prefix):
            return True
    return False

