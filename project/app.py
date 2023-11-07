from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from project.extensions import db
from project.controllers.demo_controller import main
from project.controllers.event_controller import main_event
from project.controllers.user_controller import main_user
from project.config import isTest

app = Flask(__name__)

def create_app():
    return app

if isTest:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
elif app.debug == False:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password1234@bojio-db.c3tfalfhp9o3.ap-southeast-1.rds.amazonaws.com/bojio-db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bojio_db'

app.config['SECRET_KEY'] = 'not really secret'
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True

db.init_app(app)

#db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
session = Session(app)
CORS(app, supports_credentials=True)

app.register_blueprint(main)
app.register_blueprint(main_event)
app.register_blueprint(main_user)
#from controllers import user_controller, event_controller
from project.models import  demo_model, user_model, event_model, event_invitation_model

# Creates DB tables based on models created in models folder, only if they don't exists
with app.app_context():
    session.app.session_interface.db.create_all()