# pylint: skip-file

import unittest
import sys
import os
from evernode.classes import Security
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from tests.test_class import TestClass # noqa


class Test_Classes_Security(TestClass):

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
