from flask import Blueprint, Response, current_app, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.services.competences_service import fetch_competences

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

    try:
        competences = fetch_competences()
        current_app.logger.info('Responded with selectable competences.')
        return jsonify(competences), 200
    except NoResultFound:
        return jsonify({'error': 'COMPETENCES_NOT_FOUND'}), 404
    except SQLAlchemyError:
        return jsonify({'error': 'COULD_NOT_FETCH_COMPETENCES'}), 500
