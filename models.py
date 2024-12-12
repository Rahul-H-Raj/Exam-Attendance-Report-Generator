from flask_login import UserMixin
from __init__ import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Classroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    classroom_no = db.Column(db.String(50), nullable=False)
    seat_distribution = db.Column(db.Text, nullable=True)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    code = db.Column(db.String(50))
    semester = db.Column(db.Integer)
    classroom_no = db.Column(db.String(10))
    time = db.Column(db.String(20))