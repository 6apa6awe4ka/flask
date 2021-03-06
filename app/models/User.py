import datetime
import bcrypt
from sqlalchemy import Column, Unicode, Integer, Boolean, ForeignKey, Enum, \
    DateTime
from sqlalchemy.sql import expression
from models import _Base


class User(_Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(Unicode(length=30))
    email = Column(Unicode(length=40), unique=True, nullable=False)
    _password = Column('password', Unicode(length=60))
    is_active = Column(
        Boolean, server_default=expression.false(), default=False,
        nullable=False
    )
    reg_date = Column(DateTime(), default=datetime.datetime.now())

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password: str):
        self._password = self.generate_password(raw_password)

    @staticmethod
    def generate_password(raw_password: str):
        return bcrypt.hashpw(raw_password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, inp_passwd: str):
        return bcrypt.checkpw(inp_passwd.encode(), self.password.encode())

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)