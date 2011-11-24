from django.contrib.sites.models import Site
from ella.core.models import Category
from ella_category_subdomain.models import CategorySubdomain

def create_categories(case):
    case.site = Site.objects.get_current()
    case.root_category = Category.objects.create(title='Root', slug='root', tree_parent=None, tree_path='', site=case.site)
    case.category_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.root_category, tree_path='nested-1', site=case.site)
    case.category_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.root_category, tree_path='nested-2', site=case.site)
    case.category_nested_nested_1 = Category.objects.create(title='Nested Nested 1', slug='nested-nested-1', tree_parent=case.category_nested_1, tree_path='nested-1/nested-nested-1', site=case.site)
    case.category_nested_nested_2 = Category.objects.create(title='Nested Nested 2', slug='nested-nested-2', tree_parent=case.category_nested_2, tree_path='nested-2/nested-nested-2', site=case.site)
    CategorySubdomain.objects.create(category=case.category_nested_1, subdomain_slug='nested-1')
