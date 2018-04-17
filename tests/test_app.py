# pylint: skip-file
import unittest
from evernode.classes import App
from flask import Flask


class Test_test_app(unittest.TestCase):
    def test_app_is_flask(self):
        app_class = App(__name__, root_path=('C:\\Users\\dylan.harty\\Desktop'
                                             '\\evernode\\app\\app\\app'))
        self.assertIsInstance(app_class.app, Flask)


if __name__ == '__main__':
    unittest.main()
