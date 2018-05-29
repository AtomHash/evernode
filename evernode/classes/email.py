"""
    Collect email information
"""
import os
import subprocess
import json
import base64
from flask import current_app
from pathlib import Path
from ..functions import get_python_path


class Email:
    """ Set up an email """
    config_path = None
    __addresses = []
    __ccs = []
    __files = []
    __html = ''
    __text = ''
    __subject = ''
    __data = {}
    send_as_one = None

    def __init__(self, send_as_one=False):
        self.config_path = None
        self.__addresses = []
        self.__ccs = []
        self.__files = []
        self.__html = ''
        self.__text = ''
        self.__subject = ''
        self.__data = {}
        self.send_as_one = send_as_one
        if 'CONFIG_PATH' in current_app.config:
            self.config_path = current_app.config['CONFIG_PATH']

    def add_address(self, address):
        """ Add email address """
        self.__addresses.append(address)
        return self

    def add_addresses(self, addresses):
        """ Add addresses from array """
        self.__addresses.extend(addresses)
        return self

    def add_cc(self, address):
        """ Add carbon copy """
        self.__ccs.append(address)
        return self

    def add_ccs(self, addresses):
        """ Add carbon copy with array of addresses """
        self.__ccs.extend(addresses)
        return self

    def add_file(self, absolute_file_path):
        """ Add attachment to email """
        self.__files.append(absolute_file_path)
        return self

    def html(self, html):
        """ Set html content """
        self.__html = html
        return self

    def text(self, text):
        """ Set text content """
        self.__text = text
        return self

    def subject(self, subject):
        """ Set email subject """
        self.__subject = subject
        return self

    def __create(self):
        """ Construct the email """
        self.__data = json.dumps({
            'config_path': self.encode(self.config_path),
            'subject': self.encode(self.__subject),
            'text': self.encode(self.__text),
            'html': self.encode(self.__html),
            'files': self.__files,
            'send_as_one': self.send_as_one,
            'addresses': self.__addresses,
            'ccs': self.__ccs,
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
        self.__create()
        email_script = \
            os.path.join(Path(__file__).parents[1], 'scripts', 'sendemail.py')
        if os.path.exists(email_script):
            subprocess.Popen(
                [get_python_path(), email_script, self.__data],
                stdin=None, stdout=None, stderr=None, close_fds=True)
