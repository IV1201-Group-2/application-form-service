from flask import Blueprint, Response, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app.services.applicant.competences_service import \
    store_applicant_competences

applicant_competences_bp = Blueprint('applicant_competences', __name__)


@applicant_competences_bp.route('/', methods=['POST'])
@jwt_required()
def add_applicant_competence() -> tuple[Response, int]:
    """
    Add applicant competence with JWT authentication.

    This endpoint allows the addition of applicant competences using JSON Web
    Tokens (JWT) for authentication.

    :returns: JSON response indicating the success of the competence addition.
    :raises 400: If the request payload is invalid, an error response with
                 status code 400 is returned.
    :raises 500: If an internal server error occurs during the competence
                 addition, an error response with status code 500 is returned.
    """

    if request.json is None:
        return jsonify({'error': 'INVALID_JSON_PAYLOAD'}), 400

    competence_id = int(request.json.get('competence_id'))
    experience = float(request.json.get('experience'))

    if not competence_id and competence_id > 0:
        return jsonify({'error': 'INVALID_COMPETENCE_ID'}), 400
    elif not experience and 0 <= experience <= 100:
        return jsonify({'error': 'INVALID_EXPERIENCE_VALUE'}), 400

    current_user = get_jwt_identity()

    try:
        persisted_competence = store_applicant_competences(current_user,
                                                           competence_id,
                                                           experience)
        current_app.logger.info(
                f'Persisted competences of {current_user}.')
        return jsonify(persisted_competence), 200
    except SQLAlchemyError:
        return (jsonify({
            'error': 'COULD_NOT_FETCH_APPLICANT_COMPETENCES',
            'details': 'Could not fetch competences from database'}), 500)
