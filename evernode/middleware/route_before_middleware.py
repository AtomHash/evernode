""" RouteBeforeMiddleware """
from werkzeug.exceptions import NotFound
from ..classes.json_response import JsonResponse


class RouteBeforeMiddleware:
    """ add prefix to url """
    wsgi_app = None
    flask_app = None
    prefix = None

    def __init__(self, wsgi_app, flask_app, prefix=None):
        self.wsgi_app = wsgi_app
        self.flask_app = flask_app
        self.prefix = flask_app.config['FORMATTED_PREFIX']

    def __call__(self, environ, start_response):
        with self.flask_app.app_context():
            if environ['PATH_INFO'].strip('/').lower().startswith(self.prefix):
                environ['PATH_INFO'] = \
                    environ['PATH_INFO'][len(self.prefix) + 1:]
                environ['SCRIPT_NAME'] = self.prefix
                return self.wsgi_app(environ, start_response)
            if 404 in self.flask_app.error_handler_spec:
                response = self.flask_app.error_handler_spec[404][NotFound](
                    NotFound, environ=environ)
                start_response(
                    response.status(),
                    [('Content-Type', response.mimetype())])
                return [response.content().encode()]
            json_response = JsonResponse(404, environ=environ)
            start_response(
                json_response.status(),
                [('Content-Type', json_response.mimetype())])
            return [json_response.content().encode()]
