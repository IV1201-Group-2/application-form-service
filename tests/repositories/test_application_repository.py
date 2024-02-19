from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.repositories.application_repository import \
    get_application_status_from_db, insert_application_in_db
from tests.utilities.test_utilities import add_application_status_for_user_1, \
    generate_application_status, \
    generate_availabilities, generate_competences, \
    remove_application_components_from_db, remove_competences_from_db


def test_insert_application_in_db_success(app_with_client):
    app, _ = app_with_client
    competences = generate_competences()
    availabilities = generate_availabilities()
    application_status = generate_application_status()

    with app.app_context():
        insert_application_in_db(
                competences, availabilities, application_status)

        inserted_competences = CompetenceProfile.query.all()
        assert inserted_competences[0].person_id == 1
        assert inserted_competences[0].competence_id == 1
        assert inserted_competences[0].years_of_experience == 5
        assert inserted_competences[1].person_id == 1
        assert inserted_competences[1].competence_id == 2
        assert inserted_competences[1].years_of_experience == 3

        inserted_availabilities = Availability.query.all()
        assert inserted_availabilities[0].person_id == 1
        assert inserted_availabilities[0].from_date.strftime(
                '%Y-%m-%d') == '2021-01-01'
        assert inserted_availabilities[0].to_date.strftime(
                '%Y-%m-%d') == '2021-01-02'
        assert inserted_availabilities[1].person_id == 1
        assert inserted_availabilities[1].from_date.strftime(
                '%Y-%m-%d') == '2021-01-03'
        assert inserted_availabilities[1].to_date.strftime(
                '%Y-%m-%d') == '2021-01-04'

        inserted_application_status = ApplicationStatus.query.all()
        assert inserted_application_status[0].person_id == 1
        assert inserted_application_status[0].status == 'UNHANDLED'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_insert_competences_in_db_failure(app_with_client):
    app, _ = app_with_client
    competences = generate_competences()
    availabilities = generate_availabilities()
    application_status = generate_application_status()

    with patch('app.extensions.database.session.add',
               side_effect=SQLAlchemyError) as mock:
        with app.app_context():
            with pytest.raises(SQLAlchemyError):
                mock.add.side_effect = SQLAlchemyError()
                insert_application_in_db(
                        competences, availabilities, application_status)

            CompetenceProfile.query.all()
            assert len(CompetenceProfile.query.all()) == 0

            Availability.query.all()
            assert len(Availability.query.all()) == 0

            ApplicationStatus.query.all()
            assert len(ApplicationStatus.query.all()) == 0

    remove_application_components_from_db(app)


def test_get_application_status_from_db_success(app_with_client):
    app, _ = app_with_client
    person_id = 1

    add_application_status_for_user_1(app)

    with app.app_context():
        application_status = get_application_status_from_db(person_id)
        assert application_status.person_id == 1
        assert application_status.status == 'UNHANDLED'

    remove_application_components_from_db(app)


def test_get_application_status_from_db_error(app_with_client):
    app, _ = app_with_client
    person_id = 1

    with app.app_context():
        with patch('app.models.application.ApplicationStatus.query',
                   side_effect=SQLAlchemyError) as mock:
            with pytest.raises(SQLAlchemyError) as exception_info:
                mock.filter_by.return_value.first.side_effect = SQLAlchemyError
                get_application_status_from_db(person_id)

            assert isinstance(exception_info.value, SQLAlchemyError)
            mock.filter_by.return_value.first.assert_called_once()
            mock.filter_by.assert_called_once_with(person_id=person_id)
