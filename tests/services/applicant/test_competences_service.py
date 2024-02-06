import pytest

from app.services.applicant.competences_service import \
    store_applicant_competences
from tests.utilities.test_utilities import remove_competences_from_db, \
    remove_test_user_from_db, setup_competences_in_db, setup_test_user_in_db


def test_store_applicant_competences_success(app_with_client):
    app, client = app_with_client
    setup_test_user_in_db(app)
    setup_competences_in_db(app)

    user_id = 1
    competence_id = 1
    experience = 5.0

    with app.app_context():
        result = store_applicant_competences(user_id, competence_id,
                                             experience)
        assert result == {
            'person_id': user_id,
            'competence_id': competence_id,
            'years_of_experience': experience
        }

    remove_test_user_from_db(app)
    remove_competences_from_db(app)


from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError


def test_store_applicant_competences_sqlalchemy_error(app_with_client):
    app, client = app_with_client
    setup_test_user_in_db(app)
    setup_competences_in_db(app)

    user_id = 1
    competence_id = 1
    experience = 5.0

    with patch(
            'app.services.applicant.competences_service'
            '.insert_competences_in_db') as mocked_insert:
        mocked_insert.side_effect = SQLAlchemyError(
                "DATABASE CONNECTION ERROR")

        with app.app_context():
            with pytest.raises(SQLAlchemyError) as exception:
                store_applicant_competences(user_id, competence_id, experience)

            assert str(exception.value) == 'DATABASE CONNECTION ERROR'

    remove_test_user_from_db(app)
    remove_competences_from_db(app)
