# import auth
# import events

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from controllers import demo_controller
from models import user_model,demo_model

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:j1a2c3k4@localhost/bojio_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:Password1234@bojio-db.c3tfalfhp9o3.ap-southeast-1.rds.amazonaws.com/bojio-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

if __name__ == "__main__":
    # Creates DB tables based on models created in models folder, only if they don't exists
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)
