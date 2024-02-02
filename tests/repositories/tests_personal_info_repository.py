from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound

from app.repositories.personal_info_repository import get_person_from_db


def test_get_person_from_db_success(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        person = get_person_from_db('test_user')
        assert person.username == 'test_user'
        assert person.surname == 'tester'


def test_get_person_from_db_no_result(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with pytest.raises(NoResultFound) as e:
            get_person_from_db('non_existing_user')
        assert str(e.value) == 'No user found with username non_existing_user.'


def test_get_person_from_db_multiple_results(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with pytest.raises(MultipleResultsFound) as e:
            get_person_from_db('duplicate_user')
        assert str(e.value) == 'Multiple users found with username duplicate_user.'


def test_get_person_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with patch('app.models.person.Person.query') as mock_query:
            mock_query.filter_by.side_effect = SQLAlchemyError(
                "A database error occurred")
            with pytest.raises(SQLAlchemyError) as e:
                get_person_from_db('test_user')
            assert str(e.value) == 'Error retrieving user from the database.'
