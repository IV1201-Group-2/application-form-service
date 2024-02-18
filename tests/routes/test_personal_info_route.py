from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_utilities import generate_token_for_person_id_1, \
    remove_test_user_1_from_db, \
    setup_test_user_1_in_db


def test_get_personal_info_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/application-form/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['name'] == 'test'
    assert response.json['surname'] == 'tester'
    assert response.json['role'] == 2

    remove_test_user_1_from_db(app)


def test_get_personal_info_no_result(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/application-form/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'USER_NOT_FOUND'


@patch('app.routes.personal_info_route.fetch_personal_info')
def test_get_personal_info_sqlalchemy_error(mock_fetch, app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

    response = test_client.get(
            '/api/application-form/applicant/personal-info/',
            headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 500
    assert response.json['error'] == 'COULD_NOT_FETCH_USER'
