from flask import Blueprint, Response, current_app, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.personal_info_service import fetch_personal_info
from app.utilities.status_codes import StatusCodes

personal_info_bp = Blueprint('personal-info', __name__)


@personal_info_bp.route('/', methods=['GET'])
@jwt_required()
def get_personal_info() -> tuple[Response, int]:
    """
    Gets the personal information of the current user.

    This function retrieves the personal information of the current user from
    the database. If the user is not found, it returns a 404 error. If there is
    an issue with the database operation, it returns a 500 error.

    :returns: A tuple containing the response and the status code.
    :raises NoResultFound: If no user is found in the database.
    :raises SQLAlchemyError: If there is an issue with the database operation.
    """

    person_id = get_jwt()['id']

    try:
        personal_info = fetch_personal_info(person_id)
        current_app.logger.info(
                f'Responded with personal info for id: {person_id}.')
        return jsonify(personal_info), StatusCodes.OK
    except NoResultFound:
        return jsonify({'error': 'USER_NOT_FOUND'}), StatusCodes.NOT_FOUND
    except SQLAlchemyError:
        return (jsonify({'error': 'COULD_NOT_FETCH_USER'}),
                StatusCodes.INTERNAL_SERVER_ERROR)
