# -*- coding: utf-8 -*-
'''tests.unit_test'''
from __future__ import unicode_literals

import os
import sys
import unittest

from flask import Flask


class TestPage(unittest.TestCase):

    def setUp(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        delogx = os.path.dirname(os.path.dirname(directory))
        sys.path.append(delogx)
        app = Flask(__name__)
        from DelogX import DelogX
        app_path = os.path.join(directory, 'test_app')
        delogx_app = DelogX(app_path, app)
        self.bundle = delogx_app.page_bundle
        self.page1 = self.bundle.get('page1')
        self.page2 = self.bundle.get('page2')
        self.page3 = self.bundle.get('page3')
        self.page4 = self.bundle.get('page4')
        self.page5 = self.bundle.get('page5')

    def test_title(self):
        self.assertEqual(self.page1.title, 'Title')
        self.assertEqual(self.page2.title, 'page2')
        self.assertEqual(self.page3.title, 'Title3')
        self.assertEqual(self.page4.title, 'page4')
        self.assertEqual(self.page5.title, 'Title5')

    def test_url(self):
        self.assertEqual(self.page1.url, 'page1')
        self.assertEqual(self.page2.url, 'page2')
        self.assertEqual(self.page3.url, 'page3')
        self.assertEqual(self.page4.url, 'page4')
        self.assertEqual(self.page5.url, 'page5')

    def test_hidden(self):
        self.assertFalse(self.page1.hidden)
        self.assertFalse(self.page2.hidden)
        self.assertFalse(self.page3.hidden)
        self.assertFalse(self.page4.hidden)
        self.assertTrue(self.page5.hidden)

    def test_sort(self):
        self.assertIsNone(self.page1.sort)
        self.assertEqual(self.page2.sort, 2)
        self.assertEqual(self.page3.sort, 1)
        self.assertIsNone(self.page4.sort)
        self.assertIsNone(self.page5.sort)
        self.assertEqual(self.bundle.get_list()[0].url, 'page3')
        self.assertEqual(self.bundle.get_list()[1].url, 'page2')


class TestPost(unittest.TestCase):

    def setUp(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        delogx = os.path.dirname(os.path.dirname(directory))
        sys.path.append(delogx)
        app = Flask(__name__)
        from DelogX import DelogX
        app_path = os.path.join(directory, 'test_app')
        delogx_app = DelogX(app_path, app)
        self.bundle = delogx_app.post_bundle


class TestConfig(unittest.TestCase):

    def setUp(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        delogx = os.path.dirname(os.path.dirname(directory))
        sys.path.append(delogx)
        filename = os.path.join(directory, 'test_app', 'config.json')
        from DelogX.entity.config import Config
        self.config = Config(filename)

    def test_string(self):
        self.assertEqual(self.config.get('entry_a.key_1_1'), 'String')

    def test_number(self):
        self.assertEqual(self.config.get('entry_a.key_1_2'), 1000)
        self.assertAlmostEqual(self.config.get('entry_a.key_1_3'), -30.75)

    def test_null(self):
        self.assertIsNone(self.config.get('entry_b.key_2_1'))

    def test_bool(self):
        self.assertTrue(self.config.get('entry_b.key_2_2'))
        self.assertFalse(self.config.get('entry_b.key_2_3'))

    def test_list(self):
        equal_list = ["List_1_1", "List_1_2"]
        self.assertListEqual(self.config.get('entry_c.key_3_1'), equal_list)

    def test_nest(self):
        self.assertEqual(self.config.get(
            'entry_c.key_3_2.key_3_2_1.test_1'), 'Test 1')
        self.assertEqual(self.config.get(
            'entry_c.key_3_2.key_3_2_1.key_3_2_2.test_2'), 'Test 2')
        self.assertEqual(self.config.get(
            'entry_c.key_3_2.key_3_2_3.test_3'), 'Test 3')

    def test_let(self):
        self.config.let('test', 'Test A')
        self.config.let('test2.a.b.c', 'Test B')
        self.config.let('entry_a.test', 'Test C')
        self.config.let('entry_a.test2', 'Test D')
        self.assertEqual(self.config.get('test'), 'Test A')
        self.assertEqual(self.config.get('test2.a.b.c'), 'Test B')
        self.assertEqual(self.config.get('entry_a.test'), 'Test C')
        self.assertEqual(self.config.get('entry_a.test2'), 'Test D')

    def test_delete(self):
        self.config.let('test', 'Test A')
        self.config.let('test2.a.b.c', 'Test B')
        self.assertEqual(self.config.get('test'), 'Test A')
        self.assertEqual(self.config.get('test2.a.b.c'), 'Test B')
        value_a = self.config.delete('test')
        value_b = self.config.delete('test2.a.b.c')
        self.assertEqual(value_a, 'Test A')
        self.assertEqual(value_b, 'Test B')
        self.assertIsNone(self.config.get('test'))
        self.assertIsNone(self.config.get('test2.a.b.c'))


if __name__ == '__main__':
    unittest.main()
