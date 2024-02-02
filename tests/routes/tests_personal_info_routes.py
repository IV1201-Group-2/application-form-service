from unittest.mock import patch

from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError


def test_get_personal_info_success(app_with_client):
    app, test_client = app_with_client
    with app.app_context():
        token = create_access_token(identity="test_user")
    response = test_client.get('/recruitment/personal_info/get',
                               headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'surname' in response.json
    assert response.json['surname'] == 'tester'


def test_get_personal_info_no_result(app_with_client):
    app, test_client = app_with_client
    with app.app_context():
        token = create_access_token(identity="non_existing_user")
    response = test_client.get('/recruitment/personal_info/get',
                               headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'No user found with username non_existing_user.'


def test_get_personal_info_multiple_results(app_with_client):
    app, test_client = app_with_client
    with app.app_context():
        token = create_access_token(identity="duplicate_user")
    response = test_client.get('/recruitment/personal_info/get',
                               headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 409


def test_get_personal_info_sqlalchemy_error(app_with_client):
    app, test_client = app_with_client
    with app.app_context():
        token = create_access_token(identity="test_user")

    with patch('app.routes.personal_info_routes.fetch_personal_info') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

        response = test_client.get('/recruitment/personal_info/get',
                                   headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 500, ("Expected status code 500, "
                                             "but got {}").format(response.status_code)
        assert 'error' in response.json, "Expected error message in response"
        assert response.json['error'] == 'A database error occurred'
