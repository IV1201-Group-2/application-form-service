from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from tests.utilities.test_utilities import generate_token_for_user_id_1, \
    remove_competences_from_db, remove_test_user_from_db, \
    setup_competences_in_db, setup_test_user_in_db


def test_add_applicant_competence_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)
    setup_competences_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json={
                'competence_id': 1,
                'experience': 5.0
            },
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert 'application/json' in response.content_type
    assert response.json['competence_id'] == 1
    assert response.json['years_of_experience'] == '5.00'
    assert response.json['person_id'] == 1

    remove_test_user_from_db(app)
    remove_competences_from_db(app)


def test_add_applicant_competence_invalid_experience_value(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json={
                'competence_id': 1,
                'experience': -1.0
            },
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.json == {'error': 'INVALID_EXPERIENCE_VALUE'}

    remove_test_user_from_db(app)


def test_add_applicant_competence_invalid_competence_id(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json={
                'competence_id': 0,
                'experience': 1.0
            },
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.json == {'error': 'INVALID_COMPETENCE_ID'}

    remove_test_user_from_db(app)


def test_get_personal_info_sqlalchemy_error(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_user_id_1(app)

    with patch('app.routes.applicant.competences_route'
               '.store_applicant_competences') as mock_fetch:
        mock_fetch.side_effect = SQLAlchemyError("A database error occurred")

        response = test_client.post(
                '/api/application-form/applicant/competences/',
                json={
                    'competence_id': 1,
                    'experience': 5.0
                },
                headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == 500
        assert response.json[
                   'error'] == 'COULD_NOT_FETCH_APPLICANT_COMPETENCES'
        assert response.json[
                   'details'] == 'Could not fetch competences from database'
