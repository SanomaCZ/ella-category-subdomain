from django.conf import settings

from ella.utils.settings import Settings

OLD_STYLE_URL = False

IGNORE_PATHS = ['/feeds/rss', '/feeds/atom', ]
IGNORE_PATHS.extend([settings.MEDIA_URL, settings.STATIC_URL])

ella_category_subdomain_settings = Settings('ella_category_subdomain.conf',
                                            'CATEGORY_SUBDOMAIN')
