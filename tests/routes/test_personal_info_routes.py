import datetime
from unittest.mock import patch

from flask_jwt_extended import create_access_token
from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_utilities import remove_test_user_from_db, \
	setup_test_user_in_db


def test_get_personal_info_success(app_with_client):
	app, test_client = app_with_client
	setup_test_user_in_db(app)
	token = generate_token_for_user_id_1(app)

	response = test_client.get('/applicant/personal_info/',
							   headers={'Authorization': f'Bearer {token}'})
	assert response.status_code == 200
	assert response.json['name'] == 'test'
	assert response.json['surname'] == 'tester'
	assert response.json['role'] == 2


def test_get_personal_info_no_result(app_with_client):
	app, test_client = app_with_client
	remove_test_user_from_db(app)
	token = generate_token_for_user_id_1(app)

	response = test_client.get('/applicant/personal_info/',
							   headers={'Authorization': f'Bearer {token}'})
	assert response.status_code == 404
	assert response.json['error'] == 'USER_NOT_FOUND'
	assert response.json['details'] == 'User not found with id: 1'


def test_get_personal_info_sqlalchemy_error(app_with_client):
	app, test_client = app_with_client
	token = generate_token_for_user_id_1(app)

	with patch(
			'app.routes.personal_info_routes.fetch_personal_info') as mock_fetch:
		mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

		response = test_client.get('/applicant/personal_info/',
								   headers={
									   'Authorization': f'Bearer {token}'})

		assert response.status_code == 500
		assert response.json['error'] == 'COULD_NOT_FETCH_USER'
		assert response.json['details'] == 'Could not fetch user from database'


def generate_token_for_user_id_1(app) -> tuple[str, str]:
	token_data = {
		"id": 1,
		"iat": datetime.datetime(2023, 1, 1).timestamp(),
		"exp": datetime.datetime(2025, 1, 2).timestamp()
	}

	with app.app_context():
		return create_access_token(identity=token_data)
