"""
    Help to do easy JSON modeling for db models and other classes
"""

import ast
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
    def string(value, to_json=True):
        """ alias for object_dict """
        json = Json(value)
        if to_json:
            return system_json.dumps(json.safe_object(), ensure_ascii=False)
        return json.safe_object()

    @staticmethod
    def parse(string, is_file=False, obj=False):
        """ convert a json string to dict or object """
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
        """ load small json file """
        with io.open(file_path, 'r', encoding='utf-8') as json_stream:
            return Json.parse(json_stream, True)

    def safe_object(self):
        if isinstance(self.value, datetime.date):
            return self.safe_datetime(self.value)
        elif isinstance(self.value, dict) or hasattr(self.value, '__dict__'):
            return self.__iterate_object(self.value)
        else:
            return self.value

    def __iterate_object(self, obj) -> dict:
        """ Convert object to flattened object """
        if hasattr(obj, 'items'):
            return self.construct_object(obj)
        else:
            return self.construct_object(vars(obj))
        return None

    def construct_object(self, obj):
        new_obj = {}
        for key, value in obj.items():
            string_val = ""
            if hasattr(value, '__dict__') or isinstance(value, dict):
                string_val = self.__iterate_object(value)
            else:
                string_val = self.safe_values(value)
            new_obj[self.camel_case(key)] = string_val
        return new_obj

    def safe_values(self, value):
        string_val = ""
        if isinstance(value, datetime.date):
            string_val = self.safe_datetime(value)
        elif isinstance(value, bytes):
            string_val = value.decode('utf-8')
        else:
            string_val = value
        return string_val

    def safe_datetime(self, value):
        string_val = ""
        try:
            string_val = value.strftime('{0}{1}{2}'.format(
                current_app.config['DATETIME']['DATE_FORMAT'],
                current_app.config['DATETIME']['SEPARATOR'],
                current_app.config['DATETIME']['TIME_FORMAT']))
        except RuntimeError as error:
            string_val = value.strftime('%Y-%m-%d %H:%M:%S')
        return string_val

    def camel_case(self, snake_case):
        """
        convert snake case to camel case
        """
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])
