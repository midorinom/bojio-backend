from datetime import date
from flask import render_template, request, redirect, url_for, session
from app import app, db
import re 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.user_model import User
from flask import session, redirect, url_for
# Create a SQLAlchemy engine to connect to your MySQL database



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
