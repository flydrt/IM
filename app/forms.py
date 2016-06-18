from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional
from wtforms import ValidationError
from models import User


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "email"})
    username = StringField('Username', validators=[DataRequired(), Length(6, 32),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                          'Only letters, numbers or underscores!')],
                           render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 32),
                                                     EqualTo('password2', message='Different passwords!')],
                             render_kw={"placeholder": "password"})
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(6, 32)],
                              render_kw={"placeholder": "confirm password"})
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class ProfileForm(Form):
    nickname = StringField('Nickname', validators=[Length(0, 32), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                                         'Only letters, numbers or underscores!'),
                                                   Optional()])
    gender = SelectField('Gender', choices=[('0', 'Unknown'), ('1', 'Male'), ('2', 'Female')])
    birthday = DateField('Birthday (Format: year-month-day, e.g. 2016-6-15)', validators=[Optional()])
    signature = StringField('Signature')
    introduction = StringField('Introduction')
    hometown = StringField('Hometown', validators=[Length(0, 64), Optional()])
    contact_email = StringField('Contact Email', validators=[Length(0, 64), Email(), Optional()])
    telephone = StringField('Telephone', validators=[Length(0, 32), Optional()])
    submit = SubmitField('Save')


class SearchForm(Form):
    username = StringField('Enter username to search the contact',
                           validators=[DataRequired(), Length(1, 32),
                                       Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, 'Only letters, numbers or underscores!')],
                           render_kw={"placeholder": "username"})
    submit = SubmitField('Search')


class ManageGroupForm(Form):
    group_name = StringField('Enter group name to manage the group',
                             validators=[DataRequired(), Length(1, 32),
                                         Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, 'Only letters, numbers or underscores!')],
                             render_kw={"placeholder": "group name"})
    manage = BooleanField('Not choose for add, choose for delete')
    submit = SubmitField('Manage')