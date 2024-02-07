from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.models.applicant.competence_profile import CompetenceProfile
from app.repositories.applicant.competences_repository import \
    insert_competences_in_db
from tests.utilities.test_utilities import remove_competences_from_db, \
    remove_test_user_from_db, setup_competences_in_db


def test_insert_competences_in_db_success(app_with_client):
    app, _ = app_with_client
    setup_competences_in_db(app)
    competence_profile = CompetenceProfile(competence_id=1, person_id=1,
                                           years_of_experience=5)

    with app.app_context():
        insert_competences_in_db(competence_profile)
        inserted_profile = CompetenceProfile.query.filter_by(
                person_id=1).first()
        assert inserted_profile is not None
        assert inserted_profile.years_of_experience == 5

    remove_test_user_from_db(app)
    remove_competences_from_db(app)


def test_insert_competences_in_db_failure(app_with_client):
    app, _ = app_with_client
    setup_competences_in_db(app)
    competence_profile = CompetenceProfile(competence_id=1, person_id=1,
                                           years_of_experience=5)

    with patch('app.extensions.database.session.add',
               side_effect=SQLAlchemyError) as mock:
        with app.app_context():
            with pytest.raises(SQLAlchemyError,
                               match='COULD NOT PERSIST COMPETENCE PROFILE'):
                insert_competences_in_db(competence_profile)

    mock.assert_called_once()
    remove_competences_from_db(app)
