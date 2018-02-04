"""
    Core Controller
"""

from datetime import datetime
from flask import request # noqa
from evernode.classes import JsonResponse, Render, Security, Email, User # noqa
from evernode.models import JsonModel
from evernode.decorators import load_middleware # noqa
from ..models import UserModel # noqa
from evernode.models import PasswordResetModel # noqa


class TestJsonModel(JsonModel):
    date = ""


class CoreController:
    """ route controller """

    @staticmethod
    def test():
        """ evernode testing """
        test = TestJsonModel()
        test.date = datetime.now()
        return JsonResponse(200, None, test).create()
