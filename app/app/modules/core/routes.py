from .controllers import CoreController
from .controllers import TestCtrl
from evernode.middleware import SessionMiddleware # noqa

routes = [
    {
        'url': '/no-database',
        'name': 'core-no-database',
        'methods': ['GET'],
        'function': CoreController.no_database},
    {
        'url': '/test',
        'name': 'core-test',
        'methods': ['GET', 'POST'],
        'function': CoreController.test},
    {
        'url': '/fail2ban-login',
        'name': 'core-fail2ban-login',
        'methods': ['POST'],
        'function': CoreController.fail2ban_login},
    {
        'url': '/password-reset',
        'name': 'core-password-reset-validate',
        'methods': ['POST'],
        'function': CoreController.test_validate_password_reset},
    {
        'url': '/password-reset/<email>',
        'name': 'core-password-reset-create',
        'methods': ['GET'],
        'function': CoreController.test_create_password_reset},
    {
        'url': '/user-json',
        'name': 'core-user-json',
        'methods': ['GET'],
        'function': CoreController.user_json},
    {
        'url': '/make-user',
        'name': 'core-make-user',
        'methods': ['GET'],
        'function': CoreController.make_user},
    {
        'url': '/user-token',
        'name': 'core-user-token',
        'methods': ['POST'],
        'function': CoreController.user_token},
    {
        'url': '/user-check',
        'name': 'core-user-check',
        'methods': ['GET'],
        'middleware': [SessionMiddleware],
        'function': CoreController.user_check},
    {
        'url': '/test-form',
        'name': 'core-test-form',
        'methods': ['POST'],
        'function': CoreController.test_form},
    {
        'url': '/generate-key',
        'name': 'core-generate-key',
        'methods': ['GET', 'POST'],
        'function': CoreController.generate_key},
    {
        'url': '/upload',
        'name': 'core-upload',
        'methods': ['POST'],
        'function': CoreController.test_form_upload},
    {
        'url': '/test-security',
        'name': 'core-test-security',
        'methods': ['GET'],
        'function': CoreController.test_security},
    {
        'url': '/test-render',
        'name': 'core-test-render',
        'methods': ['GET'],
        'function': CoreController.test_render},
    {
        'url': '/test-translator',
        'name': 'core-test-translator',
        'methods': ['GET'],
        'function': CoreController.test_translator},
    {
        'url': '/test-email',
        'name': 'core-test-email',
        'methods': ['GET'],
        'function': CoreController.test_email},
    {
        'url': '/test-refresh-token',
        'name': 'core-test-refresh-token',
        'methods': ['GET'],
        'function': CoreController.test_refresh_token},
    {
        'url': '/tests/page/<int:page_number>/<int:limit>',
        'name': 'core-test-paginate',
        'methods': ['GET'],
        'function': CoreController.test_paginate},
    # test ctrl
    {
        'url': '/test/model-json',
        'name': 'test-model-json',
        'methods': ['GET'],
        'function': TestCtrl.model_serialization_json},
    {
        'url': '/test/decimal-json',
        'name': 'test-decimal-json',
        'methods': ['GET'],
        'function': TestCtrl.decimal_serialization_json}]
