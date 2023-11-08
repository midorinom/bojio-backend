from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app import db
from dataclasses import dataclass
from flask_bcrypt import generate_password_hash
from flask import session
from .event_attendance_table import event_attendance

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    user_id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(200), unique=True, nullable=False)
    email: str = db.Column(db.String(200), unique=True, nullable=False)
    password: str = db.Column(db.String(200), nullable=False)
    registration_date: DateTime = db.Column(db.DateTime, default=func.now(), nullable=False)

    #Column to set for Business Account
    isBusinessAcc: Boolean = db.Column(db.Boolean, default=False) 

    #Column for Business Account
    company_name: str = db.Column(db.String(200))
    work_experience: String = db.Column(db.String(200))

    events_as_attendee = db.relationship('Event', secondary=event_attendance, backref='attendees')
    events_as_host = db.relationship('Event', backref='host')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}', registration_date='{self.registration_date}')>"

    @classmethod
    def create_user(cls, username, email, password, is_business=False, company_name=None, work_experience=None):
        hashed_password = generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email, password=hashed_password, isBusinessAcc=is_business, company_name=company_name, work_experience=work_experience)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(cls, user_id, new_username, new_email):
        user = cls.query.get(user_id)
        if user:
            user.username = new_username
            user.email = new_email
            db.session.commit()

    @classmethod
    def change_password(cls, user_id, new_password):
        user = cls.query.get(user_id)
        if user:
            hashed_password = generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            
    @classmethod
    def get_user(cls, user_id):
        return cls.query.get(user_id)
