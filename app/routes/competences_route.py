import logging

from flask import Blueprint, Response, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.competences_service import fetch_competences
from app.utilities.status_codes import StatusCodes

competences_bp = Blueprint('competences', __name__)


@competences_bp.route('/', methods=['GET'])
@jwt_required()
def get_competences() -> tuple[Response, int]:
    """
    Gets the selectable competences.

    This function retrieves the selectable competences from the database. If
    the competences are not found, it returns a 404 error. If there is an issue
    with the database operation, it returns a 500 error.

    :returns: A tuple containing the response and the status code.
    :raises NoResultFound: If no competences are found in the database.
    :raises SQLAlchemyError: If there is an issue with the database operation.
    """

    requester_ip = request.remote_addr

    try:
        competences = fetch_competences()
        logging.info(f'{requester_ip} - Responded with competences.')
        return jsonify(competences), StatusCodes.OK
    except NoResultFound:
        logging.error(f'{requester_ip} - No competences found.')
        return jsonify(
                {'error': 'COMPETENCES_NOT_FOUND'}), StatusCodes.NOT_FOUND
    except SQLAlchemyError:
        logging.error(f'{requester_ip} - Could not fetch competences.')
        return (jsonify({'error': 'COULD_NOT_FETCH_COMPETENCES'}),
                StatusCodes.INTERNAL_SERVER_ERROR)
