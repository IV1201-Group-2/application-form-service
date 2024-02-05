from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.personal_info_service import fetch_personal_info
from tests.utilities.test_utilities import remove_test_user_from_db, \
    setup_test_user_in_db


def test_fetch_personal_info_success(app_with_client):
    app, _ = app_with_client
    setup_test_user_in_db(app)
    with app.app_context():
        result = fetch_personal_info(1)
        assert result['name'] == 'test'
        assert result['surname'] == 'tester'


def test_fetch_personal_info_no_result(app_with_client):
    app, _ = app_with_client
    remove_test_user_from_db(app)
    with app.app_context():
        with pytest.raises(NoResultFound) as exception:
            fetch_personal_info(2)
        assert str(exception.value) == 'USER NOT FOUND: 2.'


def test_fetch_personal_info_sqlalchemy_error(app_with_client):
    app, _ = app_with_client

    with patch(
            'app.services.personal_info_service'
            '.get_person_from_db') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("DATABASE CONNECTION ERROR.")

        with app.app_context():
            with pytest.raises(SQLAlchemyError) as exception:
                fetch_personal_info(1)
            assert str(exception.value) == 'DATABASE CONNECTION ERROR.'
