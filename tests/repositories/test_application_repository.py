from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.repositories.application_repository import insert_application_in_db
from tests.utilities.test_utilities import generate_application_status, \
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
