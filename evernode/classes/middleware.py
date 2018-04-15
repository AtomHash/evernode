"""
    Middleware to help handle route.py conditions
"""
from flask import current_app, Flask, Response
from .json_response import JsonResponse


class Middleware:
    """ Provides useful defaults for creating fast middleware """
    status = False
    response = Response
    app = Flask

    def __init__(self):
        self.app = current_app
        self.status = self.condition()
        if self.status is False:
            self.create_response()

    def condition(self) -> bool:
        """ A condition to validate or invalidate a request """
        return False

    def create_response(self):
        """ Default response for if condition is false(invalid) """
        self.response = JsonResponse(401)
