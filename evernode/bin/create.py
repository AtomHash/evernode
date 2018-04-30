#!/usr/bin/env python

import os
import sys
import click
import yaml
from urllib import request
from evernode.classes import Json, Security


class Create:
    """ Easy evernode app creation"""

    app_name = None
    dir_name = None
    config_file = None
    uwsgi_file = None
    app_file = None
    http_messages_file = None
    branch = None

    def __init__(self, app_name, branch='master'):
        self.app_name = 'evernode_%s' % (app_name)
        self.dir_name = './%s' % (self.app_name)
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
        config['NAME'] = self.app_name
        config['SERECT'] = Security.generate_key()
        config['KEY'] = Security.generate_key()
        config['SQLALCHEMY_BINDS']['DEFAULT'] = \
            'mysql://db_user:password@localhost/db_name'
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
        docker_compose = os.path.join(
            self.dir_name, 'docker', 'docker-compose.yml')
        with open(docker_compose, 'r') as docker_compose_opened:
            try:
                yml = yaml.load(docker_compose_opened)
                yml['services'][self.app_name] = \
                    yml['services'].pop('evernode-development', None)
                yml['services'][self.app_name]['container_name'] = \
                    self.app_name
                del yml['services'][self.app_name]['volumes'][-1]
                with open(docker_compose, 'w') as new_docker_compose:
                    yaml.dump(yml, new_docker_compose,
                              default_flow_style=False, allow_unicode=True)
            except yaml.YAMLError as exc:
                print('Error: Cannot parse docker-compose.yml')
        dockerfile = os.path.join(
            self.dir_name, 'docker', 'build', 'Dockerfile')
        with open(dockerfile, 'r') as dockerfile_opened:
            lines = dockerfile_opened.readlines()
            lines[-1] = ('ENTRYPOINT pip3.6 install --upgrade -r /srv/app/'
                         'requirements.txt && python2.7 /usr/bin/supervisord')
            with open(dockerfile, 'w') as df_opened_writable:
                df_opened_writable.writelines(lines)

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
        requirements_file = os.path.join(
            self.dir_name, 'app', 'requirements.txt')
        self.__touch(requirements_file)
        with open(requirements_file, 'w') as requirements_file_writable:
            requirements_file_writable.write('evernode')
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
