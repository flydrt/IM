from flask_wtf import Form
from wtforms import StringField, SubmitField


class AccoutForm(Form):
    account = StringField('Input your account')
    password = StringField('Input your password')
    submit = SubmitField('Sign Up')