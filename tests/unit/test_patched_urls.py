from django import template
from djangosanetesting import DatabaseTestCase

from ella_category_subdomain.monkeypatch import do_monkeypatch

from unit.helpers import create_categories

class TestAbsoluteURLsCase(DatabaseTestCase):

    def __init__(self, *args, **kwargs):
        super(TestAbsoluteURLsCase, self).__init__(*args, **kwargs)
        do_monkeypatch()

    def setUp(self):
        create_categories(self)

    # get_absolute_url testes

    def test_root_category_get_absolute_urls_works_unaffected(self):
        self.assert_equals('http://example.com/', self.category_root.get_absolute_url())

    def test_root_article_get_absolute_urls_works_unaffected(self):
        self.assert_equals('http://example.com/', self.article_root.get_absolute_url())

    def test_category_get_absolute_url_is_patched(self):
        self.assert_equals('http://nested-one.example.com/', self.category_nested_1.get_absolute_url())

    def test_first_level_article_get_absolute_url_is_patched(self):
        self.assert_equals('http://nested-one.example.com/', self.article_nested_1.get_absolute_url())

    def test_category_get_absolute_url_works_for_second_level_categories(self):
        self.assert_equals('http://nested-one.example.com/nested-nested-1/', self.category_nested_nested_1.get_absolute_url())

    def test_no_subdomain_category_get_absolute_url_works_unaffected(self):
        self.assert_equals('http://example.com/nested-2/', self.category_nested_2.get_absolute_url())

    def test_no_subdomain_second_level_category_get_absolute_url_works_unaffected(self):
        self.assert_equals('http://example.com/nested-2/nested-nested-2/', self.category_nested_nested_2.get_absolute_url())

    # pathed reverse tests

    def test_root_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        self.assert_equals('http://example.com/', reverse('category_detail', args=('/',)))

    def test_category_reverse_is_patched(self):
        from django.core.urlresolvers import reverse
        self.assert_equals('http://nested-one.example.com/', reverse('category_detail', args=(self.category_nested_1.tree_path,)))

    def test_category_reverse_works_for_second_level_categories(self):
        from django.core.urlresolvers import reverse
        self.assert_equals('http://nested-one.example.com/nested-nested-1/', reverse('category_detail', args=(self.category_nested_nested_1.tree_path,)))

    def test_no_subdomain_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        self.assert_equals('http://example.com/nested-2/', reverse('category_detail', args=(self.category_nested_2.tree_path,)))

    def test_no_subdomain_second_level_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        self.assert_equals('http://example.com/nested-2/nested-nested-2/', reverse('category_detail', args=(self.category_nested_nested_2.tree_path,)))

    # url tag tests

    def test_root_category_url_tag_work_unaffected(self):
        t = template.Template('{% url category_detail category %}')

        var = {'category' : '/',}
        self.assert_equals('http://example.com/', t.render(template.Context(var)))

    def test_root_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : '/', 'content_type': 'articles', 'slug': self.placement_root.slug, 'year': 2011, 'month': 11, 'day': 1}
        self.assert_equals('http://example.com/2011/11/1/articles/root-article/', t.render(template.Context(var)))

    def test_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_1,}
        self.assert_equals('http://nested-one.example.com/', t.render(template.Context(var)))

    def test_url_tag_works_first_level_article(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : '/', 'content_type': 'articles', 'slug': self.placement_nested_1.slug, 'year': 2011, 'month': 11, 'day': 1}
        self.assert_equals('http://nested-one.example.com/2011/11/1/articles/nested-1-article/', t.render(template.Context(var)))

    def test_url_tag_works_for_second_level_categories(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_nested_1,}
        self.assert_equals('http://nested-one.example.com/nested-nested-1/', t.render(template.Context(var)))

    def test_url_tag_works_second_level_article(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : '/', 'content_type': 'articles', 'slug': self.placement_nested_nested_1.slug, 'year': 2011, 'month': 11, 'day': 1}
        self.assert_equals('http://nested-one.example.com/nested-nested-1/2011/11/1/articles/nested-1-article/', t.render(template.Context(var)))

    def test_no_subdomain_category_url_tag_works_unaffected(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_2,}
        self.assert_equals('http://example.com/nested-2/', t.render(template.Context(var)))

    def test_no_subdomain_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_2.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_2.slug, 'year': 2011, 'month': 11, 'day': 1}
        self.assert_equals('http://example.com/nested-2/2011/11/1/articles/nested-2-article/', t.render(template.Context(var)))

    def test_no_subdomain_second_level_category_url_tag_works_unaffected(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_nested_2,}
        self.assert_equals('http://example.com/nested-2/nested-nested-2/', t.render(template.Context(var)))

    def test_no_subdomain_second_level_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_nested_2.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_2.slug, 'year': 2011, 'month': 11, 'day': 1}
        self.assert_equals('http://example.com/nested-2/nested-nested-2/2011/11/1/articles/nested-2-article/', t.render(template.Context(var)))
