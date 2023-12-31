from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app import db
from dataclasses import dataclass
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import session
from .event_attendance_table import event_attendance

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    user_id:int = db.Column(db.Integer, primary_key=True)
    username:str = db.Column(db.String(200), unique=True, nullable=False)
    email:str = db.Column(db.String(200), unique=True, nullable=False)
    password:str = db.Column(db.String(200), nullable=False)
    registration_date:DateTime = db.Column(db.DateTime, default=func.now(), nullable=False)
    events_as_attendee = db.relationship('Event', secondary = event_attendance, backref = 'attendees')
    events_as_host = db.relationship('Event', backref = 'host')
    invitations_as_invitee = db.relationship('EventInvitation', foreign_keys = 'EventInvitation.invitee_id', backref = 'invitee')
    invitations_as_inviter = db.relationship('EventInvitation', foreign_keys = 'EventInvitation.inviter_id', backref = 'inviter')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}', registration_date='{self.registration_date}')>"

    @classmethod
    def change_password(cls, user_id, new_password):
        user = cls.query.get(user_id)
        if user:
            hashed_password = generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            
    @classmethod
    def create_user(cls, username, email, password):
        hashed_password = generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(cls, user_id, new_username, new_email):
        user = cls.query.get(user_id)
        if user:
            user.username = new_username
            user.email = new_email
            db.session.commit()  # Make sure to commit the changes

    @classmethod
    def delete_user(cls, user_id):
        user = cls.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

    @classmethod
    def login_user(cls, username, password):
        try:
            user = cls.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                return user
            else:
                return None
        except Exception as e:
            return None

    @classmethod
    def logout_user(cls):
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')

    @classmethod
    def display_profile(cls, user_id):
        user = cls.query.get(user_id)
        return user if user else None
    
    @classmethod
    def get_user(cls, id):
        return cls.query.get(id)
