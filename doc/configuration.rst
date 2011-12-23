.. _configuration:

Configuration
=============

The first step in actual code will be adding Ella Category Subdomain to your project's
``INSTALLED_APPS`` along with some required settings, the resulting values
(unchanged values are omitted) should look::

    ...
    INSTALLED_APPS = (            
        'django.contrib.admin',   
        'django.contrib.auth',    
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',   
        'django.contrib.redirects',
                                
        'ella_category_subdomain',
        'ella.core',
        'ella.photos',
        'ella.newman',
        'ella.articles',     

        'djangomarkup',
    )
    ...

.. note::
    Please note that the ``ella_category_subdomain`` application preceedes all other Ella applications.
    This is *REQUIRED* for the correct functionality.

Middleware
===========================

The ``CategorySubdomainMiddleware`` must be present in the application settings.::

    ...
    MIDDLEWARE_CLASSES = (
        'ella_category_subdomain.middleware.CategorySubdomainMiddleware',
    ) + MIDDLEWARE_CLASSES
    ...


RedirectMiddleware
===================================

Should you wish `Ella`_ to redirect the old style URL to a new ones, ``the CategorySubdomainRedirectMiddleware``
in the application settings::

    ...
    MIDDLEWARE_CLASSES = (
        'ella_category_subdomain.middleware.CategorySubdomainRedirectMiddleware',
    ) + MIDDLEWARE_CLASSES
    ...

.. _Ella: http://www.ellaproject.cz/

Settings
========

The Ella Category Subdomain application provides a new setting parameter called ``CATEGORY_SUBDOMAIN_OLD_STYLE_URL``.::

    ...
    CATEGORY_SUBDOMAIN_OLD_STYLE_URL = False
    ...

The parameter defaults to *False* and when set to *True*, it enables the old style URLs. These are URLs in the form 
used before the *Ella Category Subdomain* application has been used.

    * When *False* only new style URLs are allowed, throwing *404* error code when the old style URL is used.
    * When *True*, the both forms are allowed.
    * When *True* and the *CategorySubdomainRedirectMiddleware* is configured, the old style URLs are redirected to new ones.
   
The Ella Category Subdomain application provides a new setting parameter called ``CATEGORY_SUBDOMAIN_IGNORE_PATHS``.::   

	...    
	CATEGORY_SUBDOMAIN_IGNORE_PATHS = ['/feeds/rss', '/feeds/atom', ]
	...
	
The parameter is a list of URL paths which are not category related. As the list of all paths cannot be detected or found out
otherwise, so this has been added to help.
