"""
    Fail2Ban Model - NOT affiliated with https://github.com/fail2ban/fail2ban
"""

from sqlalchemy import Column, String, Integer
from ..classes.jwt import JWT
from .base_model import BaseModel


class Fail2BanModel(BaseModel):
    """ User db model """

    __tablename__ = 'evernode_fail2ban'
    location = Column(String(100))
    ip = Column(String(128))  # support IPv6
    attempts = Column(Integer, nullable=False, default=0)
    banned_token = Column(String(300))
    object_id = Column(Integer)
    json_exclude_list = []

    @classmethod
    def where_ip(cls, ip):
        """ Get db model by username """
        return cls.query.filter_by(ip=ip).first()

    @classmethod
    def where_unique(cls, ip, object_id, location):
        """ Get db model by username """
        return cls.query.filter_by(
            ip=ip,
            object_id=object_id,
            location=location).first()

    @classmethod
    def where_object_id(cls, object_id):
        """ Get db model by object id """
        return cls.query.filter_by(object_id=object_id).first()

    @classmethod
    def delete_where_unique(cls, ip, object_id, location):
        """ delete by ip and object id """
        result = cls.where_unique(ip, object_id, location)
        if result is None:
            return None
        result.delete()
        return True

    def generate_banned_token(self, valid_for):
        self.banned_token = JWT().create_token({}, valid_for)
        self.save()

    def is_banned(self) -> bool:
        if self.banned_token is None:
            return False
        banned_status = JWT().verify_token(self.banned_token)
        if banned_status:
            return True
        else:
            self.delete()
            return False

    def add_attempt_or_ban(self, number=1, max_attempts=3, valid_for=1800):
        if self.attempts >= max_attempts:
            if self.banned_token is not None:
                return
            self.generate_banned_token(valid_for=valid_for)
        else:
            self.attempts = self.attempts + number
        self.save()
        return
