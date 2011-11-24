from djangosanetesting import DatabaseTestCase
from unit.helpers import create_categories
from django.core.urlresolvers import reverse

class TestAbsoluteURLsCase(DatabaseTestCase):

    def setUp(self):
        create_categories(self)

    def test_category_get_absolute_url_is_patched(self):
        self.assert_equals('http://nested-1.example.com/', self.category_nested_1.get_absolute_url())

    def test_category_reverse_is_patched(self):
        self.assert_equals('http://nested-1.example.com/', reverse('category_detail', args=(self.category_nested_1.slug,)))
