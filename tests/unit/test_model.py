from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from djangosanetesting import DatabaseTestCase

from ella.core.models import Category
from ella_category_subdomain.models import CategorySubdomain

from unit.helpers import create_categories

class TestModelCase(DatabaseTestCase):

    def setUp(self):
        super(TestModelCase, self).setUp()
        create_categories(self)

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

