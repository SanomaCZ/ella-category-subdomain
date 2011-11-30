from django.contrib.sites.models import Site
from django.conf import settings

from ella.core.models import Category

categories = sorted(Category.objects.all())

def simple_debug(request):
    return {'categories': categories,
            'request': request,
            'domain': Site.objects.get(pk=settings.SITE_ID).domain,
            'port': settings.DEVELOPMENT_SERVER_PORT,
           }
