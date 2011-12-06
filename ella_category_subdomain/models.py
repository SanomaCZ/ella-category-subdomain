import importlib
import inspect
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import django.core.urlresolvers as urlresolvers

from ella.core.models import Category

from ella_category_subdomain.monkeypatch import patch_reverse
from ella_category_subdomain.util import get_domain_for_category

class CategorySubdomain(models.Model):
    category = models.OneToOneField(Category)
    subdomain_slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return self.subdomain_slug

    def get_domain(self, strip_www = True):
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
        verbose_name = _('SEO Category')
        verbose_name_plural = _('SEO Categories')


patched_models = {}

for app in settings.INSTALLED_APPS:
    if app.startswith('ella'):

        if (app == 'ella_category_subdomain'):
            continue
        logging.warning("Module to import: %s" % (app))
        module = importlib.import_module('%s.models' % (app,))
        module_members = inspect.getmembers(module)
        for name, member in module_members:
            if ((inspect.isclass(member)) and
                (patched_models.get(name, None) is None)):
                patched_models[name] = 1
                if hasattr(member, 'get_absolute_url'):
                    member.get_absolute_url = patch_reverse(member.get_absolute_url)

urlresolvers.reverse = patch_reverse(urlresolvers.reverse)
