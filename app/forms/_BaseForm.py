from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired as _DataRequired, Length as _Length,
    Email as _Email
)

class DataRequired(_DataRequired):
    def __init__(self):
        super().__init__(message='Required field')

class Length(_Length):
    def __init__(self, min, max):
        super().__init__(
            min, max, f'The field must be between {min} and {max} characters.'
        )

class Email(_Email):
    def __init__(self):
        super().__init__(message='Wrong email address')

class _BaseForm(FlaskForm):
    def validate(self):
        is_valid = super().validate()
        self.translate_csrf_token_field_messages()
        return is_valid

    def translate_csrf_token_field_messages(self):
        csrf_token_field = self._fields.get('csrf_token')
        if csrf_token_field is None:
            return