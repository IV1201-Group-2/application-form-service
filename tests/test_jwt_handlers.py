import datetime

from flask_jwt_extended import create_access_token

from tests.utilities.test_utilities import remove_test_user_1_from_db, \
    setup_test_user_1_in_db, generate_token_for_user_id_1


def test_valid_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    valid_token = generate_token_for_user_id_1(app)

    response = test_client.get(
        '/api/application-form/applicant/personal-info/',
        headers={
            'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200
    remove_test_user_1_from_db(app)


def test_invalid_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)
    valid_token = generate_token_for_user_id_1(app)
    invalid_token = valid_token + 'invalid'

    response = test_client.get(
        '/api/application-form/applicant/personal-info/',
        headers={
            'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'INVALID_TOKEN'


def test_expired_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_1_in_db(app)

    with app.app_context():
        expired_token = create_access_token(
            identity=None,
            additional_claims={'id': 1},
            expires_delta=datetime.timedelta(days=-1))

    response = test_client.get(
        '/api/application-form/applicant/personal-info/',
        headers={
            'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'TOKEN_EXPIRED'
    remove_test_user_1_from_db(app)


def test_unauthorized_request(app_with_client):
    app, test_client = app_with_client
    response = test_client.get(
        '/api/application-form/applicant/personal-info/')
    assert response.status_code == 401
    assert response.json['error'] == 'UNAUTHORIZED'
