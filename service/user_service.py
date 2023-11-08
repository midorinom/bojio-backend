import re
from models.user_model import User
from utilities.custom_exception_factory import CustomExceptionFactory
from flask import session

# Business logic related to user operations

def change_password(new_password):
    if 'loggedin' in session:
        user_id = session['id']
        user = User.display_profile(user_id)

        if not user:
            raise CustomExceptionFactory().create_exception('user_not_found')
        
        try:
            user.change_password(user_id, new_password)
            return "Password changed successfully"
        except Exception as e:
            raise CustomExceptionFactory().create_exception('password_change_error')

def display_profile():
    if 'loggedin' in session:
        user_id = session['id']
        user = User.display_profile(user_id)

        if user:
            return {
                "username": user.username,
                "email": user.email
            }
        else:
            raise CustomExceptionFactory().create_exception('user_not_found')
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def update_profile(new_username, new_email):
    if 'loggedin' in session:
        user_id = session['id']
        user = User.display_profile(user_id)

        if not user:
            raise CustomExceptionFactory().create_exception('user_not_found')

        try:
            user.update_user(user_id, new_username, new_email)
            return "Profile updated successfully"
        except Exception as e:
            raise CustomExceptionFactory().create_exception('profile_update_error')
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def login(username, password):
    try:
        user = User.login_user(username, password)

        if user:
            session['loggedin'] = True
            session['id'] = user.user_id
            session['username'] = user.username
            return user.user_id
        else:
            raise CustomExceptionFactory().create_exception('incorrect_credentials')
    except Exception as e:
        raise CustomExceptionFactory().create_exception('login_error')

def logout():
    if 'loggedin' in session:
        User.logout_user()
        return "Logout successfully"
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')

def register(username, password, email):
    if not username or not password or not email:
        raise CustomExceptionFactory().create_exception('incomplete_registration_data')
    elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        raise CustomExceptionFactory().create_exception('invalid_email')
    elif not re.match(r'[A-Za-z0-9]+', username):
        raise CustomExceptionFactory().create_exception('invalid_username')
    else:
        try:
            User.create_user(username, email, password)
            return "You have successfully registered"
        except Exception as e:
            raise CustomExceptionFactory().create_exception('registration_error')

def get_session():
    user_id = session.get('id')

    if user_id:
        return True
    else:
        raise CustomExceptionFactory().create_exception('user_not_logged_in')
