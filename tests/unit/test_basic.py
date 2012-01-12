# -*- coding: utf-8 -*-
from django.test import TestCase
from nose import tools

class TestBasicAsserts(TestCase):
    
    def test_assert_equals(self):
        tools.assert_equals(1, 1)