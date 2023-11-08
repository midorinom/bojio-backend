from flask import session
from models.user_model import User
from flask_bcrypt import check_password_hash

class UserFactory:
    @classmethod
    def create_user(cls, username, email, password, is_business=False, company_name=None, work_experience=None):
        if is_business:
            return cls.create_business_account(username, email, password, company_name, work_experience)
        else:
            return cls.create_normal_account(username, email, password)

    @classmethod
    def create_business_account(cls, username, email, password, company_name, work_experience):
        if not company_name or not work_experience:
            raise ValueError("Both company_name and work_experience are required for a business account")

        return User.create_user(username, email, password, is_business=True, company_name=company_name, work_experience=work_experience)

    @classmethod
    def create_normal_account(cls, username, email, password):
        return User.create_user(username, email, password, is_business=False)

    @classmethod
    def login_user(cls, username, password):
        user = User.query.filter_by(username=username).first()  # Use User.query here
        if user and check_password_hash(user.password, password):
            return user
        return None

    @classmethod
    def logout_user(cls):
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')

    @classmethod
    def display_profile(cls, user_id):
        user = User.get_user(user_id)  # Use the User model for querying
        return user if user else None

    @classmethod
    def get_user(cls, id):
        return User.get_user(id)
    
    @classmethod
    def update_profile(cls, user_id, new_username, new_email):
        user = User.get_user(user_id)
        if user:
            user.update_user(user_id, new_username, new_email)
            return True  # Return True to indicate success
        return False  # Return False to indicate failure
