#!/usr/bin/env python

import os
import sys
from urllib import request


class Module:
    """ Easy evernode modules """

    module_name = None
    module_path = None
    branch = None

    def __init__(self, module_name, command='init', branch='master'):
        self.branch = branch
        self.module_name = module_name
        self.module_path = './%s' % (self.module_name)
        getattr(self, command)()

    def __touch(self, path):
        with open(path, 'a'):
            os.utime(path, None)

    def download_file(self, url, file_name):
        request.urlretrieve(url, file_name)

    def easy_file_download(self, root, file):
        file_name = file.rsplit('/', 1)[-1]
        print('Downloading %s...' % (file_name))
        self.download_file(file, os.path.join(
            self.module_path, root, file_name))

    def init(self):
        self.make_structure()
        self.easy_file_download(
            '',
            ('https://raw.githubusercontent.com/AtomHash/evernode/'
             '%s/app/app/modules/mock_module/routes.py' % (self.branch)))
        print("""
              Done!
              %s module created.
              """ % (self.module_name))

    def make_structure(self):
        if os.path.isdir(self.module_path):
            print('Error: Module already exists.')
            sys.exit(1)
            return
        # make root folder
        os.mkdir(self.module_path)
        # make root __init__
        self.__touch(
            os.path.join(self.module_path, '__init__.py'))
        # make sub folders
        os.mkdir(os.path.join(self.module_path, 'controllers'))
        os.mkdir(os.path.join(self.module_path, 'models'))
        os.mkdir(os.path.join(self.module_path, 'classes'))
        # make sub-folder __init__ files
        self.__touch(
            os.path.join(self.module_path, 'controllers', '__init__.py'))
        self.__touch(
            os.path.join(self.module_path, 'models', '__init__.py'))
        self.__touch(
            os.path.join(self.module_path, 'classes', '__init__.py'))
        # make module resources folder
        os.mkdir(os.path.join(self.module_path, 'resources'))
        os.mkdir(os.path.join(self.module_path, 'resources', 'lang'))
        os.mkdir(os.path.join(self.module_path, 'resources', 'lang', 'en'))
        os.mkdir(os.path.join(self.module_path, 'resources', 'templates'))
