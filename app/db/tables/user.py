from tokenize import String
from xmlrpc.client import Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref, validates

from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from app.core.config import settings
from app.db.utilities import email_pattern
from app.db.tables.base import TableBase


class User(SQLAlchemyBaseUserTableUUID, TableBase):
    '''See SQLAlchemy Relationship Loading Techniques:
    - https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html
    '''
    __tablename__           = 'user'
    items                   = relationship('Item', backref=backref('user', lazy='noload'))
    clients                 = relationship('Client', secondary='user_client', backref=backref('users', lazy='noload'))

    @validates('email')
    def validate_email(self, k, v):
        assert isinstance(v, str)
        # match regex pattern
        if not email_pattern.fullmatch(v):
            raise ValueError('Invalid characters in the username/email')
        # username in email provider list
        if settings.EMAIL_PROVIDER_RESTRICTION:
            if not any( provider in v for provider in settings.ALLOWED_EMAIL_PROVIDER_LIST ):
                raise ValueError('Invalid email provider')
        return v

    def __repr__(self):
        repr_str = f'User({self.email} created on {self.created_on} [{self.id}])'
        return repr_str

