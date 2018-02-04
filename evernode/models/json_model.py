""" convert a class to json """

import flask
from datetime import datetime


class JsonModel:
    """ easy class to JSON convertion """

    exclude_list = []

    def json(self):
        """
        using the exclude lists, convert fields to a string.
        """
        default_exclude_list = ['_session', '_sa_instance_state']
        if self.exclude_list is None:
            merged_exclude_list = default_exclude_list
        else:
            merged_exclude_list = default_exclude_list + self.exclude_list
        fields = {}
        for key, item in vars(self).items():
            if key in merged_exclude_list:
                continue
            key = self.camel_case(key)
            new_key = key[0].lower() + key[1:]
            if isinstance(item, datetime):
                app = flask.current_app
                if 'DATETIME' in app.config:
                    if 'DATE_FORMAT' in app.config['DATETIME'] \
                            and 'TIME_FORMAT' in app.config['DATETIME']:
                                item = item.strftime('{0}{1}{2}'.format(
                                    app.config['DATETIME']['DATE_FORMAT'],
                                    app.config['DATETIME']['SEPARATOR'],
                                    app.config['DATETIME']['TIME_FORMAT']))
                else:
                    item = item.strftime('%x %X')
            fields[new_key] = item
        return str(fields)

    def camel_case(self, snake_case):
        """
        convert snake case to camel case
        """
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def __repr__(self):
        """
        exclude some keys, convert all to lowercase snake and string
        """
        return self.json()

    def __str__(self):
        return self.json()
