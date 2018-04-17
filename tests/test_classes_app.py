# pylint: skip-file
import unittest
from evernode.classes import App
from flask import Flask


class Test_Classes_App(unittest.TestCase):
    def test_app_is_flask(self):
        app_class = App(__name__)
        self.assertIsInstance(app_class.app, Flask)


if __name__ == '__main__':
    unittest.main()
