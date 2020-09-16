"""
    Creates a Flask App using custom framework logic
"""
import sys
import os
from flask import Flask
from flask_cors import CORS
from ..middleware import RouteBeforeMiddleware
from .json import Json
from .load_modules import LoadModules
from .load_language_files import LoadLanguageFiles
from ..functions import get_subdirectories
from ..models import db


class App:
    """ Creates a Custom Flask App """
    app = Flask
    root_path = None
    config_path = None
    prefix = None

    def __init__(self, name, prefix=None, middleware=None,
                 root_path=None, config_path=None):
        self.app = Flask(name)
        self.root_path = root_path
        self.config_path = config_path
        self.__root_path()
        self.load_config()
        self.load_database()
        self.load_cors()
        self.load_modules()
        self.load_language_files()
        self.prefix = self.__format_prefix(prefix)
        self.load_before_middleware(middleware)

    def __root_path(self):
        """ Just checks the root path if set """
        if self.root_path is not None:
            if os.path.isdir(self.root_path):
                sys.path.append(self.root_path)
                return
            raise RuntimeError('EverNode requires a valid root path.'
                               ' Directory: %s does not exist'
                               % (self.root_path))

    def __format_prefix(self, prefix):
        """ Format prefix  """
        api_version = None
        if prefix is not None:
            self.prefix = prefix
        else:
            if 'API' in self.app.config:
                if self.prefix is None:
                    self.prefix = self.app.config['API']['PREFIX'] \
                        if 'PREFIX' in self.app.config['API'] else None
                api_version = self.app.config['API']['VERSION'] \
                    if 'VERSION' in self.app.config['API'] else None
            if self.prefix is not None and api_version is not None:
                if '{v}' in self.prefix:
                    self.prefix = '%s' % \
                        (self.prefix.replace('{v}', api_version))
            elif self.prefix is None:
                self.prefix = ''
        if self.prefix is not None:
            self.prefix = self.prefix.strip('/')
        self.app.config.update({'FORMATTED_PREFIX': self.prefix})

    def get_modules(self) -> list:
        """  Get the module names(folders) in root modules folder """
        directory = None
        if self.root_path is not None:
            directory = os.path.join(self.root_path, 'modules')
        else:
            directory = os.path.join(sys.path[0], 'modules')
        if os.path.isdir(directory):
            return get_subdirectories(directory)
        raise RuntimeError('EverNode requires a valid root modules folder.'
                           'Directory: %s does not exist' % (directory))

    def load_database(self):
        """ Load default database, init flask-SQLAlchemy """
        if 'DISABLE_DATABASE' in self.app.config:
            if self.app.config['DISABLE_DATABASE']:
                return
        if 'SQLALCHEMY_DATABASE_URI' not in self.app.config:
            self.app.config['SQLALCHEMY_DATABASE_URI'] = \
                self.app.config['SQLALCHEMY_BINDS']['DEFAULT']
        db.init_app(self.app)

    def load_cors(self):
        """ Default cors allow all """
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

    def load_before_middleware(self, before_middleware):
        """ Set before app middleware """
        # prefix api middleware
        self.app.wsgi_app = RouteBeforeMiddleware(
            self.app.wsgi_app,
            self.app)
        # custom middleware
        if before_middleware is not None:
            for middleware in before_middleware:
                if isinstance(middleware, dict):
                    self.app.wsgi_app = middleware['middleware'](
                        self.app.wsgi_app, self.app, middleware['kargs'])
                else:
                    self.app.wsgi_app = middleware(self.app.wsgi_app, self.app)

    def load_config(self):
        """ Load EverNode config.json """
        config_path = None
        if self.config_path is not None:
            config_path = os.path.join(self.config_path, 'config.json')
        elif self.root_path is not None and self.config_path is None:
            config_path = os.path.join(self.root_path, 'config.json')
        else:
            config_path = os.path.join(sys.path[0], 'config.json')
        if os.path.exists(config_path):
            config = Json.from_file(config_path)
            if config is None:
                raise RuntimeError('EverNode config.json requires valid json.')
            self.app.config.update(config)
            self.app.config.update(CONFIG_PATH=config_path)
            return
        raise FileNotFoundError(config_path)

    def load_modules(self):
        """ Load folders(custom modules) in modules folder """
        LoadModules(self)()

    def load_language_files(self):
        """ Load language fiels in resources/lang dirs """
        LoadLanguageFiles(self)()
