'''
Created on 11.11.2011

@author: whit
'''
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from ella_category_subdomain.models import CategorySubdomain
from ella.core.models import Category, Placement
from ella.core.cache import get_cached_object

class CategorySubdomainMiddleware:

    def __init__(self):
        def category_get_absolute_url(category):
            # taken from ella.core.models.Category except try/except statement
            if not category.tree_parent_id:
                url = reverse('root_homepage')
            else:
                url = reverse(
                        'category_detail',
                        kwargs={
                            'category' : category.tree_path,
                        }
                    )
            site = get_cached_object(Site, pk=category.site_id)
            if category.site_id != settings.SITE_ID:
                # prepend the domain if it doesn't match current Site
                return 'http://' + site.domain + url
            try:
                cs = category.categorysubdomain
            except CategorySubdomain.DoesNotExist:
                cs = None
            if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
                port = ':%s' % settings.DEVELOPMENT_SERVER_PORT
            else:
                port = ''
            if cs is None:
                absolute_url = 'http://%s%s/' % (site.domain, port)
            else:
                absolute_url = cs.get_absolute_url()
            url = url.lstrip('/' + category.slug)
            return absolute_url + url.lstrip('/')
        Category.get_absolute_url = category_get_absolute_url

        def placement_get_absolute_url(placement, domain=False):
            # taken from ella.core.models.Placement except try/except statement
            obj = placement.publishable
            category = placement.category

            kwargs = {
                'content_type' : slugify(obj.content_type.model_class()._meta.verbose_name_plural),
                'slug' : placement.slug,
            }

            if placement.static:
                if category.tree_parent_id:
                    kwargs['category'] = category.tree_path
                    url = reverse('static_detail', kwargs=kwargs)
                else:
                    url = reverse('home_static_detail', kwargs=kwargs)
            else:
                kwargs.update({
                        'year' : placement.publish_from.year,
                        'month' : placement.publish_from.month,
                        'day' : placement.publish_from.day,
                    })
                if category.tree_parent_id:
                    kwargs['category'] = category.tree_path
                    url = reverse('object_detail', kwargs=kwargs)
                else:
                    url = reverse('home_object_detail', kwargs=kwargs)

            site = get_cached_object(Site, pk=category.site_id)
            try:
                cs = category.categorysubdomain
            except CategorySubdomain.DoesNotExist:
                cs = None
            if settings.DEBUG and hasattr(settings, 'DEVELOPMENT_SERVER_PORT'):
                port = ':%s' % settings.DEVELOPMENT_SERVER_PORT
            else:
                port = ''
            if cs is None:
                absolute_url = 'http://%s%s/' % (site.domain, port)
            else:
                absolute_url = cs.get_absolute_url()
            url = url.lstrip('/' + category.slug)
            return absolute_url + url.lstrip('/')

            if category.site_id != settings.SITE_ID or domain:
                return 'http://' + site.domain + url
            return url
        Placement.get_absolute_url = placement_get_absolute_url

    def process_request(self, request):
        if request.path_info.startswith(settings.MEDIA_URL):
            return None
        sc = self._get_subdomain_category(request.get_host())
        if sc is not None:
            request.path_info = '/%s%s' % (sc.slug, request.path_info)
            request.path = '/%s%s' % (sc.slug, request.path)
        return None

    def process_response(self, request, response):
        return response


    def _get_subdomain_category(self, host):
        domain_parts = host.split('.')
        if (len(domain_parts) > 2):
            subdomain = domain_parts[0].lower()

            try:
                cs = CategorySubdomain.objects.get(subdomain_slug=subdomain)
                if cs.category.site.pk == settings.SITE_ID:
                    return cs.category
            except CategorySubdomain.DoesNotExist:
                return None

        return None
