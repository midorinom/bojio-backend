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


from controllers import demo_controller
from models import user_model, demo_model

# Creates DB tables based on models created in models folder, only if they don't exists
with app.app_context():
    db.create_all()
