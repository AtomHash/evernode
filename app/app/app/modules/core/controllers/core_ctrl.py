"""
    Core Controller
"""
from flask import request # noqa
from evernode.classes import JsonResponse, Render, Security, Email, User, FormData # noqa
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
        key = Security.generate_key()
        return JsonResponse(200, None, key).create()

    @staticmethod
    def generate_key():
        """ evernode testing """
        key = Security.generate_key()
        return JsonResponse(200, None, key).create()

    @staticmethod
    def test_form():
        """ evernode testing """
        form = FormData()
        form.add_field('name', error="you need a name", required=True)
        form.parse()
        return JsonResponse(200, None, form.values['name']).create()

    def make_user():
        user = UserModel()
        user.firstname = 'Dylan'
        user.lastname = 'Harty'
        user.email = 'dylan.harty@growsafe.com'
        user.set_password('123321')
        user.save()
        return JsonResponse(200, None, user).create()

    def create_session_jwt():
        signin = User(UserModel).signin()
        if signin is None:
            return JsonResponse(401).create()
        return JsonResponse(200, None, signin).create()
