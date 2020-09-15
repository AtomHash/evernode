"""
    Help to do easy JSON modeling for db models and other classes
"""
import types
import decimal
import io
import datetime
import ujson as system_json
from collections import namedtuple
from sqlalchemy import inspect
from sqlalchemy import orm
from flask import current_app


class Json():
    """ help break down and construct json objects """

    __exclude_list = []

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
                raise flask_error
            return None

    @staticmethod
    def from_file(file_path) -> dict:
        """ Load JSON file """
        with io.open(file_path, 'r', encoding='utf-8') as json_stream:
            return Json.parse(json_stream, True)

    @staticmethod
    def save_file(file_path, data):
        with open(file_path, 'w') as json_file:
            system_json.dump(
                data,
                json_file,
                ensure_ascii=False,
                indent=4)

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
            except RuntimeError:
                string_val = value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, bytes):
            string_val = value.decode('utf-8')
        elif isinstance(value, decimal.Decimal):
            string_val = float(value)
        else:
            string_val = value
        return string_val

    def camel_case(self, snake_case):
        """ Convert snake case to camel case """
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def __find_object_children(self, obj) -> dict:
        """ Convert object to flattened object """
        if hasattr(obj, 'items') and \
                isinstance(obj.items, types.BuiltinFunctionType):
            return self.__construct_object(obj)
        elif isinstance(obj, (list, tuple, set)):
            return self.__construct_list(obj)
        else:
            exclude_list = []
            if hasattr(obj, '_sa_instance_state'):
                # load only deferred objects
                if len(orm.attributes.instance_state(obj).unloaded) > 0:
                    mapper = inspect(obj)
                    for column in mapper.attrs:
                        column.key
                        column.value
            if hasattr(obj, 'json_exclude_list'):
                # do not serialize any values in this list
                exclude_list = obj.json_exclude_list
            return self.__construct_object(vars(obj), exclude_list)
        return None

    def __construct_list(self, list_value):
        """ Loop list/set/tuple and parse values """
        array = []
        for value in list_value:
            array.append(self.__iterate_value(value))
        return array

    def __construct_object(self, obj, exclude_list=[]):
        """ Loop dict/class object and parse values """
        new_obj = {}
        for key, value in obj.items():
            if str(key).startswith('_') or \
                    key is 'json_exclude_list' or key in exclude_list:
                continue
            new_obj[self.camel_case(key)] = self.__iterate_value(value)
        return new_obj

    def __iterate_value(self, value):
        """ Return value for JSON serialization """
        if hasattr(value, '__dict__') or isinstance(value, dict):
            return self.__find_object_children(value)  # go through dict/class
        elif isinstance(value, (list, tuple, set)):
            return self.__construct_list(value)  # go through list
        return self.safe_values(value)  # return parse value only
