from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    nickname = db.Column(db.String(32))
    gender = db.Column(db.Boolean)
    birthday = db.Column(db.Date)
    signature = db.Column(db.Text)
    introduction = db.Column(db.Text)
    hometown = db.Column(db.String(64))
    contact_email = db.Column(db.String(64))
    telephone = db.Column(db.String(32))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))