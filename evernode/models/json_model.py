""" convert a class to json """

from datetime import datetime

class JsonModel(object):
    """ easy class to JSON convertion """
    def __repr__(self):
        #exclude some keys, convert all to lowercase snake and string
        #dictionary
        return self.json()
        
    def json(self, exclude_list=None):
        default_exclude_list = ['_session','_sa_instance_state']
        if exclude_list is None:
             merged_exclude_list = default_exclude_list
        else:
             merged_exclude_list = default_exclude_list + exclude_list
        fields = {}
        for key, item in vars(self).items():
            if key in merged_exclude_list:
                continue
            key = self.__camel_case__(key)
            new_key = key[0].lower() + key[1:]
            if isinstance(item, datetime):
                 item = item.strftime('%x %X')
            fields[new_key] = item
        return str(fields)

    def __camel_case__(self, snake_case):
        #convert snake case to camel case for JSON output
        components = snake_case.split('_')
        return components[0] + "".join(x.title() for x in components[1:])

    def __str__(self, exclude_list=None):
        return self.__repr__(exclude_list)
