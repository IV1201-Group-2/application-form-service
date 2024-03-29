import datetime as dt
from datetime import datetime

from flask_jwt_extended import create_access_token

from app.extensions import database
from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence import Competence
from app.models.competence_profile import CompetenceProfile


def generate_token_for_person_id_1(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 1, 'role': 2},
                                   expires_delta=dt.timedelta(days=1))


def generate_token_for_recruiter(app) -> tuple[str, str]:
    with app.app_context():
        return create_access_token(identity=None,
                                   additional_claims={'id': 1, 'role': 1},
                                   expires_delta=dt.timedelta(days=1))


def setup_competences_in_db(app):
    with app.app_context():
        database.session.add(Competence(i18n_key='tester'))
        database.session.add(Competence(i18n_key='developer'))
        database.session.commit()


def remove_competences_from_db(app):
    with app.app_context():
        database.session.query(Competence).delete()
        database.session.commit()


def generate_competences() -> list[CompetenceProfile]:
    return [
        CompetenceProfile(competence_id=1, person_id=1, years_of_experience=5),
        CompetenceProfile(competence_id=2, person_id=1, years_of_experience=3)]


def generate_availabilities() -> list[Availability]:
    return [
        Availability(person_id=1,
                     from_date=datetime.strptime('2021-01-01', '%Y-%m-%d'),
                     to_date=datetime.strptime('2021-01-02', '%Y-%m-%d')),
        Availability(person_id=1,
                     from_date=datetime.strptime('2021-01-03', '%Y-%m-%d'),
                     to_date=datetime.strptime('2021-01-04', '%Y-%m-%d'))]


def generate_application_status() -> ApplicationStatus:
    return ApplicationStatus(person_id=1)


def remove_application_components_from_db(app):
    with app.app_context():
        ApplicationStatus.query.delete()
        Availability.query.delete()
        CompetenceProfile.query.delete()
        database.session.commit()


def application_route_post_request(test_client, token, payload):
    return test_client.post('/api/application-form/submit/',
                            headers={'Authorization': f'Bearer {token}'},
                            json=payload)


def add_application_status_for_user_1(app):
    with app.app_context():
        database.session.add(ApplicationStatus(person_id=1))
        database.session.commit()
