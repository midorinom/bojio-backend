from datetime import date
from flask import render_template, request, redirect, url_for, session
from app import app, db
import re 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.user_model import User

# Create a SQLAlchemy engine to connect to your MySQL database



@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Create a session
        
        
        # Execute a query and retrieve results as dictionaries
        query = text('SELECT * FROM users WHERE username = :username AND password = :password')
        result = db.session.execute(query, {"username": username, "password": password})
        
        # Fetch the results as dictionaries
        users = result.fetchone()
        
        # Close the session
        db.session.close()

        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['username'] = users['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password!'
    return render_template('login.html', msg=msg)
 

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

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
