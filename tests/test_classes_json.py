# pylint: skip-file

import unittest
import sys
import os
import datetime
from json.decoder import JSONDecodeError
from evernode.classes import Json
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from tests.test_class import TestClass # noqa


class Test_Classes_Json(TestClass):

    def test_json_read_not_found(self):
        self.assertRaises(FileNotFoundError, Json.from_file, 'nofile')

    def test_json_read_found(self):
        self.assertIsInstance(
            Json.from_file(self.app_class.app.config['CONFIG_PATH']), dict)

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
