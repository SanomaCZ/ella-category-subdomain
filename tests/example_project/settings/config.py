from tempfile import gettempdir
from os.path import join, dirname
from .base import PROJECT_ROOT

import example_project

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SHOW_DEBUG_TOOLBAR = DEBUG

# database settings
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = join(PROJECT_ROOT, 'tmp', 'ecs_example.db')

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
