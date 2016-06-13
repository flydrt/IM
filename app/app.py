from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO

app = Flask(__name__)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'hello'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bs:bs123456@localhost/bsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

socketio = SocketIO(app)

import models
import views
import events