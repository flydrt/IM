from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from models import User


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "email"})
    username = StringField('Username', validators=[DataRequired(), Length(1, 32),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                          'Only letters, numbers or underscores!')],
                           render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Different passwords!')],
                             render_kw={"placeholder": "password"})
    password2 = PasswordField('Confirm password', validators=[DataRequired()], render_kw={"placeholder": "confirm password"})
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class ProfileForm(Form):
    signature = StringField('Signature')
    introduction = StringField('Introduction')
    submit = SubmitField('Save')


class SearchForm(Form):
    username = StringField('Enter username to search the contact',
                           validators=[DataRequired(), Length(1, 32),
                                       Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, 'Only letters, numbers or underscores!')],
                           render_kw={"placeholder": "username"})
    submit = SubmitField('Search')