
from flask_security.forms import (
    LoginForm, RegisterForm,
    unique_user_email, email_required, email_validator
)
from wtforms import (
    StringField, PasswordField, TextField, BooleanField,
    SubmitField, validators
)
from wtforms.validators import (
    InputRequired, Required
)


_default_field_labels = {
    'username_login': 'Username or Email',
    'username_register': 'Username/Login',
    'password': 'Password',
    'login': 'Log in',
    'first_name': 'First Name',
    'last_name': 'Last Name',
    'email': 'E-mail',
    'password': 'New Password',
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
##    remember = BooleanField(
##        get_form_field_label('remember_me'),
##    )
    submit = SubmitField(
        get_form_field_label('login'),
    )

##class ExtendedRegisterForm(RegisterForm):
##    username = StringField(
##        get_form_field_label('username_register'),
##        [InputRequired()]
##    )
##    first_name = TextField(
##        get_form_field_label('first_name'),
##        [Required()]
##    )
##    last_name = TextField(
##        get_form_field_label('last_name'),
##        [Required()]
##    )
##    email = StringField(
##        get_form_field_label('email'),
##        validators=[
##            validators.Length(
##                  min=6, max=255,
##                  message='Email must be between 6 and 255 characters'
##            ),
##            email_required, email_validator, unique_user_email
##        ]
##    )
##    password = PasswordField(
##        'New Password',
##        [
##            validators.DataRequired(),
##            validators.Length(
##                  min=6, max=50,
##                  message='Password must be between 6 and 50 characters'
##            ),
##            validators.EqualTo('password_confirm', message='Passwords are not the same')
##        ]
##    )
##    password_confirm = PasswordField(
##        'Repeat the new password'
##    )
##    submit = SubmitField(
##        get_form_field_label('submit_register')
##    )

