# import auth
# import events

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/bojio_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

from controllers import demo_controller

if __name__ == "__main__":
    # Creates DB tables based on models created in models folder, only if they don't exists
    with app.app_context():
        db.create_all()
    app.run(port=8000, debug=True)
