from django.contrib.sites.models import Site

from djangosanetesting import DatabaseTestCase

from ella.core.models import Category

from ella_category_subdomain.models import CategorySubdomain

class TestModel(DatabaseTestCase):

    def setUp(self):
        super(TestModel, self).setUp()

        site = Site.objects.create(
            domain=u'example.com',
            name=u'main domain',
        )

        self.root = Category.objects.create(
            title=u'Main',
            slug=u'main',
            description=u'Main Category',
            site=site,
        )

        self.first_level_1 = Category.objects.create(
            title=u'First 1',
            slug=u'first_1',
            description=u'First Category',
            site=site,
            tree_parent=self.root,
        )

        self.first_level_2 = Category.objects.create(
            title=u'First 2',
            slug=u'first_2',
            description=u'First Category',
            site=site,
            tree_parent=self.root,
        )

        self.second_level_2 = Category.objects.create(
            title=u'Second 1',
            slug=u'second_1',
            description=u'Second Category',
            site=site,
            tree_parent=self.first_level_1,
        )

    def test_equals(self):
        self.assert_equals(1,1)

    def test_root_category(self):
        cs = CategorySubdomain(category = self.root, subdomain_slug = "root")
        self.assert_va

