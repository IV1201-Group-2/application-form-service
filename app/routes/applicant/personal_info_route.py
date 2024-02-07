from flask import Blueprint, Response, current_app, jsonify
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.applicant.personal_info_service import fetch_personal_info

personal_info_bp = Blueprint('personal-info', __name__)
CORS(personal_info_bp)


@personal_info_bp.route('/', methods=['GET'])
@jwt_required()
def get_personal_info() -> tuple[Response, int]:
    """
    Gets the personal information of the current user.

    :return: A tuple containing the response and the status code.
    """

    current_user = get_jwt_identity().get('id')

    try:
        personal_info = fetch_personal_info(current_user)
        current_app.logger.info(
                f'Responded with personal info for {current_user}.')
        return jsonify(personal_info), 200
    except NoResultFound:
        return jsonify({
            'error': 'USER_NOT_FOUND',
            'details': f'User not found with id: {current_user}'}), 404
    except SQLAlchemyError:
        return jsonify({
            'error': 'COULD_NOT_FETCH_USER',
            'details': 'Could not fetch user from database'}), 500
