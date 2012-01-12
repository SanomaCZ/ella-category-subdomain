from tempfile import gettempdir
from os.path import dirname, join, normpath, pardir

FILE_ROOT = normpath(join(dirname(__file__), pardir))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DISABLE_CACHE_TEMPLATE = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(gettempdir(), 'ella_category_subdomain_unit.db'),
    }
}

TIME_ZONE = 'Europe/Prague'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

# Make this unique, and don't share it with anybody.
SECRET_KEY = '88b-01f^x4lh$-s5-hdccnicekg07)niir2g6)93!0#k(=mfv$'

USE_I18N = True

MEDIA_ROOT = join(FILE_ROOT, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'


MIDDLEWARE_CLASSES = (
    'ella_category_subdomain.middleware.CategorySubdomainMiddleware',
    'django.middleware.common.CommonMiddleware',
)

ROOT_URLCONF = 'unit.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(FILE_ROOT, 'templates'),

)

INSTALLED_APPS = (
    'ella_category_subdomain',
    'django.contrib.auth',
    'django.contrib.flatpages',
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'ella.core',
    'ella.articles',
    #'ella.photos',
    #'ella.polls',
)


