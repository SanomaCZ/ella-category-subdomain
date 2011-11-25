from django.contrib.sites.models import Site
from ella.core.models import Category
from ella_category_subdomain.models import CategorySubdomain

def create_categories(case):
    case.site = Site.objects.get_current()
    case.site.save()

    case.root_category = Category.objects.create(title='Root', slug='root', tree_parent=None, site=case.site)
    case.root_category.save()

    case.category_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.root_category, site=case.site)
    case.category_nested_1.save()

    case.category_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.root_category, site=case.site)
    case.category_nested_2.save()

    case.category_nested_nested_1 = Category.objects.create(title='Nested Nested 1', slug='nested-nested-1', tree_parent=case.category_nested_1, site=case.site)
    case.category_nested_nested_1.save()

    case.category_nested_nested_2 = Category.objects.create(title='Nested Nested 2', slug='nested-nested-2', tree_parent=case.category_nested_2, site=case.site)
    case.category_nested_nested_2.save()
