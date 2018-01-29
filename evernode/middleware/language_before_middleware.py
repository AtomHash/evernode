""" LanguageBeforeMiddleware """


class LanguageBeforeMiddleware:
    """ set current language for app user """
    wsgi_app = None
    flask_app = None

    def __init__(self, wsgi_app, flask_app):
        self.wsgi_app = wsgi_app
        self.flask_app = flask_app

    def __call__(self, environ, start_response):
        language = ''
        if 'HTTP_CONTENT_LANGUAGE' in environ:
            language = environ['HTTP_CONTENT_LANGUAGE']
        else:
            language = self.flask_app.config['DEFAULT_LANGUAGE']

        self.flask_app.config.update({'LANGUAGE': language})
        return self.wsgi_app(environ, start_response)
