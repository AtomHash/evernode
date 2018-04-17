# pylint: skip-file
import unittest
from evernode.classes import App
from flask import Flask


class Test_Classes_App(unittest.TestCase):

    app_class = None

    def setUp(self):
        with open('root_path.txt', 'r') as opened_file:
            root_path = opened_file.read().replace('\n', '')
            self.app_class = App(__name__, root_path=(root_path))

    def tearDown(self):
        self.app_class = None

    def test_app_is_flask(self):
        self.assertIsInstance(self.app_class.app, Flask)


if __name__ == '__main__':
    unittest.main()
