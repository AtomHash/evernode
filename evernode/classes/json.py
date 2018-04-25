"""
    Help to do easy JSON modeling for db models and other classes
"""

import io
import datetime
import json as system_json
from collections import namedtuple
from flask import current_app


class Json():
    """ help break down and construct json objects """

    def __init__(self, value):
        self.value = value

    @staticmethod
    def string(value) -> str:
        """ string dict/object/value to JSON """
        return system_json.dumps(Json(value).safe_object(), ensure_ascii=False)

    @staticmethod
    def parse(string, is_file=False, obj=False):
        """ Convert a JSON string to dict/object """
        try:
            if obj is False:
                if is_file:
                    return system_json.load(string)
                return system_json.loads(string, encoding='utf8')
            else:
                if is_file:
                    return system_json.load(
                        string,
                        object_hook=lambda d: namedtuple('j', d.keys())
                        (*d.values()), ensure_ascii=False, encoding='utf8')
                return system_json.loads(
                    string,
                    object_hook=lambda d: namedtuple('j', d.keys())
                    (*d.values()), encoding='utf8')
        except (Exception, BaseException) as error:
            try:
                if current_app.config['DEBUG']:
                    raise error
            except RuntimeError as flask_error:
                raise error
            return None

    @staticmethod
    def from_file(file_path) -> dict:
        """ Load JSON file """
        with io.open(file_path, 'r', encoding='utf-8') as json_stream:
            return Json.parse(json_stream, True)

    def safe_object(self) -> dict:
        """ Create an object ready for JSON serialization """
        return self.__iterate_value(self.value)

    def safe_values(self, value):
        """ Parse non-string values that will not serialize """
        # TODO: override-able?
        string_val = ""
        if isinstance(value, datetime.date):
            try:
                string_val = value.strftime('{0}{1}{2}'.format(
                    current_app.config['DATETIME']['DATE_FORMAT'],
                    current_app.config['DATETIME']['SEPARATOR'],
                    current_app.config['DATETIME']['TIME_FORMAT']))
            except RuntimeError as error:
                string_val = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, bytes):
            string_val = value.decode('utf-8')
        else:
            string_val = value
        return string_val

    def camel_case(self, snake_case):
        """ Convert snake case to camel case """
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def __find_object_children(self, obj) -> dict:
        """ Convert object to flattened object """
        if hasattr(obj, 'items'):
            return self.__construct_object(obj)
        elif isinstance(obj, (list, tuple, set)):
            return self.__construct_list(obj)
        else:
            return self.__construct_object(vars(obj))
        return None

    def __construct_list(self, list_value):
        """ Loop list/set/tuple and parse values """
        array = []
        for value in list_value:
            array.append(self.__iterate_value(value))
        return array

    def __construct_object(self, obj):
        """ Loop dict/class object and parse values """
        new_obj = {}
        for key, value in obj.items():
            new_obj[self.camel_case(key)] = self.__iterate_value(value)
        return new_obj

    def __iterate_value(self, value):
        """ Return value for JSON serialization """
        if hasattr(value, '__dict__') or isinstance(value, dict):
            return self.__find_object_children(value)  # go through dict/class
        elif isinstance(value, (list, tuple, set)):
            return self.__construct_list(value)  # go through list
        return self.safe_values(value)  # return parse value only
