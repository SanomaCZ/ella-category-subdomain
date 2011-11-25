from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djangosanetesting import DatabaseTestCase

from ella.core.models import Category
from ella_category_subdomain.models import CategorySubdomain

from helpers import create_categories

class TestModelCase(DatabaseTestCase):

    def setUp(self):
        super(TestModel, self).setUp()
        create_categories(self)

    def test_root_category(self):
        cs = CategorySubdomain(category = self.root_category, subdomain_slug = self.root_category.slug)
        self.assert_raises(ValidationError, cs.clean)

    def test_first_nested_category(self):
        cs = CategorySubdomain(category = self.category_nested_1, subdomain_slug = self.category_nested_1.slug)
        self.assert_is_none(cs.clean())

    def test_second_nested_category(self):
        cs = CategorySubdomain(category = self.category_nested_nested_2, subdomain_slug = self.category_nested_nested_2.slug)
        self.assert_raises(ValidationError, cs.clean)

    def test_single_reference_to_category(self):
        cs1 = CategorySubdomain(category = self.category_nested_1, subdomain_slug = self.category_nested_1.slug)
        cs1.save()
        cs2 = CategorySubdomain(category = self.category_nested_1, subdomain_slug = self.category_nested_1.slug)
        self.assert_raises(IntegrityError, cs2.save)

