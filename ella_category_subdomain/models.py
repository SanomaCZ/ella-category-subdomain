from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ella.core.models import Category

class CategorySubdomain(models.Model):
    category = models.OneToOneField(Category)
    subdomain_slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return self.subdomain_slug

    def get_absolute_url(self):
        domain = self.category.site.domain
        # FIXME: ugly
        if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
            port = ':%s' % settings.DEVELOPMENT_SERVER_PORT
        else:
            port = ''
        if domain.startswith('www.'):
            subdomain = domain.replace('www', self.subdomain_slug)
            return "http://%s%s/" % (subdomain, port)
        else:
            return "http://%s.%s%s/" % (self.subdomain_slug, domain, port)

    class Meta:
        unique_together = (('category', 'subdomain_slug'),)
        verbose_name = _('SEO Category')
        verbose_name_plural = _('SEO Categories')

# XXX: monkey-patch ella views?
# from ella.core.views import ObjectDetail, ListContentType

