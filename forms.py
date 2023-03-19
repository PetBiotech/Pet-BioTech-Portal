from flask_wtf import Form
from flask_security.forms import (
    LoginForm, RegisterForm,
    unique_user_email, email_required, email_validator
)
from wtforms import (
    StringField, PasswordField, BooleanField,
    SubmitField
)

from wtforms.validators import (
    InputRequired
)


_default_field_labels = {
    'username_login': 'Username or Email',
    'username_register': 'Username/Login',
    'password': 'Password',
    'login': 'Log in',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'E-mail',
    'password': 'Password',
    'password_repeat': 'Repeat the new password',
    'submit_register': 'Register'
}

def get_form_field_label(key):
    return _default_field_labels.get(key, '')

class ExtendedLoginForm(LoginForm):
    email = StringField(
        get_form_field_label('username_login'),
        [InputRequired()]
    )
    password = PasswordField(
        get_form_field_label('password'),
        [InputRequired()]
    )

    submit = SubmitField(
        get_form_field_label('login'),
    )

