"""
    Help to do easy JSON modeling for db models and other classes
"""

import ast
import json as system_json
from collections import namedtuple


class JsonHelper():
    """ help break down and construct json objects """

    @staticmethod
    def object_dict(object_class) -> str:
        """ convert a class object dict to json """
        obj_to_dict = JsonHelper.iterate_object(dict(object_class.__dict__))
        return system_json.dumps(obj_to_dict, ensure_ascii=False)

    @staticmethod
    def iterate_object(obj) -> dict:
        """ Convert object to flattened object """
        new_obj = {}
        if hasattr(obj, 'items'):
            for key, value in obj.items():
                string_val = ""
                if hasattr(value, '__dict__'):
                    string_val = JsonHelper.iterate_object(value)
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
        return JsonHelper.object_dict(object_class)

    @staticmethod
    def parse(string, is_file=False, obj=False):
        """ convert a json string to dict or object """
        try:
            if obj is False:
                if is_file:
                    return system_json.load(string)
                return system_json.loads(string)
            else:
                if is_file:
                    return system_json.load(
                        string,
                        object_hook=lambda d: namedtuple('j', d.keys())
                        (*d.values()))
                return system_json.loads(
                    string,
                    object_hook=lambda d: namedtuple('j', d.keys())
                    (*d.values()))
        except ValueError:
            return None

    @staticmethod
    def from_file(file_path) -> dict:
        """ load small json file """
        with open(file_path, 'r') as json_stream:
            return JsonHelper.parse(json_stream, True)
