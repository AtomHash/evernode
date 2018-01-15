#! /usr/local/bin/python
""" script to send an email async-wise """
import json
import os
import sys
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

    def __init__(self):
        self.parse()
        with open(self.config_path, 'r') as json_stream:
            self.config = json.load(json_stream)['EMAIL']
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
        self.addresses = data['addresses']

    def decode(self, value):
        """ decode args """
        return base64.b64decode(value).decode()

    def courier(self):
        """ set to from subject """
        self.multipart['Subject'] = self.subject
        self.multipart['From'] = self.config['EMAIL']
        self.multipart['To'] = ", ".join(self.addresses)

    def construct_message(self):
        """ construct the email message """
        html = MIMEText(self.html, 'html')
        alt_text = MIMEText(self.text, 'plain')
        self.multipart.attach(html)
        self.multipart.attach(alt_text)

    def send(self):
        """ send email message for to que """
        self.smtp.ehlo()
        self.smtp.login(self.config['USERNAME'], self.config['PASSWORD'])
        self.smtp.send_message(
            self.multipart, self.config['EMAIL'], self.addresses)
        self.smtp.quit()

    def create_email(self):
        """ main function to construct and send email """
        self.construct_message()
        self.courier()
        self.send()


if __name__ == '__main__':
    SendEmail()
