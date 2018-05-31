"""
    Core Controller
"""
from flask import request, current_app # noqa
from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator, JWT, Paginate, Fail2Ban # noqa
from evernode.decorators import middleware # noqa
from evernode.models import PasswordResetModel, JsonModel, BaseUserModel # noqa
from datetime import datetime
from ..models import TestModel


class CoreController:
    """ route controller """

    @staticmethod
    def test():
        """ evernode testing """
        fail2ban = Fail2Ban(1, location="passwords", ban_for=60)
        fail2ban.add_attempt(1)
        return JsonResponse(200, None, fail2ban.is_banned())

    @staticmethod
    def fail2ban_login():
        fail2ban_location = "login"
        user_auth = UserAuth(
            BaseUserModel,
            username_error="Please enter a username",
            password_error="Please Enter a password")
        session = user_auth.session()
        fail2ban = Fail2Ban(
            location=fail2ban_location,
            ban_for=60)
        if session is None:
            if user_auth.user is not None:
                fail2ban.object_id(user_auth.user.id)
                fail2ban.add_attempt()
                if fail2ban.is_banned():
                    return JsonResponse(403)
            return JsonResponse(401)
        else:
            fail2ban.object_id(user_auth.user.id)
            if fail2ban.is_banned():
                    return JsonResponse(403)
        Fail2Ban.clear(user_auth.user.id, fail2ban_location)
        return JsonResponse(200, None, session)

    @staticmethod
    def test_paginate(page_number, limit):
        """ evernode testing """
        paginate = Paginate(TestModel, limit)
        paginate.add_filter('name', 'LIKE', 'te%')
        return JsonResponse(
            200,
            None,
            paginate.json_paginate('/v1/tests/', page_number))

    @staticmethod
    def test_refresh_token():
        """ evernode testing """
        jwt = JWT()
        jwt.verify_http_auth_refresh_token()
        return JsonResponse(200, None, jwt.data)

    @staticmethod
    def test_test_model():
        """ evernode testing """
        return JsonResponse(200, None, TestModel.where_id(1))

    @staticmethod
    def test_validate_password_reset():
        """ evernode testing """
        formdata = FormData()
        formdata.add_field(
            'code', required=True, error='A code is required.')
        formdata.add_field(
            'password', required=True, error='A new password is required.')
        formdata.parse()
        result = BaseUserModel.validate_password_reset(
            formdata.values['code'], formdata.values['password'])
        return JsonResponse(200, None, result)

    @staticmethod
    def test_create_password_reset(email):
        """ evernode testing """
        token = BaseUserModel.create_password_reset(email, valid_for=3600)
        return JsonResponse(200, None, token)

    @staticmethod
    def test_json():
        """ evernode testing """
        class JJ(JsonModel):
            bob = None

            def __init__(self):
                self.bob = None
                self.time = datetime.now()
                self.time2 = {'ti_me': datetime.now(), 'set': set('test')}
                self.list = [1, datetime.now(), [{'test': [{
                    'date': datetime.now()}]}]]
                self.time3 = {
                    'ti_me': ['s', [datetime.now(), 1], datetime.now(), 1]}
                self.time4 = {
                    'ti_me': ['s', 'f', {'another_test': {
                        'another_date': datetime.now()}}]}
        return JsonResponse(200, None, JJ())

    @staticmethod
    def user_json():
        user = BaseUserModel.where_id(1)
        return JsonResponse(200, None, user)

    @staticmethod
    def test_email():
        email = Email(send_as_one=True)
        email.html('hello')
        email.text('hello')
        email.add_address('me@dylanharty.com')
        email.add_cc('example@atomhash.org')
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
        user = BaseUserModel()
        user.firstname = 'Dylan'
        user.lastname = 'Harty'
        user.email = 'example@atomhash.org'
        user.set_password('123321')
        user.save()
        return JsonResponse(200, None, user)

    def user_token():
        session = UserAuth(
            BaseUserModel,
            username_error="Please enter a username",
            password_error="Please Enter a password").session()
        if session is None:
            return JsonResponse(401)
        return JsonResponse(200, None, session)
