from django.core import RegexURLResolver, RegexURLPattern, LocaleRegexURLResolver

class CategorySubdomainURLResolver(RegexURLResolver):
    """The class changes the behaviour of the parent to support Category Subdomains."""

    def resolve(self, path):
        resolved = super(CategorySubdomainURLPattern, self).resolve(path)
        return resolved

    def reverse(self, lookup_view, *args, **kwargs):
        original = super(CategorySubdomainURLPattern, self).reverse(lookup_view, *args, **kwargs)
        return original

class CategorySubdomainURLPattern(RegexURLPattern):

    def resolve(self, path):
        resolved = super(CategorySubdomainURLPattern, self).resolve(path)
        return resolved

class CategorySubdomainLocaleURLResolver(CategorySubdomainURLResolver):

    regex = LocaleRegexURLResolver.regex

    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        super(CategorySubdomainLocaleURLResolver, self).__init__(
            None, urlconf_name, default_kwargs, app_name, namespace)
