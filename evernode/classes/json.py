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

    @staticmethod
    def object_dict(object_class) -> str:
        """ convert a class object dict to json """
        if not isinstance(object_class, dict):
            obj_to_dict = Json.iterate_object(
                dict(object_class.__dict__))
        else:
            obj_to_dict = Json.iterate_object(object_class)
        return system_json.dumps(obj_to_dict, ensure_ascii=False)

    @staticmethod
    def iterate_object(obj) -> dict:
        """ Convert object to flattened object """
        new_obj = {}
        if hasattr(obj, 'items'):
            for key, value in obj.items():
                string_val = ""
                if hasattr(value, '__dict__'):
                    string_val = Json.iterate_object(value)
                else:
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
                new_obj[key] = string_val
        else:
            new_obj = obj
        obj_to_dict = ast.literal_eval(str(new_obj))
        return obj_to_dict

    @staticmethod
    def string(object_class):
        """ alias for object_dict """
        return Json.object_dict(object_class)

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
