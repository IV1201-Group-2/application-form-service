from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_status_codes import StatusCodes
from tests.utilities.test_utilities import generate_token_for_person_id_1, \
    remove_competences_from_db, setup_competences_in_db


def test_get_competences_success(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/application-form/competences/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.OK
    assert response.json == [{'competence_id': 1, 'name': 'tester'},
                             {'competence_id': 2, 'name': 'developer'}]

    remove_competences_from_db(app)


def test_competences_no_result(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    response = test_client.get(
            '/api/application-form/competences/',
            headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == StatusCodes.NOT_FOUND
    assert response.json['error'] == 'COMPETENCES_NOT_FOUND'


@patch('app.routes.competences_route.fetch_competences')
def test_get_personal_info_sqlalchemy_error(mock_fetch, app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_person_id_1(app)

    mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

    response = test_client.get(
            '/api/application-form/competences/',
            headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == StatusCodes.INTERNAL_SERVER_ERROR
    assert response.json['error'] == 'COULD_NOT_FETCH_COMPETENCES'
