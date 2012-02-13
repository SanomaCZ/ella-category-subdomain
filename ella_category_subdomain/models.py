import inspect

import django.core.urlresolvers as urlresolvers

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import class_prepared
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module

from ella.core.models import Category
from ella.core.cache.utils import get_cached_object

from ella_category_subdomain.monkeypatch import patch_reverse
from ella_category_subdomain.util import get_domain_for_category


class CategorySubdomainManager(models.Manager):

    def get_for_path(self, path):
        """Returns a CategorySubdomain instance for a first part of the path
        if present in the database.
        """
        path_items = [path_item for path_item in path.split('/') if len(path_item) > 0]
        result = None
        if (len(path_items) > 0):
            slug = path_items[0]
            try:
                result = get_cached_object(self.model, \
                        category__slug=slug, category__site__id=settings.SITE_ID)
            except self.model.DoesNotExist:
                pass

        return result

    def get_for_host(self, host):
        """Searches for a CategorySubdomain instance matching the first part
        of the domain.
        """
        # split the domain into parts
        domain_parts = host.split('.')
        # prepare the default response
        result = None
        # process the domain if it is of the 3rd level or more
        if (len(domain_parts) > 2):
            # get the first part of the domain
            subdomain = domain_parts[0].lower()

            try:
                # get the category subdomain
                result = get_cached_object(self.model, \
                        subdomain_slug=subdomain, category__site__id=settings.SITE_ID)

            except self.model.DoesNotExist:
                # category subdomain does not exists
                pass

        return result


class CategorySubdomain(models.Model):
    objects = CategorySubdomainManager()

    category = models.OneToOneField(Category)
    subdomain_slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return self.subdomain_slug

    def get_domain(self, strip_www=True):
        domain = get_domain_for_category(self.category, strip_www)
        return domain

    def get_subdomain(self):
        return '%s.%s' % (self.subdomain_slug, self.get_domain())

    def get_absolute_url(self):
        return "http://%s.%s/" % (self.subdomain_slug, self.get_domain(),)

    def clean(self):
        """Validates that only first level category is referenced by the CategorySubdomain
        """
        if ((self.category.tree_parent is None) or
            (self.category.tree_parent.tree_parent is not None)):
            raise ValidationError(_('Subdomain can only reference a first level categories'))

    class Meta:
        unique_together = (('category', 'subdomain_slug'),)
        verbose_name = _('Category Subdomain')
        verbose_name_plural = _('Category Subdomains')

# Flag which indicates that the patches were already implemented
PATCHED = 0


@receiver(class_prepared)
def patch_stuff(sender, **kwargs):
    """The method applies patches upon receiving 'class_prepared' signal. It wraps 'resolve' method of
    the django urlresolvers module and 'get_absolute_url' method of all ella model instances having the
    method.
    """
    # reference the global flag
    global PATCHED
    # bail out it the path has been applied already
    if PATCHED:
        return

    # raise the flag of patch application
    PATCHED = 1

    # raise an error if the current application does not precede any other ella application
    ella_found = False
    for app in settings.INSTALLED_APPS:
        if ((app.startswith('ella')) and
            (app != 'ella_category_subdomain')):
            ella_found = True

        if app == 'ella_category_subdomain':
            if ella_found:
                raise ImproperlyConfigured(_('Ella category subdomain application must precede any other ella application in INSTALLED_APPS.'))
            else:
                break

    # prepare the buffer carrying the model class already patched. Each import can bring models already pathed.
    patched_models = {}

    # go through all the installed applications
    for app in settings.INSTALLED_APPS:
        # process only apps belonging to the ella framework and skip self
        if ((app.startswith('ella')) and
            (app != 'ella_category_subdomain')):

            try:
                # import the models package
                module = import_module('.models', app)
                # get all the package members
                module_members = inspect.getmembers(module)

                # wrap all the 'get_absolute_url' method in all the Model subclasses found
                for name, member in module_members:
                    if ((inspect.isclass(member)) and
                        (issubclass(member, models.Model)) and
                        (patched_models.get(name) is None)):

                        # record the class has been processed
                        patched_models[name] = 1
                        # wrap the 'get_absolute_url' method
                        if hasattr(member, 'get_absolute_url'):
                            member.get_absolute_url = patch_reverse(member.get_absolute_url)
            except ImportError:
                pass

    # patch the reverse function
    urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
