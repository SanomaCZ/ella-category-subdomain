from django import template
from django.core.urlresolvers import reverse
from djangosanetesting import DatabaseTestCase

from ella_category_subdomain.monkeypatch import do_monkeypatch

from unit.helpers import create_categories

class TestAbsoluteURLsCase(DatabaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestAbsoluteURLsCase, self).__init__(*args, **kwargs)
        do_monkeypatch()

    def setUp(self):
        create_categories(self)

    def test_category_get_absolute_url_is_patched(self):
        self.assert_equals('http://nested-1.example.com/', self.category_nested_1.get_absolute_url())

    def test_category_get_absolute_url_works_for_second_level_categories(self):
        self.assert_equals('http://nested-1.example.com/nested-nested-1/', self.category_nested_nested_1.get_absolute_url())

    def test_category_reverse_is_patched(self):
        self.assert_equals('http://nested-1.example.com/', reverse('category_detail', args=(self.category_nested_1.slug,)))

    def test_category_reverse_works_for_second_level_categories(self):
        self.assert_equals('http://nested-1.example.com/nested-nested-1/', reverse('category_detail', args=(self.category_nested_nested_1.slug,)))

    def test_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.slug %}')

        var = {'category' : self.category_nested_1,}
        self.assert_equals('http://nested-1.example.com/', t.render(template.Context(var)))

    def test_url_tag_works_for_second_level_categories(self):
        t = template.Template('{% url category_detail category.slug %}')

        var = {'category' : self.category_nested_nested_1,}
        self.assert_equals('http://nested-1.example.com/nested-nested-1/', t.render(template.Context(var)))
