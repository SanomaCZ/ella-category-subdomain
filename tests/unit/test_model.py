from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djangosanetesting import DatabaseTestCase

from ella.core.models import Category
from ella_category_subdomain.models import CategorySubdomain

from unit.helpers import create_categories_site

class TestModelCase(DatabaseTestCase):

    def setUp(self):
        super(TestModelCase, self).setUp()
        create_categories_site(self)
        settings.SITE_ID = self.site_1_id

    def test_root_category_cannot_be_user_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_root, subdomain_slug = self.category_root.slug)
        self.assert_raises(ValidationError, cs.clean)

    def test_first_level_category_validates_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_nested_1, subdomain_slug = self.category_nested_1.slug)
        self.assert_is_none(cs.clean())

    def test_second_level_category_cannot_be_user_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_nested_nested_2, subdomain_slug = self.category_nested_nested_2.slug)
        self.assert_raises(ValidationError, cs.clean)

    def test_category_can_be_referenced_by_only_one_subdomain(self):
        cs1 = CategorySubdomain(category = self.category_nested_2, subdomain_slug = self.category_nested_2.slug)
        cs1.save()
        cs2 = CategorySubdomain(category = self.category_nested_2, subdomain_slug = self.category_nested_2.slug)
        self.assert_raises(IntegrityError, cs2.save)

    def test_get_category_subdomain_for_host_example_com(self):
        host = "example.com"
        self.assert_is_none(CategorySubdomain.get_category_subdomain_for_host(host))

    def test_get_category_subdomain_for_host_www_example_com(self):
        host = "www.example.com"
        self.assert_is_none(CategorySubdomain.get_category_subdomain_for_host(host))

    def test_get_category_subdomain_for_host_nocategory_example_com(self):
        host = "nocategory.example.com"
        self.assert_is_none(CategorySubdomain.get_category_subdomain_for_host(host))

    def test_get_category_subdomain_for_host_nested_one_example_com(self):
        host = "nested-one.example.com"
        category_subdomain = CategorySubdomain.get_category_subdomain_for_host(host)
        self.assert_is_not_none(category_subdomain)
        self.assert_equals(category_subdomain.subdomain_slug, 'nested-one')

    def test_get_category_subdomain_for_path(self):
        path = "/"
        self.assert_is_none(CategorySubdomain.get_category_subdomain_for_path(path))

    def test_get_category_subdomain_for_path_nosubdomain(self):
        path = "/nosubdomain/"
        self.assert_is_none(CategorySubdomain.get_category_subdomain_for_path(path))

    def test_get_category_subdomain_for_path_nested_1(self):
        path = "/nested-1/"
        category_subdomain = CategorySubdomain.get_category_subdomain_for_path(path)
        self.assert_is_not_none(category_subdomain)
        self.assert_equals(category_subdomain.subdomain_slug, 'nested-one')

    def test_get_category_subdomain_for_path_nested_nested_1(self):
        path = "/nested-1/nested-nested-1"
        category_subdomain = CategorySubdomain.get_category_subdomain_for_path(path)
        self.assert_is_not_none(category_subdomain)
        self.assert_equals(category_subdomain.subdomain_slug, 'nested-one')
