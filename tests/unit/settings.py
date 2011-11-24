from tempfile import gettempdir
from os.path import dirname, join, normpath, pardir

FILE_ROOT = normpath(join(dirname(__file__), pardir))

DEBUG = True                                                                                            
TEMPLATE_DEBUG = DEBUG                                                                                  
DISABLE_CACHE_TEMPLATE = DEBUG                                                                                                       
                                                                                                        
DATABASE_ENGINE = 'sqlite3'                                                                             
DATABASE_NAME = join(gettempdir(), 'djangobaselibrary_unit_project.db')                                 
TEST_DATABASE_NAME =join(gettempdir(), 'test_unit_project.db')                                          
DATABASE_USER = ''                                                                                      
DATABASE_PASSWORD = ''                                                                                  
DATABASE_HOST = ''                                                                                      
DATABASE_PORT = ''                                                                                      
                                                                                                        
                                                                                                        
TIME_ZONE = 'Europe/Prague'                                                                             
                                                                                                        
LANGUAGE_CODE = 'en-us'                                                                                 
                                                                                                        
SITE_ID = 1                                                                                             
                                                                                                        
# Make this unique, and don't share it with anybody.                                                    
SECRET_KEY = '88b-01f^x4lh$-s5-hdccnicekg07)niir2g6)93!0#k(=mfv$'                                       

USE_I18N = True

MEDIA_ROOT = join(FILE_ROOT, 'static')

MEDIA_URL = '/static'

ADMIN_MEDIA_PREFIX = '/admin_media/'


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'unit_project.template_loader.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'djangobaselibrary.sample.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(FILE_ROOT, 'templates'),

)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.media',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',

    'ella.core',
    'ella.articles',
    'ella.photos',
    'ella_category_subdomain',
)

DEFAULT_PAGE_ID = 1

VERSION = 1


