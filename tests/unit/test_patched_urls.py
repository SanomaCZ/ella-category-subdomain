from django.conf import settings
from django import template

from django.test import TestCase
from nose import tools


from unit.helpers import create_categories_site

class TestAbsoluteURLsCase(TestCase):

    def setUp(self):
        super(TestAbsoluteURLsCase, self).setUp()
        create_categories_site(self)

    # get_absolute_url tests

    def test_root_category_get_absolute_urls_works_unaffected(self):
        tools.assert_equals('http://example.com/', self.category_root.get_absolute_url())

    def test_category_get_absolute_url_is_patched(self):
        tools.assert_equals('http://nested-one.example.com/', self.category_nested_1.get_absolute_url())

    def test_category_get_absolute_url_works_for_second_level_categories(self):
        tools.assert_equals('http://nested-one.example.com/nested-nested-1/', self.category_nested_nested_1.get_absolute_url())

    def test_no_subdomain_category_get_absolute_url_works_unaffected(self):
        tools.assert_equals('http://example.com/nested-2/', self.category_nested_2.get_absolute_url())

    def test_no_subdomain_second_level_category_get_absolute_url_works_unaffected(self):
        tools.assert_equals('http://example.com/nested-2/nested-nested-2/', self.category_nested_nested_2.get_absolute_url())

    # pathed reverse tests

    def test_root_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://example.com/', reverse('category_detail', args=('/',)))
        
    def test_category_reverse_is_patched(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-one.example.com/', reverse('category_detail', args=(self.category_nested_1.tree_path,)))

    def test_category_reverse_works_for_second_level_categories(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-one.example.com/nested-nested-1/', reverse('category_detail', args=(self.category_nested_nested_1.tree_path,)))

    def test_no_subdomain_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://example.com/nested-2/', reverse('category_detail', args=(self.category_nested_2.tree_path,)))

    def test_no_subdomain_second_level_category_reverse_works_unaffected(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://example.com/nested-2/nested-nested-2/', reverse('category_detail', args=(self.category_nested_nested_2.tree_path,)))

    # url tag tests

    def test_root_category_url_tag_work_unaffected(self):
        t = template.Template('{% url category_detail category %}')

        var = {'category' : '/',}
        tools.assert_equals('http://example.com/', t.render(template.Context(var)))

    def test_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_1,}
        tools.assert_equals('http://nested-one.example.com/', t.render(template.Context(var)))

    def test_url_tag_works_for_second_level_categories(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_nested_1,}
        tools.assert_equals('http://nested-one.example.com/nested-nested-1/', t.render(template.Context(var)))

    def test_no_subdomain_category_url_tag_works_unaffected(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_2,}
        tools.assert_equals('http://example.com/nested-2/', t.render(template.Context(var)))

    def test_no_subdomain_second_level_category_url_tag_works_unaffected(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.category_nested_nested_2,}
        tools.assert_equals('http://example.com/nested-2/nested-nested-2/', t.render(template.Context(var)))

    # article tests

    def test_root_article_get_absolute_urls_works_unaffected(self):
        tools.assert_equals('http://example.com/2011/9/1/articles/root-article/', self.article_root.get_absolute_url())

    def test_first_level_article_get_absolute_url_is_patched(self):
        tools.assert_equals('http://nested-one.example.com/2011/9/1/articles/nested-1-article/', self.article_nested_1.get_absolute_url())

    def test_root_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : '/', 'content_type': 'articles', 'slug': self.placement_root.slug, 'year': 2011, 'month': 11, 'day': 1}
        tools.assert_equals('http://example.com/2011/11/1/articles/root-article/', t.render(template.Context(var)))

    def test_url_tag_works_first_level_article(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_1.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_1.slug, 'year': 2011, 'month': 11, 'day': 1}
        tools.assert_equals('http://nested-one.example.com/2011/11/1/articles/nested-1-article/', t.render(template.Context(var)))

    def test_url_tag_works_second_level_article(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_nested_1.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_nested_1.slug, 'year': 2011, 'month': 11, 'day': 1}
        tools.assert_equals('http://nested-one.example.com/nested-nested-1/2011/11/1/articles/nested-nested-1-article/', t.render(template.Context(var)))

    def test_no_subdomain_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_2.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_2.slug, 'year': 2011, 'month': 11, 'day': 1}
        tools.assert_equals('http://example.com/nested-2/2011/11/1/articles/nested-2-article/', t.render(template.Context(var)))

    def test_no_subdomain_second_level_article_url_tag_work_unaffected(self):
        t = template.Template('{% url object_detail category year month day content_type slug %}')

        var = {'category' : self.category_nested_nested_2.tree_path, 'content_type': 'articles', 'slug': self.placement_nested_2.slug, 'year': 2011, 'month': 11, 'day': 1}
        tools.assert_equals('http://example.com/nested-2/nested-nested-2/2011/11/1/articles/nested-2-article/', t.render(template.Context(var)))


    # site 2 tests
class TestAbsoluteURLsSite2Case(TestCase):

    def setUp(self):
        super(TestAbsoluteURLsSite2Case, self).setUp()
        create_categories_site(self)
        settings.SITE_ID = self.site_2_id

    def test_site_2_root_category_get_absolute_url_works(self):
        tools.assert_equals('http://example1.com/', self.site_2_root.get_absolute_url())

    def test_site_2_category_get_absolute_url_is_patched(self):
        tools.assert_equals('http://nested-one.example1.com/', self.site_2_nested_1.get_absolute_url())

    def test_category_reverse_is_patched(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-one.example1.com/', reverse('category_detail', args=(self.site_2_nested_1.tree_path,)))

    def test_site_2_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.site_2_nested_1,}
        tools.assert_equals('http://nested-one.example1.com/', t.render(template.Context(var)))


class TestAbsoluteURLsSite3Case(TestCase):

    def setUp(self):
        super(TestAbsoluteURLsSite3Case, self).setUp()
        create_categories_site(self)
        settings.SITE_ID = self.site_3_id

    def test_site_3_root_category_get_absolute_url_works(self):
        tools.assert_equals('http://www.example.com/', self.site_3_root.get_absolute_url())

    def test_site_3_category_get_absolute_url_is_patched(self):
        tools.assert_equals('http://nested-one.example.com/', self.site_3_nested_1.get_absolute_url())

    def test_category_reverse_is_patched(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-one.example.com/', reverse('category_detail', args=(self.site_3_nested_1.tree_path,)))

    def test_site_3_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.site_3_nested_1,}
        tools.assert_equals('http://nested-one.example.com/', t.render(template.Context(var)))


class TestAbsoluteURLsSite4Case(TestCase):

    def setUp(self):
        super(TestAbsoluteURLsSite4Case, self).setUp()
        create_categories_site(self)
        settings.SITE_ID = self.site_4_id

    def test_site_4_root_category_get_absolute_url_works(self):
        tools.assert_equals('http://www.example.co.uk/', self.site_4_root.get_absolute_url())

    def test_site_4_category_get_absolute_url_is_patched(self):
        tools.assert_equals('http://nested-one.example.co.uk/', self.site_4_nested_1.get_absolute_url())

    def test_category_reverse_is_patched(self):
        from django.core.urlresolvers import reverse
        tools.assert_equals('http://nested-one.example.co.uk/', reverse('category_detail', args=(self.site_4_nested_1.tree_path,)))

    def test_site_4_url_tag_is_patched(self):
        t = template.Template('{% url category_detail category.tree_path %}')

        var = {'category' : self.site_4_nested_1,}
        tools.assert_equals('http://nested-one.example.co.uk/', t.render(template.Context(var)))
