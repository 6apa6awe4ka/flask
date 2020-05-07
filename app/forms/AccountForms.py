from flask import g
from ._BaseForm import _BaseForm, DataRequired, Email, Length
from wtforms.fields import (StringField, PasswordField)
from models import User
from wtforms.validators import ValidationError

class LoginForm(_BaseForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        is_valid = super().validate()
        if not is_valid:
            return False

        return self._email(self.email) and self._password(self.password)

    def _email(self, field):
        self.user = g.db_session.query(User).filter_by(email=field.data).first()

        if not self.user:
            field.errors.append(
                'User with this email address is not registered'
            )
            return False

        if not self.user.is_active:
            field.errors.append(
                'Account is not activated, check your email for activation link'
            )
            return False

        return True

    def _password(self, field):
        if not self.user.check_password(field.data):
            field.errors.append('Invalid password entered')
            return False

        return True

class RegistrationForm(_BaseForm):
    nickname = StringField(
        'Nickname', validators=[DataRequired(), Length(min=3, max=30)]
    )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=10)]
    )
    password_verification = PasswordField(
        'Password confirmation',
        validators=[DataRequired(), Length(min=6, max=10)]
    )

    def validate_email(self, field):
        self.user = g.db_session.query(User).filter_by(email=field.data).first()

        if self.user:
            raise ValidationError(
                'The email address you have entered is already registered'
            )

        return True

    def validate_password(self, field):
        if self.password.data != self.password_verification.data:
            raise ValidationError('Passwords entered do not match')

    def get_fields(self):
        return {
            'nickname': self.nickname.data,
            'email': self.email.data,
            'password': self.password.data
        }

