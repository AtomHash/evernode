"""
    Used for banning ip's for a certain amoung of time
"""
from flask import request
from ..models.fail2ban_model import Fail2BanModel


class Fail2Ban:
    """ EverNode Fail2Ban """
    __fail2ban_model = None
    __location = None
    __object_id = None
    __ip = None
    ban_for = None
    max_attempts = None

    def __init__(self, object_id=None, location="",
                 max_attempts=3, ip=None, ban_for=1800):
        self.__object_id = object_id
        self.ban_for = ban_for
        self.max_attempts = max_attempts
        self.__location = location
        if ip is None:
            self.__ip = request.remote_addr
        self.__fail2ban_model = Fail2BanModel.where_unique(
            self.__ip,
            self.__object_id,
            self.__location)

    def object_id(self, object_id):
        self.__object_id = object_id
        self.__fail2ban_model = Fail2BanModel.where_unique(
            self.__ip,
            self.__object_id,
            self.__location)

    def add_attempt(self, number=1):
        if self.__fail2ban_model is None:
            self.__fail2ban_model = Fail2BanModel()
            self.__fail2ban_model.ip = self.__ip
            self.__fail2ban_model.object_id = self.__object_id
            self.__fail2ban_model.location = self.__location
            self.__fail2ban_model.attempts = 0
        self.__fail2ban_model.add_attempt_or_ban(
            number,
            self.max_attempts,
            valid_for=self.ban_for)

    def clear(self, object_id, ip=None):
        if ip is None:
            ip = request.remote_addr
        Fail2BanModel.delete_where_unique(ip, object_id, self.__location)

    def is_banned(self):
        if self.__fail2ban_model is None:
            return False
        return self.__fail2ban_model.is_banned()
