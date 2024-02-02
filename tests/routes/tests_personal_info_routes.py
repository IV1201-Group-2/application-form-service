import datetime
from unittest.mock import patch

from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError


def generate_valid_and_invalid_tokens(app_with_client) -> tuple[str, str]:
    app, test_client = app_with_client

    valid_token_data = {
        "id": 1,
        "iat": datetime.datetime(2023, 1, 1).timestamp(),
        "exp": datetime.datetime(2025, 1, 2).timestamp()
    }

    invalid_token_data = {
        "id": 2,
        "iat": datetime.datetime(2023, 1, 1).timestamp(),
        "exp": datetime.datetime(2025, 1, 2).timestamp()
    }

    with app.app_context():
        valid_token = create_access_token(identity=valid_token_data)
        invalid_token = create_access_token(identity=invalid_token_data)

    return valid_token, invalid_token


def test_get_personal_info_success(app_with_client):
    _, test_client = app_with_client
    valid_token, _ = generate_valid_and_invalid_tokens(app_with_client)

    response = test_client.get('/applicant/personal_info/',
                               headers={'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'test'
    assert response.json['surname'] == 'tester'
    assert response.json['role'] == 2


def test_get_personal_info_no_result(app_with_client):
    _, test_client = app_with_client
    _, invalid_token = generate_valid_and_invalid_tokens(app_with_client)

    response = test_client.get('/applicant/personal_info/',
                               headers={'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'USER_NOT_FOUND'
    assert response.json['details'] == 'User not found with id: 2'


def test_get_personal_info_sqlalchemy_error(app_with_client):
    _, test_client = app_with_client
    valid_token, _ = generate_valid_and_invalid_tokens(app_with_client)

    with patch('app.routes.personal_info_routes.fetch_personal_info') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

        response = test_client.get('/applicant/personal_info/',
                                   headers={'Authorization': f'Bearer {valid_token}'})

        assert response.status_code == 500
        assert response.json['error'] == 'COULD_NOT_FETCH_USER'
        assert response.json['details'] == 'Could not fetch user from database'
