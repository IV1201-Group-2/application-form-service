import datetime

from flask_jwt_extended import create_access_token

from tests.utilities.test_utilities import setup_test_user_in_db


def test_valid_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)

    with app.app_context():
        valid_token = create_access_token(
                identity={'id': 1}, expires_delta=datetime.timedelta(days=1))

    response = test_client.get('/application-form/applicant/personal-info/',
                               headers={
                                   'Authorization': f'Bearer {valid_token}'})
    assert response.status_code == 200


def test_invalid_token(app_with_client):
    app, test_client = app_with_client

    with app.app_context():
        valid_token = create_access_token(
                identity={'id': 1}, expires_delta=datetime.timedelta(days=1))
        invalid_token = valid_token + 'invalid'

    response = test_client.get('/application-form/applicant/personal-info/',
                               headers={
                                   'Authorization': f'Bearer {invalid_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'INVALID_TOKEN'


def test_expired_token(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)

    with app.app_context():
        expired_token = create_access_token(
                identity={'id': 1}, expires_delta=datetime.timedelta(days=-1))

    response = test_client.get('/application-form/applicant/personal-info/',
                               headers={
                                   'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'TOKEN_EXPIRED'


def test_unauthorized_request(app_with_client):
    app, test_client = app_with_client
    response = test_client.get('/application-form/applicant/personal-info/')
    assert response.status_code == 401
    assert response.json['error'] == 'UNAUTHORIZED'
