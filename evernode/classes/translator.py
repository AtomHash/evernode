""" Easy Translator """
import os
from flask import current_app, request
from werkzeug.utils import secure_filename
from .json import Json


class Translator:
    """ Uses dot-key syntax to translate phrases to words """

    app_language = None
    module_name = None

    def __init__(self, module_name=None, environ=None):
        try:
            self.app_language = request.headers.get('Content-Language')
        except (Exception, BaseException) as error:
            if environ is not None:
                if 'HTTP_CONTENT_LANGUAGE' in environ:
                    self.app_language = environ['HTTP_CONTENT_LANGUAGE']
            if environ is None and current_app.config['DEBUG']:
                raise RuntimeError('When running out of request context, '
                                   'please specify environ')
        if self.app_language is None:
            if 'DEFAULT_LANGUAGE' in current_app.config:
                self.app_language = current_app.config['DEFAULT_LANGUAGE']
            elif 'DEFAULT_LANGUAGE' not in current_app.config:
                if current_app.config['DEBUG']:
                    raise Exception(
                        'Please set "DEFAULT_LANGUAGE" in evernode config')
        else:
            # just strip encase of an absolute path in content-language
            self.app_language = secure_filename(self.app_language)
        self.module_name = module_name
        if self.module_name is None:
            self.module_name = 'root'

    def trans(self, key) -> str:
        """
        Root Example:
        Translator()
        Translator.trans('messages.hello')
        resources/lang/en/messages.lang will be opened
        and parsed for { 'hello': 'Some english text' }
        If language is fr,
        resources/lang/fr/messages.lang will be opened
        and parsed for { 'hello': 'Some french text' }
        Module Example:
        Translator('[module-name]')
        Translator.trans('messages.hello')
        """

        key_list = self.__list_key(key)
        try:
            current_selection = \
                current_app.config['LANGUAGE_PACKS'][
                    self.module_name][self.app_language]
        except KeyError as error:
            if current_app.config['DEBUG']:
                raise error
            return None
        for parsed_dot_key in key_list:
            try:
                current_selection = current_selection[parsed_dot_key]
            except (Exception, BaseException) as error:
                if current_app.config['DEBUG']:
                    raise error
                return None
        return current_selection

    def __load_file(self, key_list) -> str:
        """ Load a translator file """
        file = str(key_list[0]) + self.extension
        key_list.pop(0)
        file_path = os.path.join(self.path, file)
        if os.path.exists(file_path):
            return Json.from_file(file_path)
        else:
            raise FileNotFoundError(file_path)

    def __list_key(self, key) -> list:
        """ List a trans command by splitting dot-key syntax """
        return key.split(".")
