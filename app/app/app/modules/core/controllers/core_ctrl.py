"""
    Core Controller
"""
from flask import request, current_app # noqa
from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator # noqa
from evernode.decorators import middleware # noqa
from ..models import UserModel # noqa
from evernode.models import PasswordResetModel, JsonModel # noqa
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
        current_app.config['UPLOADS']['EXTENSIONS']


class CoreController:
    """ route controller """

    @staticmethod
    def test():
        """ evernode testing """
        class JJ(JsonModel):
            bob = None

            def __init__(self):
                self.bob = None
                self.time = datetime.now()
                self.time2 = {'ti_me': datetime.now()}
                self.time3 = {'ti_me': ['s', 'f', 1]}
        return JsonResponse(200, None, JJ())

    @staticmethod
    def user_json():
        user = UserModel.get_by_id(0)
        return JsonResponse(200, None, user)

    @staticmethod
    def test_email():
        email = Email(send_as_one=True)
        email.html('hello')
        email.text('hello')
        email.add_address('me@dylanharty.com')
        email.add_cc('dylantechy@gmail.com')
        email.add_file('/srv/logs/uwsgi.log')
        email.send()
        return JsonResponse(200, None, "")

    @staticmethod
    def test_translator():
        trans = Translator()
        return JsonResponse(200, None,
                            trans.trans('welcome.home'))

    @staticmethod
    def test_render():
        """ evernode testing """
        render = Render()
        render.compile('ev/ern/ode.html', folder="emails/user")
        render.templates['evernode.html']
        return JsonResponse(200, None,
                            render.templates['evernode.html'])

    @staticmethod
    def test_security():
        security_functions = dict(
            string="EverNode",
            encrypted=Security.encrypt("EverNode"),
            decrypt=Security.decrypt(Security.encrypt("EverNode")),
        )
        return JsonResponse(200, None, security_functions)

    @staticmethod
    @middleware
    def user_check():
        return JsonResponse(200, None, "is logged in")

    @staticmethod
    def test_form_upload():
        """ evernode testing """
        form = FormData()
        form.add_file("image-file")
        form.add_file("another-file")
        form.parse()
        form.file_save('image-file')
        return JsonResponse(200, None, str(form.files))

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
        return JsonResponse(200, None, form.values['name'])

    def make_user():
        user = UserModel()
        user.firstname = 'Dylan'
        user.lastname = 'Harty'
        user.email = 'dylan.harty@growsafe.com'
        user.set_password('123321')
        user.save()
        return JsonResponse(200, None, user)

    def user_token():
        session = UserAuth(
            UserModel,
            username_error="Please enter a username",
            password_error="Please Enter a password").session()
        if session is None:
            return JsonResponse(401).create()
        return JsonResponse(200, None, session)
