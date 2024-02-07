from unittest.mock import patch

from sqlalchemy.exc import SQLAlchemyError

from app.services.applicant.competences_service import \
    store_applicant_competences


def test_store_applicant_competences_multiple_success(app_with_client):
    app, client = app_with_client
    user_id = 1

    competences = [
        {'competence_id': 1, 'experience': 5.0},
        {'competence_id': 2, 'experience': 3.0}
    ]

    with app.app_context():
        result = store_applicant_competences(user_id, competences)
        assert len(result['successes']) == 2
        assert len(result['failures']) == 0
        assert result['successes'][0]['competence_id'] == 1
        assert result['successes'][1]['competence_id'] == 2


def test_store_applicant_competences_mixed_results(app_with_client):
    app, client = app_with_client
    user_id = 1

    competences = [
        {'competence_id': 1, 'experience': 5.0},
        {'competence_id': -1, 'experience': 100.1}
    ]

    with app.app_context():
        result = store_applicant_competences(user_id, competences)
        assert len(result['successes']) == 1
        assert len(result['failures']) == 1
        assert result['successes'][0]['competence_id'] == 1
        assert result['failures'][0]['competence_id'] == -1


def test_store_applicant_competences_invalid_input(app_with_client):
    app, client = app_with_client
    user_id = 1

    competences = [
        {'competence_id': -1, 'experience': 5.0},
        {'competence_id': 2, 'experience': -1.0}
    ]

    with app.app_context():
        result = store_applicant_competences(user_id, competences)
        assert len(result['successes']) == 0
        assert len(result['failures']) == 2
        assert result['failures'][0]['competence_id'] == -1
        assert result['failures'][1]['competence_id'] == 2


@patch('app.services.applicant.competences_service'
       '.insert_competences_in_db')
def test_store_applicant_competences_sqlalchemy_error(mock_insert,
                                                      app_with_client):
    app, client = app_with_client
    user_id = 1

    competences = [{'competence_id': 1, 'experience': 5.0}]
    mock_insert.side_effect = SQLAlchemyError("DATABASE CONNECTION ERROR")

    with app.app_context():
        result = store_applicant_competences(user_id, competences)
        assert mock_insert.call_count == 1
        assert len(result['failures']) == 1
        assert "DATABASE CONNECTION ERROR" in result['failures'][0]['error']
