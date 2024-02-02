from flask import Blueprint, jsonify, Response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError

from app.services.personal_info_service import fetch_personal_info

personal_info_bp = Blueprint('personal_info', __name__)


@personal_info_bp.route('/get', methods=['GET'])
@jwt_required()
def get_personal_info() -> tuple[Response, int]:
    """
    Gets the personal information of the current user.

    :return: A tuple containing the response and the status code.
    """

    current_user = get_jwt_identity()

    try:
        personal_info = fetch_personal_info(current_user)
        current_app.logger.info(f'Responded with personal info for {current_user}.')
        return jsonify(personal_info), 200
    except NoResultFound:
        return jsonify({'error': 'USER_NOT_FOUND',
                        'details': f'User not found with email: {current_user}'}), 404
    except MultipleResultsFound:
        return jsonify({'error': 'MULTIPLE_USERS_FOUND',
                        'details':
                            f'Multiple users found with email: {current_user}'}), 409
    except SQLAlchemyError:
        return jsonify({'error': 'COULD_NOT_FETCH_USER',
                        'details': 'Could not fetch user from database'}), 500
