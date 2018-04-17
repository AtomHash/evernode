# pylint: skip-file

import unittest
from evernode.classes import Security
from evernode.classes import App


class Test_Classes_Security(unittest.TestCase):

    app_class = None

    def setUp(self):
        self.app_class = App(
            __name__,
            root_path=('C:\\Users\\dylan.harty\\'
                       'Desktop\\evernode\\app\\app\\app'))

    def tearDown(self):
        self.app_class = None

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
