import logging
from flask import g
from forms import RegistrationForm
from models import User

class UserRepository():
    @staticmethod
    def registration(form: RegistrationForm):
        try:
            user = User(**form.get_fields())
            user.is_active = True
            g.db_session.add(user)
            g.db_session.commit()
            return True
        except Exception:
            logging.getLogger().exception(
                f'Error while creating a new user with an email address: '
                f'{form.email.data}'
            )
            g.db_session.rollback()
            return False