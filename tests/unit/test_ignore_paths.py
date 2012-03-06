from django.conf import settings
from django.test import TestCase

from nose import tools

from ella_category_subdomain.conf import ella_category_subdomain_settings
from ella_category_subdomain.models import CategorySubdomain
from ella_category_subdomain.monkeypatch import get_url
from ella_category_subdomain.util import is_path_ignored
from unit.helpers import create_categories_site

class TestIgnorePaths(TestCase):

    def setUp(self):
        super(TestIgnorePaths, self).setUp()
        self.original_ignore_path = ella_category_subdomain_settings.IGNORE_PATHS
        ella_category_subdomain_settings.IGNORE_PATHS = ['/ign_path', '/nested-1/']
        create_categories_site(self)
        self.category_subdomain_nested_2 = CategorySubdomain.objects.create(category=self.category_nested_2, subdomain_slug='nested-two')
        self.category_subdomain_nested_2.save()
        settings.SITE_ID = self.site_1_id


    def tearDown(self):
        ella_category_subdomain_settings.IGNORE_PATHS = self.original_ignore_path

    def test_normal_path(self):
        tools.assert_false(is_path_ignored('/normal_path/sub_path/'))

    def test_ignored_path(self):
        tools.assert_true(is_path_ignored('/ign_path/'))
        tools.assert_true(is_path_ignored('/ign_path/sub_path'))

    def test_category_subdomain_get_url_ignores(self):
        tools.assert_equals('/nested-1/', get_url('/nested-1/'))

    def test_category_subdomain_get_url_non_ignore(self):
        tools.assert_equals('http://nested-two.example.com/', get_url('/nested-2/'))

    def test_category_subdomain_get_absolute_url_ignored(self):
        tools.assert_equals('/nested-1/', self.category_nested_1.get_absolute_url())

    def test_category_subdomain_get_absolute_url_non_ignore(self):
        tools.assert_equals('http://nested-two.example.com/', self.category_nested_2.get_absolute_url())

    def test_category_subdomain_reverse_ignored(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('/nested-1/', reverse('category_detail', args=(self.category_nested_1.tree_path,)))

    def test_category_subdomain_reverse_non_ignore(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-two.example.com/',reverse('category_detail', args=(self.category_nested_2.tree_path,)))
