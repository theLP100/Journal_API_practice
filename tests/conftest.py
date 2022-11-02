
import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.journal import Journal

@pytest.fixture
def app():
    app = create_app({"TESTING" : True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

#we'll make a fixture that populates the db with two journals for testing.
@pytest.fixture
def two_saved_journals(app):
    #arrange
    tree_journal = Journal(design = "tree of life")
    dragon_journal = Journal(design = "dragon")
    db.session.add_all([tree_journal, dragon_journal])
    db.session.commit()