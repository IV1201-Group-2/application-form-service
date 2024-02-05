from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_utilities import generate_token_for_user_id_1, \
    remove_competences_from_db, setup_competences_in_db


def test_get_competences_success(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.get(
            '/application-form/competences/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json == {'1': 'tester', '2': 'developer'}


def test_competences_no_result(app_with_client):
    app, test_client = app_with_client
    remove_competences_from_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.get(
            '/application-form/competences/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404
    assert response.json['error'] == 'COMPETENCES_NOT_FOUND'
    assert response.json['details'] == 'No competences found in the database'


def test_get_personal_info_sqlalchemy_error(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_user_id_1(app)

    with patch('app.routes.competences_routes.'
               'fetch_competences') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

        response = test_client.get(
                '/application-form/competences/',
                headers={'Authorization': f'Bearer {token}'})

        assert response.status_code == 500
        assert response.json['error'] == 'COULD_NOT_FETCH_COMPETENCES'
        assert response.json['details'] == ('Could not '
                                            'fetch competences from database')
