from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    def __repr__(self):
        return self.username
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    face_prediksi = db.Column(db.Integer, default=0)
    absen = db.relationship('Absen', backref='author', lazy='dynamic')


@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))


# class Pesan(db.Model):
#     id = db.Column(db.Integer, primay_key=True)
#     user_id = db.C


class Absen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pertemuan = db.Column(db.String(64))
    materi = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Absen {self.pertemuan}'
