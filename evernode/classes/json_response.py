"""
    Easy JSON HTTP responses
"""
from .base_response import BaseResponse


class JsonResponse(BaseResponse):
    """ JsonResponse is a wrapper for BaseResponse """
    __mimetype__ = "application/json; charset=utf-8"

    def __init__(self, status_code=200, message=None, data=None, environ=None):
        super().__init__(status_code, message=message,
                         data=data, environ=environ)
        if message is None:
            self.quick_response(status_code)
