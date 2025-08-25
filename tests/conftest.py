# tests/conftest.py
import pytest
from app import create_app
from app.extensions import db
from app.config import TestingConfig

@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        yield app

@pytest.fixture(scope="function", autouse=True)
def db_session(app):
    db.drop_all()
    db.create_all()
    yield db.session
    db.session.rollback()
    db.drop_all()
