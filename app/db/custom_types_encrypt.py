'''
import base64
import datetime
import json
import os
import warnings

from sqlalchemy.types import LargeBinary, String, TypeDecorator

from sqlalchemy_utils.exceptions import ImproperlyConfigured
from sqlalchemy_utils.types.encrypted.padding import PADDING_MECHANISM
from sqlalchemy_utils.types.json import JSONType
from sqlalchemy_utils.types.scalar_coercible import ScalarCoercible

cryptography = None
try:
    import cryptography
    from cryptography.exceptions import InvalidTag
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers import (
        algorithms,
        Cipher,
        modes
    )
except ImportError:
    pass

dateutil = None
try:
    import dateutil
    from dateutil.parser import parse as datetime_parse
except ImportError:
    pass


class StringEncryptedType(TypeDecorator, ScalarCoercible):
    """
    EncryptedType provides a way to encrypt and decrypt values,
    to and from databases, that their type is a basic SQLAlchemy type.
    For example Unicode, String or even Boolean.
    On the way in, the value is encrypted and on the way out the stored value
    is decrypted.

    EncryptedType needs Cryptography_ library in order to work.

    When declaring a column which will be of type EncryptedType
    it is better to be as precise as possible and follow the pattern
    below.

    .. _Cryptography: https://cryptography.io/en/latest/

    ::


        a_column = sa.Column(EncryptedType(sa.Unicode,
                                           secret_key,
                                           FernetEngine))

        another_column = sa.Column(EncryptedType(sa.Unicode,
                                           secret_key,
                                           AesEngine,
                                           'pkcs5'))


    A more complete example is given below.

    ::


        import sqlalchemy as sa
        from sqlalchemy import create_engine
        try:
            from sqlalchemy.orm import declarative_base
        except ImportError:
            # sqlalchemy 1.3
            from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker

        from sqlalchemy_utils import EncryptedType
        from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

        secret_key = 'secretkey1234'
        # setup
        engine = create_engine('sqlite:///:memory:')
        connection = engine.connect()
        Base = declarative_base()


        class User(Base):
            __tablename__ = "user"
            id = sa.Column(sa.Integer, primary_key=True)
            username = sa.Column(EncryptedType(sa.Unicode,
                                               secret_key,
                                               AesEngine,
                                               'pkcs5'))
            access_token = sa.Column(EncryptedType(sa.String,
                                                   secret_key,
                                                   AesEngine,
                                                   'pkcs5'))
            is_active = sa.Column(EncryptedType(sa.Boolean,
                                                secret_key,
                                                AesEngine,
                                                'zeroes'))
            number_of_accounts = sa.Column(EncryptedType(sa.Integer,
                                                         secret_key,
                                                         AesEngine,
                                                         'oneandzeroes'))


        sa.orm.configure_mappers()
        Base.metadata.create_all(connection)

        # create a configured "Session" class
        Session = sessionmaker(bind=connection)

        # create a Session
        session = Session()

        # example
        user_name = 'secret_user'
        test_token = 'atesttoken'
        active = True
        num_of_accounts = 2

        user = User(username=user_name, access_token=test_token,
                    is_active=active, number_of_accounts=num_of_accounts)
        session.add(user)
        session.commit()

        user_id = user.id

        session.expunge_all()

        user_instance = session.query(User).get(user_id)

        print('id: {}'.format(user_instance.id))
        print('username: {}'.format(user_instance.username))
        print('token: {}'.format(user_instance.access_token))
        print('active: {}'.format(user_instance.is_active))
        print('accounts: {}'.format(user_instance.number_of_accounts))

        # teardown
        session.close_all()
        Base.metadata.drop_all(connection)
        connection.close()
        engine.dispose()

    The key parameter accepts a callable to allow for the key to change
    per-row instead of being fixed for the whole table.

    ::


        def get_key():
            return 'dynamic-key'

        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            username = sa.Column(EncryptedType(
                sa.Unicode, get_key))

    """
    impl = String
    cache_ok = True

    def __init__(
        self,
        type_in=None,
        key=None,
        engine=None,
        padding=None,
        **kwargs
    ):
        """Initialization."""
        if not cryptography:
            raise ImproperlyConfigured(
                "'cryptography' is required to use EncryptedType"
            )
        super().__init__(**kwargs)
        # set the underlying type
        if type_in is None:
            type_in = String()
        elif isinstance(type_in, type):
            type_in = type_in()
        self.underlying_type = type_in
        self._key = key
        if not engine:
            engine = AesEngine
        self.engine = engine()
        if isinstance(self.engine, AesEngine):
            self.engine._set_padding_mechanism(padding)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    def _update_key(self):
        key = self._key() if callable(self._key) else self._key
        self.engine._update_key(key)

    def process_bind_param(self, value, dialect):
        """Encrypt a value on the way in."""
        if value is not None:
            self._update_key()

            try:
                value = self.underlying_type.process_bind_param(
                    value, dialect
                )

            except AttributeError:
                # Doesn't have 'process_bind_param'

                # Handle 'boolean' and 'dates'
                type_ = self.underlying_type.python_type
                if issubclass(type_, bool):
                    value = 'true' if value else 'false'

                elif issubclass(type_, (datetime.date, datetime.time)):
                    value = value.isoformat()

                elif issubclass(type_, JSONType):
                    value = json.dumps(value)

            return self.engine.encrypt(value)

    def process_result_value(self, value, dialect):
        """Decrypt value on the way out."""
        if value is not None:
            self._update_key()
            decrypted_value = self.engine.decrypt(value)

            try:
                return self.underlying_type.process_result_value(
                    decrypted_value, dialect
                )

            except AttributeError:
                # Doesn't have 'process_result_value'

                # Handle 'boolean' and 'dates'
                type_ = self.underlying_type.python_type
                date_types = [datetime.datetime, datetime.time, datetime.date]

                if issubclass(type_, bool):
                    return decrypted_value == 'true'

                elif type_ in date_types:
                    return DatetimeHandler.process_value(
                        decrypted_value, type_
                    )

                elif issubclass(type_, JSONType):
                    return json.loads(decrypted_value)

                # Handle all others
                return self.underlying_type.python_type(decrypted_value)

    def _coerce(self, value):
        if isinstance(self.underlying_type, ScalarCoercible):
            return self.underlying_type._coerce(value)

        return value

'''
