from tests.utilities.test_utilities import generate_token_for_user_id_1, \
    remove_competences_from_db, remove_test_user_from_db, \
    setup_competences_in_db, setup_test_user_in_db


def test_add_applicant_competences_success(app_with_client):
    app, test_client = app_with_client
    setup_test_user_in_db(app)
    setup_competences_in_db(app)
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json=[
                {'competence_id': 1, 'experience': 5.0},
                {'competence_id': 2, 'experience': 3.0}
            ],
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert len(response.json['successes']) == 2
    assert response.json['successes'][0]['competence_id'] == 1
    assert response.json['successes'][0]['years_of_experience'] == '5.00'
    assert response.json['successes'][1]['competence_id'] == 2
    assert response.json['successes'][1]['years_of_experience'] == '3.00'

    remove_test_user_from_db(app)
    remove_competences_from_db(app)


def test_add_applicant_competences_invalid_json(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json={'not': 'a list'},
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.json['error'] == 'INVALID_JSON_PAYLOAD'


def test_add_applicant_competences_empty_list(app_with_client):
    app, test_client = app_with_client
    token = generate_token_for_user_id_1(app)

    response = test_client.post(
            '/api/application-form/applicant/competences/',
            json=[],
            headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.json == {'failures': [], 'successes': []}
