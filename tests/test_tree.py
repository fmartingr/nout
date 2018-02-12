# -*- coding: utf-8 -*-
import os
import os.path
import unittest

from nout.tree import Tree
from nout.conf import config


class TreeTestCase(unittest.TestCase):
    path = os.path.join(os.getcwd(), 'tests', 'notes')

    def create_path(self, path):
        return os.path.join(self.path, path)

    @classmethod
    def setUpClass(cls):
        config.path = cls.path

    def tearDown(self):
        # Destroy tree singleton
        del Tree.instance
        Tree.instance = None

    def test_tree_enable_database_true_and_default(self):
        tree = Tree()
        self.assertTrue(hasattr(tree, 'database'))

    def test_tree_enable_database_false(self):
        tree = Tree(enable_database=False)
        self.assertFalse(hasattr(tree, 'database'))

    def test_tree_fully_reads_the_tree(self):
        tree = Tree(enable_database=False)
        print(config.path)
        tree.read()
        print(tree.files)
        self.assertEqual(len(tree.files.keys()), 2)

    def test_ignored_patterns(self):
        tree = Tree()
        self.assertIn('.*', tree.ignore_patterns)  # Mandatory
        self.assertTrue(tree.matches_ignore_patterns('.hidden_file'))

    def test_add_file_ok(self):
        tree = Tree(enable_database=False)
        tree.add_file(self.create_path('note1.md'))
        self.assertIn('/note1.md', tree.files.keys())

    def test_add_file_ko(self):
        tree = Tree(enable_database=False)
        with self.assertRaises(FileNotFoundError):
            tree.add_file(self.create_path('note_unexistant.md'))

    def test_remove_file_ok(self):
        tree = Tree(enable_database=False)
        tree.read()
        tree.delete_file(self.create_path('/note1.md'))
        self.assertNotIn('/note1.md', tree.files.keys())

    def test_remove_file_ko(self):
        # TDB
        pass
