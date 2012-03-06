from django.conf import settings

from ella.utils.settings import Settings

OLD_STYLE_URL = False

IGNORE_PATHS = ['/feeds/rss', '/feeds/atom', ]
if (settings.MEDIA_URL):
    IGNORE_PATHS.append(settings.MEDIA_URL)
if (settings.STATIC_URL):
    IGNORE_PATHS.append(settings.STATIC_URL)

ella_category_subdomain_settings = Settings('ella_category_subdomain.conf',
                                            'CATEGORY_SUBDOMAIN')
