import pytest
from project.app import create_app, db
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS

@pytest.fixture()
def app():
    app = create_app()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()