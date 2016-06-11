from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(30))
    email = db.Column(db.String(40), unique=True)
    nickname = db.Column(db.String(20))
    gender = db.Column(db.Boolean)
    birthday = db.Column(db.Date)
    signature = db.Column(db.Text)
    introduction = db.Column(db.Text)
    hometown = db.Column(db.String(50))
    contact_email = db.Column(db.String(40))
    telephone = db.Column(db.String(20))