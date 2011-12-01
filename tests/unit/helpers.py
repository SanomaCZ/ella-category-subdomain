import datetime
import logging

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site

from ella.core.models import Category
from ella.core.models import Author
from ella.core.models import Placement
from ella.articles.models import Article
from ella_category_subdomain.models import CategorySubdomain

def create_categories_site(case):
    # site 1
    case.site_1 = Site.objects.create(name="example.com", domain="example.com")
    case.site_1.save()
    case.site_1_id = case.site_1.id

    # site 1 categories
    case.category_root = Category.objects.create(title='Root', slug='root_homepage', tree_parent=None, site=case.site_1)
    case.category_root.save()

    case.category_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.category_root, site=case.site_1)
    case.category_nested_1.save()

    case.category_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.category_root, site=case.site_1)
    case.category_nested_2.save()

    case.category_nested_nested_1 = Category.objects.create(title='Nested Nested 1', slug='nested-nested-1', tree_parent=case.category_nested_1, site=case.site_1)
    case.category_nested_nested_1.save()

    case.category_nested_nested_2 = Category.objects.create(title='Nested Nested 2', slug='nested-nested-2', tree_parent=case.category_nested_2, site=case.site_1)
    case.category_nested_nested_2.save()

    case.category_subdomain_nested_1 = CategorySubdomain.objects.create(category=case.category_nested_1, subdomain_slug='nested-one')
    case.category_subdomain_nested_1.save()

    # site 1 articles
    publish_from = datetime.datetime(2011, 9, 1)

    author = Author.objects.create(name='User', slug='user')
    author.save()

    case.article_root = Article(category=case.category_root, title='Root Article', slug='root-article',)
    case.article_root.save()
    case.article_root.authors.add(author)

    case.placement_root = Placement.objects.create(publishable=case.article_root, category=case.category_root, publish_from=publish_from,)
    case.placement_root.save()

    case.article_nested_1 = Article(category=case.category_nested_1, title='Nested 1 Article', slug='nested-1-article',)
    case.article_nested_1.save()
    case.article_nested_1.authors.add(author)

    case.placement_nested_1 = Placement.objects.create(publishable=case.article_nested_1, category=case.category_nested_1, publish_from=publish_from,)
    case.placement_nested_1.save()

    case.article_nested_nested_1 = Article(category=case.category_nested_nested_1, title='Nested Nested 1 Article', slug='nested-nested-1-article',)
    case.article_nested_nested_1.save()
    case.article_nested_nested_1.authors.add(author)

    case.placement_nested_nested_1 = Placement.objects.create(publishable=case.article_nested_nested_1, category=case.category_nested_nested_1, publish_from=publish_from,)
    case.placement_nested_nested_1.save()

    case.article_nested_2 = Article(category=case.category_nested_2, title='Nested 2 Article', slug='nested-2-article',)
    case.article_nested_2.save()
    case.article_nested_2.authors.add(author)

    case.placement_nested_2 = Placement.objects.create(publishable=case.article_nested_2, category=case.category_nested_2, publish_from=publish_from,)
    case.placement_nested_2.save()

    case.article_nested_nested_2 = Article(category=case.category_nested_nested_2, title='Nested 2 Article', slug='nested-2-article',)
    case.article_nested_nested_2.save()
    case.article_nested_nested_2.authors.add(author)

    case.placement_nested_nested_2 = Placement.objects.create(publishable=case.article_nested_nested_2, category=case.category_nested_nested_2, publish_from=publish_from,)
    case.placement_nested_nested_2.save()

    # site 2
    case.site_2 = Site.objects.create(name="example1.com", domain="example1.com")
    case.site_2.save()
    case.site_2_id = case.site_2.id

    # site 2 categories
    case.site_2_root = Category.objects.create(title='Root', slug='root', tree_parent=None, site=case.site_2)
    case.site_2_root.save()

    case.site_2_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.site_2_root, site=case.site_2)
    case.site_2_nested_1.save()

    case.site_2_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.site_2_root, site=case.site_2)
    case.site_2_nested_2.save()

    # site 3
    case.site_3 = Site.objects.create(name="www.example.com", domain="www.example.com")
    case.site_3.save()
    case.site_3_id = case.site_3.id

    # site 3 categories
    case.site_3_root = Category.objects.create(title='Root', slug='root', tree_parent=None, site=case.site_3)
    case.site_3_root.save()

    case.site_3_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.site_3_root, site=case.site_3)
    case.site_3_nested_1.save()

    case.site_3_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.site_3_root, site=case.site_3)
    case.site_3_nested_2.save()

    # site 4
    case.site_4 = Site.objects.create(name="www.example.co.uk", domain="www.example.co.uk")
    case.site_4.save()
    case.site_4_id = case.site_4.id

    # site 4 categories
    case.site_4_root = Category.objects.create(title='Root', slug='root', tree_parent=None, site=case.site_4)
    case.site_4_root.save()

    case.site_4_nested_1 = Category.objects.create(title='Nested 1', slug='nested-1', tree_parent=case.site_4_root, site=case.site_4)
    case.site_4_nested_1.save()

    case.site_4_nested_2 = Category.objects.create(title='Nested 2', slug='nested-2', tree_parent=case.site_4_root, site=case.site_4)
    case.site_4_nested_2.save()
