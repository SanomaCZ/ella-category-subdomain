from django.conf import settings
from django.test import TestCase

from nose import tools

from ella_category_subdomain.util import is_path_ignored

class TestIgnorePaths(TestCase):

    def setUp(self):
        super(TestIgnorePaths, self).setUp()
        settings.CATEGORY_SUBDOMAIN_IGNORE_PATHS = ['/ign_path']

    def test_normal_path(self):
        tools.assert_false(is_path_ignored('/normal_path/sub_path/'))

    def test_ignored_path(self):
        tools.assert_true(is_path_ignored('/ign_path/'))
        tools.assert_true(is_path_ignored('/ign_path/sub_path'))
