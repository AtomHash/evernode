""" Easy Translator for modules and appp """
import os
import sys
from flask import current_app
from ..helpers import JsonHelper


class Translator:
    """ Uses dot-key syntax to translate phrases to words """
    path = None
    extension = '.lang'
    app_language = ''

    def __init__(self, module_folder_name=None):
        self.app_language = current_app.config['LANGUAGE']
        if module_folder_name is None:
            path = os.path.join(
                sys.path[0], 'resources', 'lang', self.app_language)
            if os.path.isdir(path):
                self.path = path
            else:
                self.path = os.path.join(
                    sys.path[0],
                    'resources',
                    'lang',
                    current_app.config['DEFAULT_LANGUAGE'])
        else:
            path = os.path.join(
                sys.path[0],
                'modules',
                module_folder_name,
                'resources',
                'lang',
                self.app_language)
            if os.path.isdir(path):
                self.path = path
            else:
                raise NotADirectoryError

    def trans(self, key) -> str:
        """
        ** Execute a translate command **
            file.command
            file.level1.command
            file.level1.level2.command
            ect...
        Example:
            Translator.trans('messages.hello')
            If language is en,
            In the example a file called
                resources/lang/en/messages.lang will be opened
            and parsed for { 'hello': 'Some english text' }
            If language is fr,
            In the example a file called
                resources/lang/fr/messages.lang will be opened
            and parsed for { 'hello': 'Some french text' }
        """
        key_list = self.__list_key__(key)
        json = self.__load_file__(key_list)
        current_selection = json
        for parsed_dot_key in key_list:
            try:
                current_selection = current_selection[parsed_dot_key]
            except (Exception, BaseException) as error:
                if current_app.config['DEBUG']:
                    print(error)
                return None
        return current_selection

    def __load_file__(self, key_list) -> str:
        """ Load a translator file """
        file = str(key_list[0]) + self.extension
        key_list.pop(0)
        file_path = os.path.join(self.path, file)
        if os.path.exists(file_path):
            return JsonHelper.from_file(file_path)

    def __list_key__(self, key) -> list:
        """ list a trans command by splitting dot-key syntax """
        return key.split(".")
