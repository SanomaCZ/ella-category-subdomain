from django.db import models
from django.utils.translation import ugettext_lazy as _

from ella.core.models import Category

class SeoCat(models.Model):
    category = models.OneToOneField(Category)
    subdomain_slug = models.SlugField(max_length=64)

    def __unicode__(self):
        return self.subdomain_slug

    def get_absolute_url(self):
        d = self.category.site.domain
        # FIXME: ugly
        if d.startswith('www.'):
            return "http://%s/" % d.replace('www', self.subdomain_slug)
        else:
            return "http://%s.%s/" % (self.subdomain_slug, d)

    class Meta:
        unique_together = (('category', 'subdomain_slug'),)
        verbose_name = _('SEO Category')
        verbose_name_plural = _('SEO Categories')

# XXX: monkey-patch ella views?
# from ella.core.views import ObjectDetail, ListContentType

