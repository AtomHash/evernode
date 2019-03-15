"""
    Response wrapper for HTTP request
"""

from flask import Response
from .translator import Translator
from ..models.response_model import ResponseModel


class BaseResponse:
    """ Base class for a HTTP response """
    __mimetype__ = "text/plain; charset=utf-8"
    environ = None
    response_model = ResponseModel
    response = Response

    def __init__(self, status_code, message=None,
                 data=None, environ=None):
        self.environ = environ
        self.response_model = ResponseModel(
            status_code, message, data=data)

    def __call__(self, environ=None, start_response=None) -> Response:
        """ Send response """
        start_response(self.status(), [('Content-Type', self.mimetype())])
        return [self.content()]

    def status(self, status_code=None):
        """ Set status or Get Status """
        if status_code is not None:
            self.response_model.status = status_code
        # return string for response support
        return str(self.response_model.status)

    def message(self, message=None):
        """ Set response message """
        if message is not None:
            self.response_model.message = message
        return self.response_model.message

    def data(self, data=None):
        """ Set response data """
        if data is not None:
            self.response_model.data = data
        return self.response_model.data

    def content(self) -> str:
        """ Get full content of response """
        return str(self.response_model)

    def mimetype(self) -> str:
        """ Return private minetype """
        return self.__mimetype__

    def quick_response(self, status_code):
        """ Quickly construct response using a status code """
        translator = Translator(environ=self.environ)
        if status_code == 404:
            self.status(404)
            self.message(translator.trans('http_messages.404'))
        elif status_code == 401:
            self.status(401)
            self.message(translator.trans('http_messages.401'))
        elif status_code == 400:
            self.status(400)
            self.message(translator.trans('http_messages.400'))
        elif status_code == 200:
            self.status(200)
            self.message(translator.trans('http_messages.200'))
