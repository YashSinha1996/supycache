#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import supycache

class TestDictCache(unittest.TestCase):
    """ Test the DictCache backend
    """

    def setUp(self):
        from supycache.backends import DictCache
        self.cache = DictCache()
        supycache.set_default_backend(self.cache)

    def tearDown(self):
        self.cache.clear()

    def test_init(self):
        """Testing DictCache constructor"""
        self.assertTrue(hasattr(self.cache, 'set'))
        self.assertTrue(hasattr(self.cache, 'get'))
        self.assertTrue(hasattr(self.cache, 'clear'))

    def test_methods(self):
        """Testing DictCache methods"""
        self.cache.set('key', 'value')
        self.assertTrue(self.cache.get('key') == 'value')
        self.assertTrue(bool(self.cache.get('non-existent')) == False)
        self.assertTrue(self.cache.clear() == None)
        self.assertTrue(len(self.cache._data) == 0)


class TestExpiringDictCache(unittest.TestCase):
    """ Test the ExpiringDictCache backend
    """

    def setUp(self):
        from supycache.backends import ExpiringDictCache
        self.cache = ExpiringDictCache()
        supycache.set_default_backend(self.cache)

    def tearDown(self):
        self.cache.clear()

    def test_init(self):
        """Testing ExpiringDictCache constructor"""
        self.assertTrue(self.cache._data['DoesNotExist'] == ('', 0))

    def test_get_without_ignoring_errors(self):
        """Testing ExpiringDictCache get() method"""

        @supycache.supycache(cache_key='simple_key', ignore_errors=False, max_age=10)
        def simple_function():
            return 'simple_value'

        with self.assertRaises(KeyError) as context:
            simple_function()


    def test_get_with_ignoring_errors(self):
        """Testing ExpiringDictCache get() method"""

        @supycache.supycache(cache_key='simple_key', max_age=10)
        def simple_function():
            return 'simple_value'

        self.assertTrue(simple_function() == 'simple_value')
        self.assertTrue(self.cache.get('simple_key') == 'simple_value')
        self.assertTrue(self.cache._data['simple_key'][1] != 0)
