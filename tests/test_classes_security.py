# pylint: skip-file

import unittest
import sys
import os
from evernode.classes import Security
from evernode.classes import App
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from tests.test_class import TestClass # noqa


class Test_Classes_Security(TestClass):

    app_class = None

    @classmethod
    def setUpClass(cls):
        script_path = os.path.dirname(__file__)
        root_path_file = os.path.join(script_path, 'root_path.txt')
        with open(root_path_file, 'r') as opened_file:
            root_path = opened_file.read().replace('\n', '')
            cls.app_class = App(__name__, root_path=(root_path))

    @classmethod
    def tearDownClass(cls):
        cls.app_class = None

    def test_generate_key(self):
        self.assertIsInstance(Security.generate_key(), str)

    def test_encrypt(self):
        with self.app_class.app.app_context():
            self.assertIsInstance(Security.encrypt('hello'), str)

    def test_decrypt(self):
        with self.app_class.app.app_context():
            self.assertIsInstance(
                Security.decrypt(Security.encrypt('hello')), str)


if __name__ == '__main__':
    unittest.main()
