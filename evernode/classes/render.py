"""
    Easy way to render jinja templates
"""

import os
import sys
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
from flask import current_app


class Render:
    """ Jinja template renderer """

    jinja = None
    template_path = None
    templates = {}

    def __init__(self, module_name=None):
        if module_name is None:
            path = os.path.join(sys.path[0], 'resources', 'templates')
            if os.path.isdir(path):
                self.template_path = path
            else:
                raise NotADirectoryError
        else:
            path = os.path.join(
                sys.path[0],
                'modules',
                module_name,
                'resources',
                'templates')
            if os.path.isdir(path):
                self.template_path = path
            else:
                raise NotADirectoryError
        self.__init_jinja()

    def __init_jinja(self):
        self.jinja = Environment(
            loader=FileSystemLoader(self.template_path),
            trim_blocks=True)

    def compile(self, name, folder=None, data=None):
        """
        renders template_name + self.extension file with data using jinja
        """
        template_name = name.replace('/', "")
        if folder is None:
            folder = ""
        full_name = os.path.join(
            folder.strip('/'), template_name)
        if data is None:
            data = {}
        try:
            self.templates[template_name] = \
                self.jinja.get_template(full_name).render(data)
        except TemplateNotFound as template_error:
            if current_app.config['DEBUG']:
                raise template_error
