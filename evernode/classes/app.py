"""
    Creates a Flask App using custom framework logic
"""
import sys
import os
from pathlib import Path
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
        self.load_config()
        self.load_cors()
        self.load_default_database()
        self.load_modules()
        self.load_before_middleware()

    def load_cors(self):
        """ default cors allow all """
        options = dict(
            origins='*',
            methods=[
                'GET',
                'HEAD',
                'POST',
                'OPTIONS',
                'PUT',
                'PATCH',
                'DELETE'],
            allow_headers='*',
            expose_headers=None,
            supports_credentials=False,
            max_age=None,
            send_wildcard=False,
            vary_header=True,
            resources=r'/*')
        if 'CORS' in self.app.config:
            if 'ORIGINS' in self.app.config['CORS']:
                options['origins'] = \
                    self.app.config['CORS']['ORIGINS']
            if 'METHODS' in self.app.config['CORS']:
                options['methods'] = \
                    self.app.config['CORS']['METHODS']
            if 'ALLOW_HEADERS' in self.app.config['CORS']:
                options['allow_headers'] = \
                    self.app.config['CORS']['ALLOW_HEADERS']
            if 'EXPOSE_HEADERS' in self.app.config['CORS']:
                options['expose_headers'] = \
                    self.app.config['CORS']['EXPOSE_HEADERS']
            if 'SUPPORTS_CREDENTIALS' in self.app.config['CORS']:
                options['supports_credentials'] = \
                    self.app.config['CORS']['SUPPORTS_CREDENTIALS']
            if 'MAX_AGE' in self.app.config['CORS']:
                options['max_age'] = \
                    self.app.config['CORS']['MAX_AGE']
            if 'SEND_WILDCARD' in self.app.config['CORS']:
                options['send_wildcard'] = \
                    self.app.config['CORS']['SEND_WILDCARD']
            if 'VARY_HEADER' in self.app.config['CORS']:
                options['vary_header'] = \
                    self.app.config['CORS']['VARY_HEADER']
            if 'RESOURCES' in self.app.config['CORS']:
                options['resources'] = \
                    self.app.config['CORS']['RESOURCES']
        CORS(self.app, **options)

    def load_default_database(self):
        """ Set default database form config.json """
        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
            self.app.config['SQLALCHEMY_BINDS']['DEFAULT']

    def api_prefix(self):
        """ Get api prefix set in config.json """
        config_api_prefix = self.app.config['API']['PREFIX']
        config_api_version = self.app.config['API']['VERSION']
        version_ident = '{version}'
        if '{version}' in config_api_prefix:
            return '/%s' % (config_api_prefix.replace(
                version_ident, config_api_version))
        return ''

    def load_before_middleware(self):
        """ Set before app middleware """
        self.app.wsgi_app = RouteBeforeMiddleware(
            self.app.wsgi_app,
            self.app, prefix=self.api_prefix())
        self.app.wsgi_app = LanguageBeforeMiddleware(
            self.app.wsgi_app, self.app)

    def load_config(self):
        """ Load config.json into memory """
        config_path = os.path.join(Path(sys.path[0]).parent, 'config.json')
        config = JsonHelper.from_file(config_path)
        if config is None:
            raise FileNotFoundError
        self.app.config.update(config)
        self.app.config.update(CONFIG_PATH=config_path)

    def load_modules(self):
        """ Load folders(custom modules) in modules folder """
        LoadModules(self.app)()
