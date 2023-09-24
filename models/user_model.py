from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app import db
from dataclasses import dataclass
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import session

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    user_id:int = db.Column(db.Integer, primary_key=True)
    username:str = db.Column(db.String(200), unique=True, nullable=False)
    email:str = db.Column(db.String(200), unique=True, nullable=False)
    password:str = db.Column(db.String(200), nullable=False)
    registration_date:DateTime = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}', email='{self.email}', registration_date='{self.registration_date}')>"


    @classmethod
    def create_user(cls, username, email, password):
        hashed_password = generate_password_hash(password).decode('utf-8')
        user = cls(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(user_id, new_username, new_email):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            user.username = new_username
            user.email = new_email
            db.session.commit()

    @classmethod
    def delete_user(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()   
    

    @classmethod
    def login_user(cls, username, password):
        try:
            # Find a user with the given username
            user = cls.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                # Password matches; return the user object
                return user
            else:
                # Invalid username or password; return None
                return None
        except Exception as e:
            # Handle exceptions (e.g., database connection issues)
            return None

        
    @classmethod
    def logout_user(cls):
        # Clear the user's session data
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
