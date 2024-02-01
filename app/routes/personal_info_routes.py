from flask import Blueprint, jsonify, Response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError

from app.services.personal_info_service import fetch_personal_info

personal_info_bp = Blueprint('personal_info', __name__)


@personal_info_bp.route('/get', methods=['GET'])
@jwt_required()
def get_personal_info() -> tuple[Response, int]:
    current_user = get_jwt_identity()

    def handle_error(exception, status_code):
        error_message = {'error': str(exception)}
        return jsonify(error_message), status_code

    try:
        personal_info = fetch_personal_info(current_user)
        current_app.logger.info(f'Responded with personal info for {current_user}.')
        return jsonify(personal_info), 200
    except NoResultFound as ex:
        return handle_error(ex, 404)
    except MultipleResultsFound as ex:
        return handle_error(ex, 409)
    except SQLAlchemyError as ex:
        return handle_error(ex, 500)
