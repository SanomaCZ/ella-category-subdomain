from tempfile import gettempdir
from os.path import join, dirname
from .base import PROJECT_ROOT

# import example_project

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SHOW_DEBUG_TOOLBAR = DEBUG
DEVELOPMENT_SERVER_PORT = 8000

# database settings
join(PROJECT_ROOT, 'tmp', 'example.db')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': join(PROJECT_ROOT, 'tmp', 'example.db'), # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1#h7o0k$ea%ciox$$p&@(r&1eokb*mvk(n(v9!wb11bt(^4$ns'

# cache settings
CACHE_BACKEND = 'dummy://'

# DEBUG TOOLBAR
if DEBUG and SHOW_DEBUG_TOOLBAR:
    try:
        from sensa.settings.enable_debug_toolbar import *
    except ImportError:
        pass

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
