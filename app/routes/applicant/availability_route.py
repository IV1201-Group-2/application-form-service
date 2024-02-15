from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.services.applicant.availabilities_service import \
    store_applicant_availabilities

applicant_availabilities_bp = Blueprint('applicant_availabilities', __name__)


@applicant_availabilities_bp.route('/', methods=['POST'])
@jwt_required()
def add_applicant_availabilities() -> tuple[Response, int]:
    """
    Add applicant availabilities with JWT authentication.

    This endpoint allows the addition of applicant availabilities using JWT
    for authentication.

    :returns: A tuple containing a JSON response indicating the success or
              failure of the availability addition and the HTTP status code.
    :raises 400: If the request payload is invalid or not in the expected
                 format, an error response with status code 400 is returned.
    :raises 207: If some availabilities are successfully added but others fail,
                 a partial success response with status code 207 is returned.
    """

    if request.json is None or not isinstance(request.json, list):
        return jsonify({'error': 'INVALID_JSON_PAYLOAD'}), 400

    availabilities = request.json
    current_user = get_jwt()['id']

    result = store_applicant_availabilities(current_user, availabilities)

    if result['successes']:
        if result['failures']:
            return jsonify(result), 207
        else:
            return jsonify(result), 200
    elif result['failures']:
        return jsonify(result), 400
    else:
        return jsonify(result), 200
