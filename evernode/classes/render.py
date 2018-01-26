""" easy way to render jinja templates """

import os
import sys
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from flask import current_app


class Render:
    """ Jinja template renderer """

    path = None
    extension = '.html'
    extension_text = '.txt'
    jinja = None
    html = None
    text = None

    def __init__(self, module_folder_name=None):
        if module_folder_name is None:
            path = os.path.join(sys.path[0], 'resources', 'emails')
            if os.path.isdir(path):
                self.path = path
            else:
                raise NotADirectoryError
        else:
            path = os.path.join(
                sys.path[0],
                'modules',
                module_folder_name,
                'resources',
                'emails')
            if os.path.isdir(path):
                self.path = path
            else:
                raise NotADirectoryError
        self.__jinja_init__()

    def __jinja_init__(self):
        self.jinja = Environment(
            loader=FileSystemLoader(self.path),
            trim_blocks=True)

    def compile_text(self, template_name, data=None):
        """
        renders template_name + self.extension_text
        file with data using jinja
        """
        if data is None:
            data = {}
        try:
            self.text = self.jinja.get_template(
                template_name + self.extension_text).render(data)
        except TemplateNotFound as template_error:
            if current_app.config['DEBUG']:
                print(template_error)
            return None

    def compile(self, template_name, data=None):
        """
        renders template_name + self.extension file with data using jinja
        """
        if data is None:
            data = {}
        try:
            self.html = self.jinja.get_template(
                template_name + self.extension).render(data)
            self.compile_text(template_name, data)
        except TemplateNotFound as template_error:
            if current_app.config['DEBUG']:
                print(template_error)
            return None
