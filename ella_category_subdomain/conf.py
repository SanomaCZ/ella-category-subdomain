from ella.utils.settings import Settings

OLD_STYLE_URL = False

IGNORE_PATHS = ['/feeds/rss', '/feeds/atom', ]

ella_category_subdomain_settings = Settings('ella_category_subdomain.conf',
                                            'CATEGORY_SUBDOMAIN')
