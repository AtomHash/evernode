"""
    Fetch form data
"""
from flask import abort, request
from .json_response import JsonResponse


class FormData:
    json_form_data = None
    field_arguments = []
    values = {}

    def __init__(self):
        self.json_form_data = self.get_json_form_data()

    def get_json_form_data(self):
        return request.get_json(silent=True, force=True)

    def add_field(self, name, default=None, required=False, error=None):
        if name is None:
            return
        self.field_arguments.append(dict(
            name=name,
            default=default,
            required=required,
            error=error))

    def parse(self):
        for field in self.field_arguments:
            self.values[field['name']] = self.get_value(field['name'])
            if self.values[field['name']] is None and field['required']:
                self.invalid_request(field['error'])

    def get_value(self, field_name):
        value = request.values.get(field_name)
        if value is None:
            if self.json_form_data is None:
                value = None
            elif field_name in self.json_form_data:
                value = self.json_form_data[field_name]
        return value

    def invalid_request(self, error):
        error = {
            'error': {
                'message': error
            }
        }
        abort(JsonResponse(status_code=400, data=error).create())
