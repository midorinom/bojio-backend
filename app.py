import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)

if app.debug == False:
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

app.config['SECRET_KEY'] = 'not really secret'
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
session = Session(app)
CORS(app, supports_credentials=True)

from controllers import demo_controller, user_controller, event_controller
from models import user_model, demo_model, event_model, event_invitation_model

# Creates DB tables based on models created in models folder, only if they don't exists
with app.app_context():
    session.app.session_interface.db.create_all()
