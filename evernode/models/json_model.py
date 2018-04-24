""" convert a class to json """

import flask
from datetime import datetime
from ..classes.json import Json
import ast


class JsonModel:
    """ easy class to JSON conversion """

    exclude_list = []

    def json(self):
        """
        using the exclude lists, convert fields to a string.
        """
        if self.exclude_list is None:
            self.exclude_list = []
        fields = {}
        for key, item in vars(self).items():
            if str(key).startswith('_') or key in self.exclude_list:
                continue
            key = self.camel_case(key)
            new_key = key[0].lower() + key[1:]
            item = item
            fields[new_key] = item
        obj = Json.string(fields, to_json=False)
        print('----4454---')
        print(str(obj))
        return str(fields)

    def camel_case(self, snake_case):
        """
        convert snake case to camel case
        """
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def add(self, name, value):
        setattr(self, name, value)

    def remove(self, name):
        del self.__dict__[name]

    def __repr__(self):
        """
        exclude some keys, convert all to lowercase snake and string
        """
        return self.json()

    def __str__(self):
        return self.json()
