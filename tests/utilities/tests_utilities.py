from app.extensions import database
from app.models.person import Person


def setup_test_user_in_db(app):
    with app.app_context():
        database.session.add(Person(name='test', surname='tester', role_id=2))
        database.session.commit()


def remove_test_user_from_db(app):
    with app.app_context():
        database.session.query(Person).filter(Person.person_id == 1).delete()
        database.session.commit()
