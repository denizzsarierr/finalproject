from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):

    id = db.Column(db.Integer,primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone = True),default=func.now())    
    #timezone allowing us to deal with different timezones
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #ONE-TO-MANY RELATIONSHIP BETWEEN USER AND NOTES




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    email = db.Column(db.String(150),unique = True)
    username = db.Column(db.String(16),unique = True)
    #unique --> No user can have same email
    password = db.Column(db.String(20))
    notes = db.relationship('Note',backref='owner')

