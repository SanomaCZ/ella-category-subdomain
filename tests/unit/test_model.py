from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.test import TestCase
from nose import tools

from ella_category_subdomain.models import CategorySubdomain

from unit.helpers import create_categories_site

class TestModelCase(TestCase):

    def setUp(self):
        super(TestModelCase, self).setUp()
        create_categories_site(self)
        settings.SITE_ID = self.site_1_id

    def test_root_category_cannot_be_user_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_root, subdomain_slug = self.category_root.slug)
        tools.assert_raises(ValidationError, cs.clean)

    def test_first_level_category_validates_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_nested_1, subdomain_slug = self.category_nested_1.slug)
        tools.assert_false(cs.clean())

    def test_second_level_category_cannot_be_user_for_subdomain(self):
        cs = CategorySubdomain(category = self.category_nested_nested_2, subdomain_slug = self.category_nested_nested_2.slug)
        tools.assert_raises(ValidationError, cs.clean)

    def test_category_can_be_referenced_by_only_one_subdomain(self):
        cs1 = CategorySubdomain(category = self.category_nested_2, subdomain_slug = self.category_nested_2.slug)
        cs1.save()
        cs2 = CategorySubdomain(category = self.category_nested_2, subdomain_slug = self.category_nested_2.slug)
        tools.assert_raises(IntegrityError, cs2.save)

    def test_get_category_subdomain_for_host_example_com(self):
        host = "example.com"
        tools.assert_false(CategorySubdomain.objects.get_for_host(host))

    def test_get_category_subdomain_for_host_www_example_com(self):
        host = "www.example.com"
        tools.assert_false(CategorySubdomain.objects.get_for_host(host))

    def test_get_category_subdomain_for_host_nocategory_example_com(self):
        host = "nocategory.example.com"
        tools.assert_false(CategorySubdomain.objects.get_for_host(host))

    def test_get_category_subdomain_for_host_nested_one_example_com(self):
        host = "nested-one.example.com"
        category_subdomain = CategorySubdomain.objects.get_for_host(host)
        tools.assert_true(category_subdomain)
        tools.assert_equals(category_subdomain.subdomain_slug, 'nested-one')

    def test_get_category_subdomain_for_path(self):
        path = "/"
        tools.assert_false(CategorySubdomain.objects.get_for_path(path))

    def test_get_category_subdomain_for_path_nosubdomain(self):
        path = "/nosubdomain/"
        tools.assert_false(CategorySubdomain.objects.get_for_path(path))

    def test_get_category_subdomain_for_path_nested_1(self):
        path = "/nested-1/"
        category_subdomain = CategorySubdomain.objects.get_for_path(path)
        tools.assert_true(category_subdomain)
        tools.assert_equals(category_subdomain.subdomain_slug, 'nested-one')

    def test_get_category_subdomain_for_path_nested_nested_1(self):
        path = "/nested-1/nested-nested-1"
        category_subdomain = CategorySubdomain.objects.get_for_path(path)
        tools.assert_true(category_subdomain)
        tools.assert_equals(category_subdomain.subdomain_slug, 'nested-one')
