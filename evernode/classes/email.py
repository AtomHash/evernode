"""
    Collect email information
"""
from flask import current_app
import os
from pathlib import Path
import subprocess
import json
import base64


class Email:
    """ Set up an email """
    config_path = None
    __addresses = []
    __html = ''
    __text = ''
    __subject = ''
    __data = {}

    def __init__(self, config_path=None):
        if config_path is None:
            if 'CONFIG_PATH' in current_app.config:
                self.config_path = current_app.config['CONFIG_PATH']

    def add_address(self, address):
        """ add email address """
        self.__addresses.append(address)

    def html(self, html):
        """ Set html content """
        self.__html = html

    def text(self, text):
        """ Set text content """
        self.__text = text

    def subject(self, subject):
        """ Set email subject """
        self.__subject = subject

    def __create__(self):
        """ Construct the email """
        # TODO: Use pickle instead of encode base64 & JSON
        self.__data = json.dumps({
            'config_path': self.encode(self.config_path),
            'subject': self.encode(self.__subject),
            'text': self.encode(self.__text),
            'html': self.encode(self.__html),
            'addresses': self.__addresses,
        })

    def encode(self, value):
        """ Encode parts of email to base64 for transfer """
        return base64.b64encode(value.encode()).decode()

    def send(self):
        """
        Construct and execute sendemail.py script
        Finds python binary by os.py, then
        uses the /usr/bin/python to execute email script
        """
        self.__create__()
        email_script = \
            os.path.join(Path(__file__).parents[1], 'scripts', 'sendemail.py')
        if os.path.exists(email_script):
            python = str(os.__file__.rsplit('/')[-2])
            python_bin = '/usr/bin/%s' % (python)
            subprocess.Popen(
                [python_bin, email_script, self.__data],
                stdin=None, stdout=None, stderr=None, close_fds=True)
            """
            output = subprocess.check_output([python_bin, \
                email_script, self.__data])
            print(str(output))
            print(python_bin)
            """
