from datetime import date
from flask import render_template, request, redirect, url_for, session
from app import app, db
import re 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.user_model import User
from flask import session, redirect, url_for
# Create a SQLAlchemy engine to connect to your MySQL database


@app.route('/profile', methods=['GET'])
def display_profile():
    if 'loggedin' in session:
        user_id = session['id']
        user = User.display_profile(user_id)  # Use the new method
        if user:
            return {
                "status": "success",
                "data": user
            }, 200
        else:
            return {
                "status": "error",
                "message": "User not found"
            }, 404
    else:
        return {
            "status": "error",
            "message": "User not logged in"
        }, 401
    
@app.route('/profile', methods=['POST'])
def update_profile():
    if 'loggedin' in session:
        user_id = session['id']
        data = request.get_json()
        new_username = data.get('username')
        new_email = data.get('email')
        new_password = data.get('password')

        if not new_username or not new_email:
            return {
                "status": "error",
                "message": "Please provide a new username and email"
            }, 400

        user = User.display_profile(user_id)  # Use the new method
        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }, 404

        try:
            user.update_user(user_id, new_username, new_email)  # Pass user_id
            return {
                "status": "success",
                "message": "Profile updated successfully"
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": "Error updating the profile. Please try again."
            }, 500
    else:
        return {
            "status": "error",
            "message": "User not logged in"
        }, 401
   
@app.route('/login', methods=['POST'])
def login():
    msg = ''
    
    if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password']

            # Use the login method to check if the user's credentials are valid
            user = User.login_user(username, password)

            if user:
                session['loggedin'] = True
                session['id'] = user.user_id
                session['username'] = user.username
                msg = 'Logged in successfully!'
                return {
                        "status": "success",
                        "message": msg
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
    User.logout_user()  # Call the logout method from your User model
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

        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        else:
            # Attempt to create the user using the class method
            try:
                User.create_user(username=username, email=email, password=password)
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
