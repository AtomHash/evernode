"""
    Mock Controller
"""
from flask import current_app # noqa
from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator # noqa
from evernode.decorators import middleware # noqa
from ..models import HelloWorldModel


class MockController:
    """ Mock Module, Mock Controller """

    @staticmethod
    def hello_world():
        """ Hello World Controller """
        return JsonResponse(200, None, HelloWorldModel())
