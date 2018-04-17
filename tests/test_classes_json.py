# pylint: skip-file

import unittest
import datetime
from json.decoder import JSONDecodeError
from evernode.classes import Json


class Test_test_json_filenotfound(unittest.TestCase):
    def test_json_read_not_found(self):
        self.assertRaises(FileNotFoundError, Json.from_file, 'nofile')

    def test_json_read_found(self):
        self.assertIsInstance(
            Json.from_file('../app/app/app/config.json'), dict)

    def test_json_string_parse(self):
        self.assertIsInstance(
            Json.parse('{"first": "hello"}'), dict)

    def test_json_object_to_string(self):
        self.assertIsInstance(
            Json.string({"second": "message"}), str)

    def test_parse_string_to_json_object_to_string(self):
        string = '{"third": "hello"}'
        dict = Json.parse(string)
        string_two = Json.string(dict)
        self.assertIsInstance(string_two, str)

    def test_json_handle_date(self):
        self.assertIsInstance(
            Json.string({"datetime": datetime.datetime.now()}), str)

    def test_json_read_error(self):
        self.assertRaises(JSONDecodeError, Json.parse, '{{{{{}')


if __name__ == '__main__':
    unittest.main()
