""" Easy password reset for BaseUserModel"""

from ..models import PasswordResetModel
from .security import Security


class PasswordReset:
    """ Password Reset """
    email = ''
    code = None
    new_password = None
    user = None

    def __init__(self, user, email, code=None, new_password=None):
        self.user = user
        self.email = email
        self.code = code
        self.new_password = new_password

    def create_password_reset(self):
        """
        Create a password reset request in the user_password_resets
        database table set self.code to unhashed code, while hashed
        code gets stored in the database you may email the code
        to the user or use it for something else
        """
        user = self.user.get_by_email(self.email)
        if user is None:
            return False
        PasswordResetModel.delete_by_email(self.email)
        self.code = Security.random_string(6)
        password_reset_model = PasswordResetModel()
        password_reset_model.code = Security.hash(self.code)
        password_reset_model.email = self.email
        password_reset_model.user_id = user.id
        password_reset_model.save()
        return True

    def validate_and_reset(self):
        """
        Validates an unhashed code against a hashed code.
        Once the code has been validated and confirmed
        self.new_password will replace the old users password
        by email
        """
        password_reset_model = PasswordResetModel.get_by_email(self.email)
        if password_reset_model is None:
            return False
        if Security.verify_hash(self.code, password_reset_model.code):
            user = self.user.get_by_email(self.email)
            if user is None:
                return False
            user.set_password(self.new_password)
            PasswordResetModel.delete_by_email(self.email)
            return True
        return False
