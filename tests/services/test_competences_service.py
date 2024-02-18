from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.competences_service import fetch_competences
from tests.utilities.test_utilities import remove_competences_from_db, \
    setup_competences_in_db


def test_fetch_competences_success(app_with_client):
    app, _ = app_with_client
    setup_competences_in_db(app)
    with app.app_context():
        result = fetch_competences()
        assert result == [{'competence_id': 1, 'name': 'tester'},
                          {'competence_id': 2, 'name': 'developer'}]

    remove_competences_from_db(app)


def test_fetch_competences_no_result(app_with_client):
    app, _ = app_with_client
    with app.app_context():
        with pytest.raises(NoResultFound) as exception_info:
            fetch_competences()

        exception = exception_info.value
        assert isinstance(exception, NoResultFound)


@patch('app.services.competences_service.get_competences_from_db')
def test_fetch_competences_sqlalchemy_error(mock_fetch, app_with_client):
    app, _ = app_with_client

    mock_fetch.side_effect = SQLAlchemyError("DATABASE CONNECTION ERROR.")

    with app.app_context():
        with pytest.raises(SQLAlchemyError) as exception:
            fetch_competences()
        assert str(exception.value) == 'DATABASE CONNECTION ERROR.'
