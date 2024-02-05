from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.repositories.competences_repository import get_competences_from_db
from tests.utilities.test_utilities import remove_competences_from_db, \
    setup_competences_in_db


def test_get_competences_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_competences_in_db(app)
    with app.app_context():
        competences = get_competences_from_db()
        assert competences[0].competence_id == 1
        assert competences[0].name == 'tester'
        assert competences[1].competence_id == 2
        assert competences[1].name == 'developer'


def test_get_competences_from_db_no_result(app_with_client):
    app, _ = app_with_client
    remove_competences_from_db(app)
    with app.app_context():
        with pytest.raises(NoResultFound) as exception_info:
            get_competences_from_db()
        exception = exception_info.value
        assert isinstance(exception, NoResultFound)
        assert str(exception) == "NO COMPETENCES FOUND"


def test_get_person_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with patch('app.models.competence.Competence.query') as mock_query:
            mock_query.all.side_effect = SQLAlchemyError(
                    "A database error occurred")
            with pytest.raises(SQLAlchemyError) as exception_info:
                get_competences_from_db()
            exception = exception_info.value
            assert str(exception) == "COULD NOT FETCH COMPETENCES"
