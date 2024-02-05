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

    :return: A tuple containing the response and the status code.
    """

    try:
        competences = fetch_competences()
        current_app.logger.info('Responded with selectable competences.')
        return jsonify(competences), 200
    except NoResultFound:
        return jsonify({
            'error': 'COMPETENCES_NOT_FOUND',
            'details': 'No competences found in the database'}), 404
    except SQLAlchemyError:
        return jsonify({
            'error': 'COULD_NOT_FETCH_COMPETENCES',
            'details': 'Could not fetch competences from database'}), 500
