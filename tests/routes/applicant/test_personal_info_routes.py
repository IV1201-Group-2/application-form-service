from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_utilities import generate_token_for_user_id_1, \
    remove_test_user_from_db, \
    setup_test_user_in_db


def test_get_personal_info_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.get(
            '/application-form/applicant/personal_info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'test'
    assert response.json['surname'] == 'tester'
    assert response.json['role'] == 2


def test_get_personal_info_no_result(app_with_client):
    app, test_client = app_with_client
    remove_test_user_from_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.get(
            '/application-form/applicant/personal_info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'USER_NOT_FOUND'
    assert response.json['details'] == 'User not found with id: 1'


def test_get_personal_info_sqlalchemy_error(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_user_id_1(app)

    with patch('app.routes.applicant.personal_info_routes.'
               'fetch_personal_info') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

        response = test_client.get(
                '/application-form/applicant/personal_info/',
                headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 500
        assert response.json['error'] == 'COULD_NOT_FETCH_USER'
        assert response.json['details'] == 'Could not fetch user from database'
