""" RouteBeforeMiddleware """

from ..classes.json_response import JsonResponse


class RouteBeforeMiddleware:
    """ add prefix to url """
    wsgi_app = None
    flask_app = None

    def __init__(self, wsgi_app, flask_app, prefix=''):
        self.wsgi_app = wsgi_app
        self.flask_app = flask_app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        with self.flask_app.app_context():
            if environ['PATH_INFO'].startswith(self.prefix):
                environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
                environ['SCRIPT_NAME'] = self.prefix
                return self.wsgi_app(environ, start_response)
            json_response = JsonResponse(404)
            start_response(
                json_response.status(),
                [('Content-Type', json_response.mimetype())])
            return [json_response.content().encode()]
