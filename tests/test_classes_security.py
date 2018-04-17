# pylint: skip-file

import unittest
from evernode.classes import Security
from evernode.classes import App


class Test_Classes_Security(unittest.TestCase):

    app_class = None

    def setUp(self):
        with open('root_path.txt', 'r') as opened_file:
            root_path = opened_file.read().replace('\n', '')
            self.app_class = App(__name__, root_path=(root_path))

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
