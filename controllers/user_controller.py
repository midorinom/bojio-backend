from datetime import date
from flask import render_template, request, redirect, url_for, session
from app import app, db
import re 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.user_model import User
from flask import session, redirect, url_for

from service.user_factory import UserFactory
# Create a SQLAlchemy engine to connect to your MySQL database

@app.route('/change_password', methods=['POST'])
def change_password():
    
    data = request.get_json()
    user_id = session['id']
    new_password = data.get('password')

    if not new_password:
        return {
            "status": "error",
             "message": "Please provide a new password"
            }, 400

    user = UserFactory.display_profile(user_id)

    if not user:
        return {
            "status": "error",
            "message": "User not found"
            }, 404

    try:
        user.change_password(user_id,new_password)
        return {
            "status": "success",
            "message": "Password changed successfully"
        }, 200
    
    except Exception as e:
        return {
            "status": "error",
            "message": "Error changing the password. Please try again."
        }, 500
    
    
@app.route('/profile', methods=['GET'])
def display_profile():

    user_id = session['id']
    user = UserFactory.display_profile(user_id)  # Use the new method
    if user:
        return {
            "status": "success",
            "data": {
                "username": user.username,
                "email": user.email,
                "companyname":user.company_name,
                "workexperience":user.work_experience,

            }
        }, 200
    else:
        return {
            "status": "error",
            "message": "User not logged in"
        }, 401
    
    
@app.route('/updateprofile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = session.get('id')
    new_username = data.get('username')
    new_email = data.get('email')
    is_business = data.get('is_business')
    company_name = data.get('company_name')
    work_experience = data.get('work_experience')

    if not new_username or not new_email:
        return {
            "status": "error",
            "message": "Please provide a new username and email"
        }, 400

    user = UserFactory.display_profile(user_id)

    if not user:
        return {
            "status": "error",
            "message": "User not found or logged in"
        }, 404

    try:
        print(f"Updating user: {user_id}")
        print(f"New username: {new_username}")
        print(f"New email: {new_email}")

        if is_business:
            print(f"Updating as a business user")
            print(f"Company name: {company_name}")
            print(f"Work experience: {work_experience}")

            user.update_user(user_id, new_username, new_email, company_name, work_experience)
        else:
            print("Updating as a non-business user")

            user.update_user(user_id, new_username, new_email)

        print("Profile updated successfully")

        return {
            "status": "success",
            "message": "Profile updated successfully"
        }, 200
    except Exception as e:
        print(f"Error updating the profile: {e}")
        return {
            "status": "error",
            "message": "Error updating the profile. Please try again."
        }, 500

   
@app.route('/login', methods=['POST'])
def login():
    msg = ''
    
    if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password']

            # Use the login method to check if the user's credentials are valid
            user = UserFactory.login_user(username, password)

            if user:
                session['loggedin'] = True
                session['id'] = user.user_id
                session['username'] = user.username
                msg = 'Logged in successfully!'
                return {
                        "status": "success",
                        "message": msg,
                        "id": user.user_id
                    }, 200
                #return render_template('index.html', msg=msg)
            else:
                msg = 'Incorrect username or password!'
                return {
                        "status": "error",
                        "message": msg
                    }, 500
        #return render_template('login.html', msg=msg)
    return {
            "status": "error",
            "message": msg
        }, 400
    
@app.route('/logout', methods=['GET'])
def logout():
    UserFactory.logout_user()  # Call the logout method from your User model
    msg = 'Logout successfully!'
    return {
                        "status": "success",
                        "message": msg
                    }, 200
 
@app.route('/register', methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        is_business = data.get('is_business', False)  # Check if it's a Business Account
        company_name = data.get('company_name')
        work_experience = data.get('work_experience')

        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            # Attempt to create the user using the UserFactory
            try:
                if is_business:
                    user = UserFactory.create_business_account(username, email, password, company_name, work_experience)
                else:
                    user = UserFactory.create_normal_account(username, email, password)

                msg = 'You have successfully registered!'
                return {
                    "status": "success",
                    "message": msg
                }, 200
            except Exception as e:
                msg = 'Error creating the account. Please try again.'
                return {
                    "status": "error",
                    "message": msg
                }, 500

    # If any validation fails or there's an error, return an appropriate response
    return {
        "status": "error",
        "message": msg
    }, 400

@app.route('/get-session', methods=['GET'])
def get_session():

    user_id = session.get('id')
    
    if user_id:
        return {
            "status": "success",
            "data": True
        }, 200
    else:
        return {
            "status": "error",
            "message": "User not logged in"
        }, 401