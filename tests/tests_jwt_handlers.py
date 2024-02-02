import datetime

from flask_jwt_extended import create_access_token


def test_invalid_token(app_with_client):
    app, test_client = app_with_client
    response = test_client.get('/applicant/personal_info/',
                               headers={'Authorization': 'Bearer invalid token'})
    assert response.status_code == 401
    assert response.json['error'] == 'Invalid token provided'


def test_expired_token(app_with_client):
    app, test_client = app_with_client
    test_identity = 'test_user_id'
    with app.app_context():
        expired_token = create_access_token(identity=test_identity,
                                            expires_delta=datetime.timedelta(
                                                minutes=-1))

    response = test_client.get('/applicant/personal_info/',
                               headers={'Authorization': f'Bearer {expired_token}'})
    assert response.status_code == 401
    assert response.json['error'] == 'Token has expired'


def test_unauthorized_request(app_with_client):
    app, test_client = app_with_client
    response = test_client.get('/applicant/personal_info/')
    assert response.status_code == 401
    assert response.json['error'] == 'Unauthorized'
