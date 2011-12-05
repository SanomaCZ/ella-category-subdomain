import logging

from django.conf import settings
from django.contrib.sites.models import Site

from ella.core.models import Category


def get_domain_for_category(category=None, strip_www=False):
    """Return site domain with development server port (if DEBUG)."""
    # get the domain for the category if defined

    if category is not None:
        domain = category.site.domain
    # get the site domain otherwise
    else:
        domain = Site.objects.get(pk = settings.SITE_ID).domain

    # append the port to the domain when neccessary
    if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
        domain = '%s:%s' % (domain, settings.DEVELOPMENT_SERVER_PORT,)

    www = 'www.'
    logging.warning("Original domain: %s" % (domain,))
    domain = domain[len(www):] if domain.startswith(www) and strip_www else domain
    logging.warning("Stripped domain: %s" % (domain,))
    return domain

