from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.services.applicant.competences_service import \
    store_applicant_competences

applicant_competences_bp = Blueprint('applicant_competences', __name__)


@applicant_competences_bp.route('/', methods=['POST'])
@jwt_required()
def add_applicant_competences() -> tuple[Response, int]:
    """
    Add applicant competences with JWT authentication.

    This endpoint allows the addition of applicant competences using JWT
    for authentication.

    :returns: A tuple containing a JSON response indicating the
              success of the competence addition and the HTTP status code.
    :raises 400: If the request payload is invalid or not in the expected
                 format, an error response with status code 400 is returned.
    """
    if request.json is None or not isinstance(request.json, list):
        return jsonify({'error': 'INVALID_JSON_PAYLOAD'}), 400

    competences = request.json
    current_user = get_jwt()['id']

    result = store_applicant_competences(current_user, competences)

    if result['successes']:
        if result['failures']:
            return jsonify(result), 207
        else:
            return jsonify(result), 200
    elif result['failures']:
        return jsonify(result), 400
    else:
        return jsonify(result), 200
