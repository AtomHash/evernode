"""
    Easy JSON HTTP responses
"""
from flask import current_app, Response
from .base_response import BaseResponse


class JsonResponse(BaseResponse):
    """ JsonResponse is a wrapper for BaseResponse """
    __mimetype__ = "application/json; charset=utf-8"

    def __init__(self, status_code=200, message=None, data=None, environ=None):
        super().__init__(status_code, message=message,
                         data=data, environ=environ)
        if message is None or data is None:
            self.quick_response(status_code)

    def create(self) -> Response:
        """ Construct response """
        json_content = str(self.response_model)
        self.response = current_app.response_class(
            json_content,
            mimetype=self.__mimetype__
        )
        self.response.status = self.status()
        return self.response
