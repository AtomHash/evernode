"""
    Fetch form data
"""
import os
from flask import abort, request, current_app
from werkzeug.utils import secure_filename
from .json_response import JsonResponse


class FormData:
    json_form_data = None
    field_arguments = []
    file_arguments = []
    values = {}
    files = {}

    def __init__(self):
        self.field_arguments = []
        self.file_arguments = []
        self.values = {}
        self.files = {}
        self.json_form_data = self.get_json_form_data()

    def get_json_form_data(self):
        """ Load request Json Data, if any """
        return request.get_json(silent=True, force=True)

    def add_field(self, name, default=None, required=False, error=None):
        """ Add a text/non-file field to parse for a value in the request """
        if name is None:
            return
        self.field_arguments.append(dict(
            name=name,
            default=default,
            required=required,
            error=error))

    def add_file(self, name, required=False, error=None, extensions=None):
        """ Add a file field to parse on request (uploads) """
        if name is None:
            return
        self.file_arguments.append(dict(
            name=name,
            required=required,
            error=error,
            extensions=extensions))

    def file_save(self, name, filename=None, folder="", keep_ext=True) -> bool:
        """ Easy save of a file """
        if name in self.files:
            file_object = self.files[name]
            clean_filename = secure_filename(file_object.filename)
            if filename is not None and keep_ext:
                clean_filename = filename + ".%s" % \
                    (clean_filename.rsplit('.', 1)[1].lower())
            elif filename is not None and not keep_ext:
                clean_filename = filename
            file_object.save(os.path.join(
                current_app.config['UPLOADS']['FOLDER'],
                folder, clean_filename))
        return None

    def parse(self, fail_callback=None):
        """ Parse text fields and file fields for values and files """
        # get text fields
        for field in self.field_arguments:
            self.values[field['name']] = self.__get_value(field['name'])
            if self.values[field['name']] is None and field['required']:
                if fail_callback is not None:
                    fail_callback()
                self.__invalid_request(field['error'])
        # get file fields
        for file in self.file_arguments:
            self.files[file['name']] = self.__get_file(file)
            if self.files[file['name']] is None and file['required']:
                if fail_callback is not None:
                    fail_callback()
                self.__invalid_request(file['error'])

    def __get_value(self, field_name):
        """ Get request Json value by field name """
        value = request.values.get(field_name)
        if value is None:
            if self.json_form_data is None:
                value = None
            elif field_name in self.json_form_data:
                value = self.json_form_data[field_name]
        return value

    def __get_file(self, file):
        """ Get request file and do a security check """
        file_object = None
        if file['name'] in request.files:
            file_object = request.files[file['name']]
            clean_filename = secure_filename(file_object.filename)
            if clean_filename == '':
                return file_object
            if file_object and self.__allowed_extension(
                    clean_filename, file['extensions']):
                return file_object
        elif file['name'] not in request.files and file['required']:
            return file_object
        return file_object

    def __allowed_extension(self, filename, extensions):
        """ Check allowed file extensions """
        allowed_extensions = current_app.config['UPLOADS']['EXTENSIONS']
        if extensions is not None:
            allowed_extensions = extensions
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
            allowed_extensions

    def __invalid_request(self, error):
        """ Error response on failure """
        # TODO: make this modifiable
        error = {
            'error': {
                'message': error
            }
        }
        abort(JsonResponse(status_code=400, data=error))
