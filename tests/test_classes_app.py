# pylint: skip-file

import unittest
import sys
import os
from flask import Flask
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from tests.test_class import TestClass # noqa


class Test_Classes_App(TestClass):

    def test_app_is_flask(self):
        self.assertIsInstance(self.app_class.app, Flask)


if __name__ == '__main__':
    unittest.main()
