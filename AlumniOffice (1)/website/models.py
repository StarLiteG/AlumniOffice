from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Visitor')  # Default role is Visitor

    def __repr__(self):
        return f'<User {self.username}>'

# Define roles
class Role:
    ADMIN = 'Administrative'
    REGISTERED_ALUMNI = 'Registered Alumni'
    APPLIED_ALUMNI = 'Applied Alumni'
    VISITOR = 'Visitor'

class AlumniProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('profile', uselist=False))
