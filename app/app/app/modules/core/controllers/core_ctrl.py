"""
    Core Controller
"""
from flask import request, current_app # noqa
from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator # noqa
from evernode.decorators import middleware # noqa
from ..models import UserModel # noqa
from evernode.models import PasswordResetModel # noqa


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
        current_app.config['UPLOADS']['EXTENSIONS']


class CoreController:
    """ route controller """

    @staticmethod
    def test():
        """ evernode testing """
        return JsonResponse(200, None, "").create()

    @staticmethod
    def test_translator():
        trans = Translator()
        return JsonResponse(200, None,
                            trans.trans('welcome.home')).create()

    @staticmethod
    def test_render():
        """ evernode testing """
        render = Render()
        render.compile('ev/ern/ode.html', folder="emails/user")
        render.templates['evernode.html']
        return JsonResponse(200, None,
                            render.templates['evernode.html']).create()

    @staticmethod
    def test_security():
        security_functions = dict(
            string="EverNode",
            encrypted=Security.encrypt("EverNode"),
            decrypt=Security.decrypt(Security.encrypt("EverNode")),
        )
        return JsonResponse(200, None, security_functions).create()

    @staticmethod
    @middleware
    def user_check():
        return JsonResponse(200, None, "is logged in").create()

    @staticmethod
    def test_form_upload():
        """ evernode testing """
        form = FormData()
        form.add_file("image-file")
        form.add_file("another-file")
        form.parse()
        form.file_save('image-file')
        return JsonResponse(200, None, str(form.files)).create()

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

    def user_token():
        session = UserAuth(
            UserModel,
            username_error="Please enter a username",
            password_error="Please Enter a password").session()
        if session is None:
            return JsonResponse(401).create()
        return JsonResponse(200, None, session).create()
