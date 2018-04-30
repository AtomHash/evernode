""" convert a class to json """

from ..classes.json import Json


class JsonModel:
    """ easy class to JSON conversion """

    __exclude_list = []
    """ add names in here to exclude attributes in serialization """

    def add(self, name, value):
        """ Add attribute """
        setattr(self, name, value)

    def remove(self, name):
        """ Remove attribute """
        del self.__dict__[name]

    def __json(self):
        """
        Using the exclude lists, convert fields to a string.
        """
        if self.exclude_list is None:
            self.exclude_list = []
        fields = {}
        for key, item in vars(self).items():
            if str(key).startswith('_') or key in self.exclude_list:
                continue
            fields[key] = item
        obj = Json.safe_object(fields)
        return str(obj)
