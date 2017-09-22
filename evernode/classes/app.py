"""
    Creates a Flask App using custom framework logic
"""
from flask import Flask
from flask_cors import CORS
from ..middleware import RouteBeforeMiddleware, LanguageBeforeMiddleware
from .load_modules import LoadModules
from ..helpers import JsonHelper
from ..models import db

class App:
    """ Creates a Custom Flask App """
    app = Flask

    def __init__(self, name):
        self.app = Flask(name)
        db.init_app(self.app)
        self.load_cors()
        self.load_config()
        self.load_default_database()
        self.load_modules()
        self.load_before_middleware()

    def load_cors(self):
        """ default cors allow all """
        CORS(self.app, resources=r'/*',
             allow_headers=[
                 'Origin',
                 'Content-Type',
                 'Accept',
                 'Authorization',
                 'X-Request-With',
                 'Content-Language'
             ],
             supports_credentials=True)

    def load_default_database(self):
        """ Set default database form config.json """
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.app.config['SQLALCHEMY_BINDS']['default']

    def api_prefix(self):
        """ Get api prefix set in config.json """
        config_api_prefix = self.app.config['API']['PREFIX']
        config_api_version = self.app.config['API']['VERSION']
        version_ident = '{version}'
        if '{version}' in config_api_prefix:
            return '/' + config_api_prefix.replace(version_ident, config_api_version)
        return ''

    def load_before_middleware(self):
        """ Set before app middleware """
        self.app.wsgi_app = RouteBeforeMiddleware(self.app.wsgi_app, \
            self.app, prefix=self.api_prefix())
        self.app.wsgi_app = LanguageBeforeMiddleware(self.app.wsgi_app, self.app)

    def load_config(self):
        """ Load config.json into memory """
        config = JsonHelper.from_file('../config.json')
        if config is None:
           raise FileNotFoundError
        self.app.config.update(config)

    def load_modules(self, override=False):
        """ Load folders(custom modules) in modules folder """
        if self.app.config['DEBUG'] != True or override:
            LoadModules(self.app)()