import pytest
from project.app import create_app, db
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS

@pytest.fixture()
def app():
    app = create_app()
    
    # app.config['SESSION_SQLALCHEMY'] = db
    # session = Session(app)
    # CORS(app, supports_credentials=True)

    # # Creates DB tables based on models created in models folder, only if they don't exists
    # with app.app_context():
    #     session.app.session_interface.db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()