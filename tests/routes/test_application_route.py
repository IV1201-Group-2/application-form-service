from tests.utilities.test_status_codes import StatusCodes
from tests.utilities.test_utilities import generate_token_for_person_id_1, \
    remove_application_components_from_db, remove_competences_from_db, \
    setup_competences_in_db

def test_add_application_success(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.CREATED
    response_data = response.json

    assert 'competences' in response_data
    assert 'availabilities' in response_data

    expected_competences = payload['competences']
    expected_availabilities = payload['availabilities']

    assert response_data['competences'] == expected_competences
    assert response_data['availabilities'] == expected_availabilities

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_application_with_invalid_json(app_with_client):
    _, test_client = app_with_client
    token = generate_token_for_person_id_1(app_with_client[0])

    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                data="This is not JSON")

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert response.json == {'error': 'INVALID_JSON_PAYLOAD'}


def test_add_application_missing_competences(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.CREATED
    assert response.json['competences'] == []
    assert response.json['availabilities'] == payload['availabilities']
    assert response.json['status'] == 'UNHANDLED'

    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_competence_type(app_with_client):
    app, test_client = app_with_client
    (app)
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": "invalid_type",
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_PAYLOAD_STRUCTURE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_missing_competence_id(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"years_of_experience": '5.00'}],
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'MISSING_COMPETENCE_ID'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_missing_years_of_experience(
        app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1}],
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'MISSING_YEARS_OF_EXPERIENCE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_competence_id(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 999, "years_of_experience": '5.00'}],
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_COMPETENCE_ID'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_years_of_experience(
        app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '-5.00'}],
        "availabilities": [
            {"from_date": "2021-01-01", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_YEARS_OF_EXPERIENCE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_availabilities_type(
        app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": "invalid_type"
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_PAYLOAD_STRUCTURE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_missing_availabilities(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": []
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'MISSING_AVAILABILITIES'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_availability_type(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": ["invalid_type"]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_AVAILABILITY'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_missing_from_date(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": [{"to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'MISSING_FROM_DATE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_missing_to_date(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": [{"from_date": "2021-01-01"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'MISSING_TO_DATE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_date_format(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": [
            {"from_date": "invalid_date", "to_date": "2021-01-02"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_DATE_FORMAT'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)


def test_add_submitted_application_invalid_date_range(app_with_client):
    app, test_client = app_with_client
    setup_competences_in_db(app)
    token = generate_token_for_person_id_1(app)

    payload = {
        "competences": [{"competence_id": 1, "years_of_experience": '5.00'}],
        "availabilities": [
            {"from_date": "2021-01-02", "to_date": "2021-01-01"}]
    }
    response = test_client.post('/api/application-form/submit/',
                                headers={'Authorization': f'Bearer {token}'},
                                json=payload)

    assert response.status_code == StatusCodes.BAD_REQUEST
    assert 'error' in response.json
    assert response.json['error'] == 'INVALID_DATE_RANGE'

    remove_competences_from_db(app)
    remove_application_components_from_db(app)
