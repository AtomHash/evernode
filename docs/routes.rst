.. _routes:

Routes
==================

EverNode requries a web server and Python3.6. It assumes you already have Python3.6 installed.

routes.py
---------

Each module needs a routes.py file. A basic routes.py file can look like::

    from .controllers import MockController

    routes = [
        {
            'url': '/hello-world',
            'name': 'hello-world',
            'methods': ['GET'],  # POST, PUT, PATCH, UPDATE
            'function': MockController.hello_world}]

Authorization on Routes
-----------------------

If you would like to lock a route to a logged in user. An :code:`Authorization: Bearer <token>`
HTTP header must be supplied. 

Example::

    # modules/<module-name>/routes.py
    from .controllers import MockController
    from evernode.middleware import SessionMiddleware # noqa

    routes = [
        {
            'url': '/hello-world',
            'name': 'hello-world',
            'methods': ['GET'],
            'middleware': [SessionMiddleware],  # returns a 401 response if not authorized
            'function': MockController.protected}]
    # -------------------------------------------------------
    # modules/<module-name>/controllers/mock_controller.py
    from flask import current_app # noqa
    from evernode.classes import JsonResponse, Render, Security, Email, UserAuth, FormData, Translator # noqa
    from evernode.decorators import middleware # noqa

    class MockController:
        """ Mock Module, Mock Controller """

        @staticmethod
        @middleware  # this is required!
        def protected():
            """ Hello World Controller Protected """
            return JsonResponse(200, None, "Hello World, you're authorized!")
