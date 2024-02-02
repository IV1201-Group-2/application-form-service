import pytest
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from app.services.personal_info_service import fetch_personal_info


def test_fetch_personal_info_success(app_with_client):
    app, client = app_with_client
    with app.app_context():
        result = fetch_personal_info('test_user')
        assert result['username'] == 'test_user'
        assert result['surname'] == 'tester'


def test_fetch_personal_info_no_result(app_with_client):
    app, client = app_with_client
    with app.app_context():
        with pytest.raises(NoResultFound):
            fetch_personal_info('non_existent_user')


def test_fetch_personal_info_multiple_results(app_with_client):
    app, client = app_with_client
    with app.app_context():
        with pytest.raises(MultipleResultsFound):
            fetch_personal_info('duplicate_user')
