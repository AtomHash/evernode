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
        self.prefix = prefix
        self.format_prefix()

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

    def __format_prefix(self):
        if self.prefix is not None:
            self.prefix = self.prefix.strip('/')

    def format_prefix(self):
        """ Format prefix  """
        api_version = None
        if 'API' in self.flask_app.config:
            if self.prefix is None:
                self.prefix = self.flask_app.config['API']['PREFIX'] \
                    if 'PREFIX' in self.flask_app.config['API'] else None
            api_version = self.flask_app.config['API']['VERSION'] \
                if 'VERSION' in self.flask_app.config['API'] else None
        if self.prefix is not None and api_version is not None:
            if '{v}' in self.prefix:
                self.prefix = '%s' % (self.prefix.replace('{v}', api_version))
        elif self.prefix is None:
            self.prefix = ''
        self.__format_prefix()
