from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from app.services.application_service import already_applied, store_application
from tests.utilities.test_utilities import add_application_status_for_user_1, \
    generate_availabilities, \
    generate_competences, remove_application_components_from_db


def test_insert_application_in_db_success(app_with_client):
    app, client = app_with_client
    person_id = 1
    competences = generate_competences()
    availabilities = generate_availabilities()

    with app.app_context():
        application = store_application(person_id, competences, availabilities)

        assert application['status'] == 'Pending'
        assert len(application['competences']) == 2
        assert application['competences'][0]['competence_id'] == 1
        assert len(application['availabilities']) == 2
        assert application['availabilities'][0]['from_date'] == '2021-01-01'

    remove_application_components_from_db(app)


def test_already_applied_true(app_with_client):
    app, client = app_with_client
    person_id = 1

    with app.app_context():
        add_application_status_for_user_1(app)
        assert already_applied(person_id) is True

    remove_application_components_from_db(app)


def test_already_applied_false(app_with_client):
    app, client = app_with_client
    person_id = 1

    with app.app_context():
        assert already_applied(person_id) is False

    remove_application_components_from_db(app)


@patch('app.services.application_service.insert_application_in_db')
def test_insert_application_in_db_sqlalchemy_error(
        mock_insert, app_with_client):
    app, client = app_with_client
    person_id = 1
    competences = generate_competences()
    availabilities = generate_availabilities()

    mock_insert.side_effect = SQLAlchemyError
    with app.app_context():
        try:
            store_application(person_id, competences, availabilities)
            assert False
        except SQLAlchemyError:
            assert True

        assert mock_insert.called is True

    remove_application_components_from_db(app)
