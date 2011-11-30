from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ella.core.models import Category

class CategorySubdomain(models.Model):
    category = models.OneToOneField(Category)
    subdomain_slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return self.subdomain_slug

    def get_site_domain(self):
        """Get site domain without leading www."""
        domain = self.category.site.domain
        return domain[4:] if domain.startswith('www.') else domain

    def get_subdomain(self):
        return '%s.%s' % (self.subdomain_slug, self.get_site_domain())

    def get_absolute_url(self):
        return "http://%s%s/" % (self.get_subdomain(), port)

    @staticmethod
    def _development_server_port():
        if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
            return ':%s' % settings.DEVELOPMENT_SERVER_PORT
        else:
            return ''

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

