import pdb

from django.core import RegexURLResolver, RegexURLPattern, LocaleRegexURLResolver

class CategorySubdomainURLResolver(RegexURLResolver):
    """The class changes the behaviour of the parent to support Category Subdomains."""

    def __init__(self, parent_instance):
        super(CategorySubdomainURLResolver, self).__init__(
            regex = parent_instance.regex,
            urlconf_name = parent_instance.urlconf_name,
            default_kwargs=parent_instance.default_kwargs,
            app_name=parent_instance.app_name,
            namespace=parent_instance,
        )

    def resolve(self, path):
        resolved = super(CategorySubdomainURLPattern, self).resolve(path)
        pdb.set_trace()
        return resolved

    def reverse(self, lookup_view, *args, **kwargs):
        original = super(CategorySubdomainURLPattern, self).reverse(lookup_view, *args, **kwargs)
        pdb.set_trace()
        return original

class CategorySubdomainURLPattern(RegexURLPattern):

    def __init__(self, parent_instance):
        super(CategorySubdomainURLResolver, self).__init__(
            regex=parent_instance.regex,
            callback=parent_instance.callback,
            default_args=parent_instance.default_args,
            name=parent_instance.name
        )

    def resolve(self, path):
        resolved = super(CategorySubdomainURLPattern, self).resolve(path)
        pdb.set_trace()
        return resolved

class CategorySubdomainLocaleURLResolver(CategorySubdomainURLResolver):

    regex = LocaleRegexURLResolver.regex

    def __init__(self, parent_instance):
        super(CategorySubdomainLocaleURLResolver, self).__init__(parent_instance)

