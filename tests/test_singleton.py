# -*- coding: utf-8 -*-
import unittest

from nout import singleton


class TestClass(metaclass=singleton.Singleton):
    pass


class SingletonTestCase(unittest.TestCase):
    def test_singleton_classes_are_single(self):
        cls1 = TestClass()
        cls2 = TestClass()

        self.assertEqual(cls1, cls2)
        self.assertEqual(id(cls1), id(cls2))
