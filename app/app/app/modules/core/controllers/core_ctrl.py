"""
    Core Controller
"""

from flask import request # noqa
from evernode.classes import JsonResponse, Render, Security, Email, User # noqa
from evernode.decorators import load_middleware # noqa
from ..models import UserModel # noqa
from evernode.models import PasswordResetModel # noqa


class CoreController:
    """ route controller """

    @staticmethod
    def test():
        """ evernode testing """
        return JsonResponse(200, None, {}).create()
