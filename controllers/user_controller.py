from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
from __main__ import app, db
import re 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Create a SQLAlchemy engine to connect to your MySQL database
engine = create_engine("mysql://username:password@hostname/database")

Session = sessionmaker(bind=engine)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Create a session
        session_db = Session()
        
        # Execute a query and retrieve results as dictionaries
        query = text('SELECT * FROM accounts WHERE username = :username AND password = :password')
        result = session_db.execute(query, {"username": username, "password": password})
        
        # Fetch the results as dictionaries
        account = result.fetchone()
        
        # Close the session
        session_db.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
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
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Get today's date
        today = date.today().strftime("%Y-%m-%d")

        # Create a session
        session_db = Session()

        # Check if the username already exists
        existing_user = session_db.execute("SELECT id FROM accounts WHERE username = :username", {"username": username}).fetchone()

        if existing_user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Insert the new user into the database with the registration date
            session_db.execute("INSERT INTO accounts (username, password, email, registration_date) VALUES (:username, :password, :email, :registration_date)",
                               {"username": username, "password": password, "email": email, "registration_date": today})
            session_db.commit()
            msg = 'You have successfully registered!'

        # Close the session
        session_db.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)