"""
    Helper functions for application security
"""
import secrets
import random
import string
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app


class Security:
    """ Static functions to help app security """

    @staticmethod
    def generate_uuid(multiplier=1):
        uuid = ''
        counter = 0
        while counter < multiplier:
            uuid = uuid + secrets.token_hex()
            counter = counter + 1
        return uuid

    @staticmethod
    def generate_key() -> str:
        """ Generate a Fernet key"""
        return Fernet.generate_key().decode("utf-8")

    @staticmethod
    def encrypt(clear_text) -> str:
        """ Use config.json key to encrypt """
        if not isinstance(clear_text, bytes):
            clear_text = str.encode(clear_text)
        cipher = Fernet(current_app.config['KEY'])
        return cipher.encrypt(clear_text).decode("utf-8")

    @staticmethod
    def decrypt(crypt_text) -> str:
        """ Use config.json key to decrypt """
        cipher = Fernet(current_app.config['KEY'])
        if not isinstance(crypt_text, bytes):
            crypt_text = str.encode(crypt_text)
        return cipher.decrypt(crypt_text).decode("utf-8")

    @staticmethod
    def random_string(length) -> str:
        """ Create a random string for security purposes """
        return ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + string.digits)
            for _ in range(length))

    @staticmethod
    def hash(clear_text) -> str:
        """ Hash clear text """
        return generate_password_hash(
            clear_text,
            method=current_app.config['AUTH']['PASSWORD_HASHING'])

    @staticmethod
    def verify_hash(clear_text, hashed_text) -> bool:
        """ Check a hash """
        return check_password_hash(hashed_text, clear_text)
