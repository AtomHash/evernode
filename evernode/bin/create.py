#!/usr/bin/env python

import os
import sys
import click
from urllib import request
from evernode.classes import Json, Security


class Create:
    """ Easy evernode app creation"""

    dir_name = None
    config_file = None
    uwsgi_file = None
    app_file = None
    http_messages_file = None
    branch = None

    def __init__(self, dir_name, branch='dev-1.1.0'):
        self.dir_name = './evernode_%s' % (dir_name)
        self.branch = branch
        self.app_file = os.path.join(self.dir_name, 'app', 'app.py')
        self.http_messages_file = os.path.join(
            self.dir_name, 'app', 'resources',
            'lang', 'en', 'http_messages.lang')
        self.config_file = os.path.join(self.dir_name, 'app', 'config.json')
        self.uwsgi_file = os.path.join(self.dir_name, 'uwsgi.ini')
        print('Making folder structure.')
        self.make_structure()
        print('Downloading config.json...')
        self.configure_config()
        print('Downloading sample uwsgi.ini...')
        self.download_sample_uwsgi()
        print('Downloading sample app.py...')
        self.download_sample_app()
        print('Downloading sample resources/lang/en/http_messages.lang...')
        self.download_sample_http_errors()
        if click.confirm('Use a docker development enviroment?', default=True):
            self.configure_docker()
        print('Done!')

    def __touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def download_file(self, url, file_name):
        request.urlretrieve(url, file_name)

    def configure_config(self):
        # download current config file from github
        self.download_file(
            ('https://raw.githubusercontent.com/AtomHash/evernode/'
                '%s/app/app/config.json' % (self.branch)),
            self.config_file)
        config = Json.from_file(self.config_file)
        config['SERECT'] = Security.generate_key()
        config['KEY'] = Security.generate_key()
        Json.save_file(self.config_file, config)

    def download_sample_uwsgi(self):
        self.download_file(
            ('https://raw.githubusercontent.com/AtomHash/evernode/'
                '%s/app/uwsgi.ini' % (self.branch)),
            self.uwsgi_file)

    def download_sample_app(self):
        self.download_file(
            ('https://raw.githubusercontent.com/AtomHash/evernode/'
                '%s/app/app/app.py' % (self.branch)),
            self.app_file)

    def download_sample_http_errors(self):
        self.download_file(
            ('https://raw.githubusercontent.com/AtomHash/evernode/'
                '%s/app/app/resources/lang/en/http_messages.lang'
                % (self.branch)),
            self.http_messages_file)

    def configure_docker(self):
        needed_files = [
            {'docker': [
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/docker-compose.yml' % (self.branch))
            ]},
            {'build': [
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/supervisord.conf' % (self.branch)),
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/Dockerfile' % (self.branch)),
            ]},
            {'nginx': [
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/nginx/nginx.conf' % (self.branch))
            ]},
            {'ssls': [
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/nginx/ssls/'
                 'api.localhost.crt' % (self.branch)),
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/nginx/ssls/'
                 'api.localhost.key' % (self.branch))
            ]},
            {'conf.d': [
                ('https://raw.githubusercontent.com/AtomHash/evernode/'
                 '%s/app/docker/build/nginx/conf.d/'
                 'api.localhost.conf' % (self.branch))
            ]}]
        for folder in needed_files:
            for key, value in folder.items():
                    root = ''
                    if key is 'docker':
                        root = 'docker'
                    elif key is 'build':
                        root = 'docker/build'
                    elif key is 'nginx':
                        root = 'docker/build/nginx'
                    elif key is 'ssls':
                        root = 'docker/build/nginx/ssls'
                    elif key is 'conf.d':
                        root = 'docker/build/nginx/conf.d'
                    os.mkdir(os.path.join(self.dir_name, root))
                    for file in value:
                        self.__docker_file_download(root, file)

    def __docker_file_download(self, root, file):
        self.download_file(file, os.path.join(
            self.dir_name, root, file.rsplit('/', 1)[-1]))

    def make_structure(self):
        if os.path.isdir(self.dir_name):
            print('Error: Projects already exists.')
            sys.exit(1)
            return
        # make root folder
        os.mkdir(self.dir_name)
        # make app folder
        os.mkdir(os.path.join(self.dir_name, 'app'))
        # make app folder
        os.mkdir(os.path.join(self.dir_name, 'logs'))
        # make uploads folder
        os.mkdir(os.path.join(self.dir_name, 'uploads'))
        # make public folder
        os.mkdir(os.path.join(self.dir_name, 'public'))
        # make public static folder
        os.mkdir(os.path.join(self.dir_name, 'public', 'static'))
        # make app root modules folder
        os.mkdir(os.path.join(self.dir_name, 'app', 'modules'))
        self.__touch(
            os.path.join(self.dir_name, 'app', 'modules', '__init__.py'))
        # make app root resources folder
        os.mkdir(os.path.join(self.dir_name, 'app', 'resources'))
        os.mkdir(os.path.join(self.dir_name, 'app', 'resources', 'lang'))
        os.mkdir(os.path.join(self.dir_name, 'app', 'resources', 'lang', 'en'))
        os.mkdir(os.path.join(self.dir_name, 'app', 'resources', 'templates'))
