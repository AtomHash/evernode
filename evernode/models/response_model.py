""" a structure for responses """
from ..helpers import JsonHelper


class ResponseModel:
    """ Class for a response a centralized response structure """
    status = 200
    message = "Connection sucessful"
    data = {}

    def __init__(self, status, message, data=None):
        if data is None:
            data = {}
        self.status = status
        self.message = message
        self.data = data

    def __repr__(self):
        return JsonHelper.string(self)

    def __str__(self):
        return self.__repr__()
