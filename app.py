import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if app.debug == False:
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)
CORS(app)

app.secret_key = 'bojio'
from controllers import demo_controller, user_controller, event_controller
from models import user_model, demo_model, event_model

# Creates DB tables based on models created in models folder, only if they don't exists
with app.app_context():
    db.create_all()
