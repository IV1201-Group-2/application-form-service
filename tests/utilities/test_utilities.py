import datetime

from flask_jwt_extended import create_access_token

from app.extensions import database
from app.models.competence import Competence
from app.models.person import Person


def setup_test_user_in_db(app):
    with app.app_context():
        database.session.add(Person(name='test', surname='tester', role_id=2))
        database.session.commit()


def remove_test_user_from_db(app):
    with app.app_context():
        database.session.query(Person).filter(Person.person_id == 1).delete()
        database.session.commit()


def generate_token_for_user_id_1(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity={'id': 1},
                                   expires_delta=datetime.timedelta(days=1))


def setup_competences_in_db(app):
    with app.app_context():
        database.session.add(Competence(name='tester'))
        database.session.add(Competence(name='developer'))
        database.session.commit()


def remove_competences_from_db(app):
    with app.app_context():
        database.session.query(Competence).delete()
        database.session.commit()
