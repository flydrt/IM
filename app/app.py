from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField

# basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hello'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bs:bs123456@localhost/bsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
import models

@app.route('/', methods=['GET', 'POST'])
def index():
	form = AccoutForm()
	return render_template('index.html', form=form)

# @app.route('/')
# def register(username):
# 	return render_template('user.html', name=username)

class AccoutForm(Form):
	account = StringField('Input your account')
	password = StringField('Input your password')
	submit = SubmitField('Sign Up')

if __name__ == '__main__':
	app.run(debug=True)