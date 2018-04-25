""" convert a class to json """

from ..classes.json import Json


class JsonModel:
    """ easy class to JSON conversion """

    exclude_list = []
    """ add names in here to exclude attributes in serialization """

    def add(self, name, value):
        """ add attribute """
        setattr(self, name, value)

    def remove(self, name):
        """ remove attribute """
        del self.__dict__[name]

    def __json(self):
        """
        using the exclude lists, convert fields to a string.
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

    def __repr__(self):
        """
        exclude some keys, convert all to lowercase snake and string
        """
        return self.__json()

    def __str__(self):
        return self.__json()
