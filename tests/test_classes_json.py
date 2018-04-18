# pylint: skip-file

import unittest
import os
import datetime
from json.decoder import JSONDecodeError
from evernode.classes import Json
from evernode.classes import App


class Test_Classes_Json(unittest.TestCase):

    app_class = None

    def setUp(self):
        script_path = os.path.dirname(__file__)
        root_path_file = os.path.join(script_path, 'root_path.txt')
        with open(root_path_file, 'r') as opened_file:
            root_path = opened_file.read().replace('\n', '')
            self.app_class = App(__name__, root_path=(root_path))

    def tearDown(self):
        self.app_class = None

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
