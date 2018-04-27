#!/usr/bin/env python

""" script to send an email async-wise """
import json
import os
from os.path import basename
import sys
import base64
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
os.chdir(FILE_PATH)


class SendEmail:
    """ send email from the command line with async abilities """
    multipart = MIMEMultipart
    smtp = smtplib.SMTP
    config_path = None
    config = None
    subject = None
    text = None
    html = None
    addresses = None
    ccs = None
    send_as_one = None
    files = []

    def __init__(self):
        self.parse()
        with open(self.config_path, 'r') as json_stream:
            loaded_json = json.load(json_stream)
            if 'EMAIL' not in loaded_json:
                raise RuntimeError(
                    'EverNode sendemail.py requires SMTP login details.')
            self.config = loaded_json['EMAIL']
            self.smtp = smtplib.SMTP(self.config['HOST'], self.config['PORT'])
            self.smtp.starttls()
            self.smtp.set_debuglevel(0)
            self.multipart = MIMEMultipart('alternative')
            self.create_email()

    def parse(self):
        """ parses args json """
        data = json.loads(sys.argv[1])
        self.config_path = self.decode(data['config_path'])
        self.subject = self.decode(data['subject'])
        self.text = self.decode(data['text'])
        self.html = self.decode(data['html'])
        self.send_as_one = data['send_as_one']
        if 'files' in data:
            self.parse_files(data['files'])
        self.ccs = data['ccs']
        self.addresses = data['addresses']
        if not self.addresses:
            raise ValueError(
                'Atleast one email address is required to send an email')

    def parse_files(self, files):
        if files is None or not files:
            return
        for file in files:
            part = None
            with open(file, "rb") as file_opened:
                part = MIMEApplication(
                    file_opened.read(),
                    Name=basename(file)
                )
            part['Content-Disposition'] = \
                'attachment; filename="%s"' % basename(file)
            self.files.append(part)

    def decode(self, value):
        """ decode args """
        return base64.b64decode(value).decode()

    def construct_message(self, email=None):
        """ construct the email message """
        # add subject, from and to
        self.multipart['Subject'] = self.subject
        self.multipart['From'] = self.config['EMAIL']
        self.multipart['Date'] = formatdate(localtime=True)
        if email is None and self.send_as_one:
            self.multipart['To'] = ", ".join(self.addresses)
        elif email is not None and self.send_as_one is False:
            self.multipart['To'] = email
        # add ccs
        if self.ccs is not None and self.ccs:
            self.multipart['Cc'] = ", ".join(self.ccs)
        # add html and text body
        html = MIMEText(self.html, 'html')
        alt_text = MIMEText(self.text, 'plain')
        self.multipart.attach(html)
        self.multipart.attach(alt_text)
        for file in self.files:
            self.multipart.attach(file)

    def connect(self):
        self.smtp.ehlo()
        self.smtp.login(self.config['USERNAME'], self.config['PASSWORD'])

    def disconnect(self):
        self.smtp.quit()

    def send(self, email=None):
        """ send email message """
        if email is None and self.send_as_one:
            self.smtp.send_message(
                self.multipart, self.config['EMAIL'], self.addresses)
        elif email is not None and self.send_as_one is False:
            self.smtp.send_message(
                self.multipart, self.config['EMAIL'], email)
        self.multipart = MIMEMultipart('alternative')

    def create_email(self):
        """ main function to construct and send email """
        self.connect()
        if self.send_as_one:
            self.construct_message()
            self.send()
        elif self.send_as_one is False:
            for email in self.addresses:
                self.construct_message(email)
                self.send(email)
        self.disconnect()


if __name__ == '__main__':
    SendEmail()
