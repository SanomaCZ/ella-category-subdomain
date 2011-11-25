from os.path import join, dirname, abspath
from tempfile import gettempdir

import example_project

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SHOW_DEBUG_TOOLBAR = DEBUG
DEVELOPMENT_SERVER_PORT = 8000

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(gettempdir(), 'example_project.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

SECRET_KEY = '1#h7o0k$ea%ciox$$p&@(r&1eokb*mvk(n(v9!wb11bt(^4$ns'

PROJECT_ROOT = dirname(abspath(__file__))

TIME_ZONE = 'Europe/Prague'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = join(PROJECT_ROOT, 'static')

MEDIA_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'ella.newman.context_processors.newman_media',
    'example_project.service.context_processors.simple_debug',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'ella_category_subdomain.middleware.CategorySubdomainMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'example_project.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',

    'ella.core',
    'ella.photos',
    'ella.newman',
    'ella.articles',

    'ella_category_subdomain',

    'djangomarkup',

    'example_project.service',
    'django_extensions',
    'debug_toolbar',
)

NEWMAN_MEDIA_PREFIX = MEDIA_URL + 'newman/'
# ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'

DEFAULT_MARKUP = 'markdown'

CACHE_BACKEND = 'dummy://'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
