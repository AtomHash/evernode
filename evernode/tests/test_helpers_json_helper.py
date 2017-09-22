# pylint: skip-file

import unittest
from everflow.helpers import JsonHelper

class Test_test_helper_json_helper(unittest.TestCase):
    def test_json_read_not_found(self):
        self.assertIsNone(JsonHelper.from_file('nofile'))

    def test_json_read_found(self):
        self.assertIsInstance(JsonHelper.from_file('../config.json'), \
            dict)

    def test_json_read_error(self):
        self.assertIsNone(JsonHelper.parse('{{{{'), \
            dict)

if __name__ == '__main__':
    unittest.main()
