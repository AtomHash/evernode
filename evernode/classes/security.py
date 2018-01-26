""" helper functions for application security """

import base64
import random
import string
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class Security:
    """ static functions to help app security """

    @staticmethod
    def encrypt(clear_text) -> str:
        """ use config.json key to encrypt """
        cipher = Fernet(current_app.config['KEY'])
        return base64.b64encode(cipher.encrypt(clear_text)).decode()

    @staticmethod
    def decrypt(crypt_text) -> str:
        """ use config.json key to decrypt """
        cipher = Fernet(current_app.config['KEY'])
        return cipher.decrypt(base64.b64decode(crypt_text))

    @staticmethod
    def random_string(length) -> str:
        """ create a random string for security purposes """
        return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits)
            for _ in range(length))

    @staticmethod
    def hash(clear_text) -> str:
        """ hash clear text """
        return generate_password_hash(
            clear_text,
            method=current_app.config['AUTH']['PASSWORD_HASHING'])

    @staticmethod
    def verify_hash(clear_text, hashed_text) -> bool:
        """ check a hash """
        return check_password_hash(hashed_text, clear_text)
