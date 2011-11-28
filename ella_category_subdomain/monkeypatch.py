import django.conf.urls.defaults
from django.core.urlresolvers import RegexURLResolver
from django.core.urlresolvers import RegexURLPattern

from .models import CategorySubdomain
from ella.core.models import Category, Placement
from ella.core.cache import get_cached_object

from ella_category_subdomain.urlresolvers import CategorySubdomainURLPattern
from ella_category_subdomain.urlresolvers import CategorySubdomainURLResolver
#from ella_category_subdomain.urlresolvers import CategorySubdomainLocaleURLResolver


original_url = django.conf.urls.defaults.url

def url(regex, view, kwargs=None, name=None, prefix=''):
    regex_url = original_url(regex, view, kwargs, name, prefix)
    if isinstance(regex_url, RegexURLPattern):
        regex_url = CategorySubdomainURLPattern(regex, regex_url)
    if isinstance(regex_url, RegexURLResolver):
        regex_url = CategorySubdomainURLResolver(regex, regex_url)
    return regex_url


def do_monkeypatch():
    django.conf.urls.defaults.url = url
