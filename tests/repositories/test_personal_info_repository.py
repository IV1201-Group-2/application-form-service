from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.repositories.personal_info_repository import \
    get_person_from_db
from tests.utilities.test_utilities import remove_test_user_1_from_db, \
    setup_test_user_1_in_db


def test_get_person_from_db_success(app_with_client):
    app, _ = app_with_client
    setup_test_user_1_in_db(app)
    with app.app_context():
        person = get_person_from_db(1)
        assert person.name == 'test'
        assert person.surname == 'tester'

    remove_test_user_1_from_db(app)


def test_get_person_from_db_no_result(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with pytest.raises(NoResultFound) as exception_info:
            get_person_from_db(2)
        assert exception_info.type == NoResultFound


def test_get_person_from_db_sqlalchemy_error(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with patch('app.models.person.Person.query') as mock_query:
            mock_filter_by = mock_query.filter_by.return_value
            mock_filter_by.one.side_effect = SQLAlchemyError(
                    "A database error occurred")
            with pytest.raises(SQLAlchemyError) as exception_info:
                get_person_from_db(1)

        mock_query.filter_by.assert_called_once_with(person_id=1)
        assert exception_info.type == SQLAlchemyError
