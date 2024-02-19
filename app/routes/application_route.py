from datetime import datetime

from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.services.application_service import already_applied, store_application
from app.services.competences_service import fetch_competences
from app.utilities.status_codes import StatusCodes

application_submission_bp = Blueprint('application_submission', __name__)


@application_submission_bp.route('/', methods=['POST'])
@jwt_required()
def add_submitted_application() -> tuple[Response, int]:
    """
    Add a submitted application.

    This function adds a submitted application to the database. It first
    validates request and the data, and if all validations pass, it stores
    the application in the database.

    :returns: A tuple containing a Response object and an HTTP status code.
    """

    person_id = get_jwt()['id']

    role = get_jwt()['role']
    if role != 2:
        return (jsonify({'error': 'UNAUTHORIZED_ROLE'}),
                StatusCodes.UNAUTHORIZED)

    if (not request or request.content_type != 'application/json'
            or not request.json):
        return (jsonify({'error': 'INVALID_JSON_PAYLOAD'}),
                StatusCodes.BAD_REQUEST)

    if already_applied(person_id):
        return (jsonify({'error': 'ALREADY_APPLIED_BEFORE'}),
                StatusCodes.CONFLICT)

    application = request.json

    try:
        competences = application[
            'competences'] if 'competences' in application else []

        availabilities = application[
            'availabilities'] if 'availabilities' in application else []

        valid_competences = __validate_competences(person_id, competences)
        valid_availabilities = __validate_availabilities(
                person_id, availabilities)

        application = store_application(
                person_id, valid_competences, valid_availabilities)

    except (TypeError, KeyError, ValueError) as exception:
        return jsonify(exception.args[0]), StatusCodes.BAD_REQUEST
    except SQLAlchemyError as exception:
        return jsonify(exception.args[0]), StatusCodes.INTERNAL_SERVER_ERROR

    return jsonify(application), StatusCodes.CREATED


def __validate_competences(
        person_id: int, competences: list[dict]) -> list[CompetenceProfile]:
    """
    Validate competences.

    This function validates the competences of an application. It checks if the
    competences are a list and if they are valid competences.

    :param person_id: The ID of the person submitting the application.
    :param competences: A list of dictionaries representing the competences of
                        the application.
    :returns: A list of CompetenceProfile objects representing the validated
              competences.
    :raises TypeError: If the competences are not a list.
    """

    if not isinstance(competences, list):
        raise TypeError({'error': 'INVALID_PAYLOAD_STRUCTURE'})

    if competences:
        valid_competences = fetch_competences()
        return [__validate_competence(person_id, competence, valid_competences)
                for competence in competences]

    return []


def __validate_competence(
        person_id: int, competence: dict,
        valid_competences: list[dict]) -> CompetenceProfile:
    """
    Validate a competence.

    This function validates a single competence of an application. It checks if
    the competence is a dictionary and if it contains the required keys. It
    also checks if the competence ID is valid and if the years of experience is
    a valid float.

    :param person_id: The ID of the person submitting the application.
    :param competence: A dictionary representing a competence of the
                       application.
    :param valid_competences: A dictionary of valid competences.
    :returns: A CompetenceProfile object representing the validated competence.
    :raises TypeError: If the competence is not a dictionary.
    :raises KeyError: If a required key is missing from the competence.
    :raises ValueError: If a value in the competence is invalid.
    """

    if not isinstance(competence, dict):
        raise TypeError({'error': 'INVALID_COMPETENCE'})

    if 'competence_id' not in competence:
        raise KeyError({'error': 'MISSING_COMPETENCE_ID'})

    if 'years_of_experience' not in competence:
        raise KeyError({'error': 'MISSING_YEARS_OF_EXPERIENCE'})

    valid_competence_ids = [comp['competence_id'] for comp in
                            valid_competences]
    if competence['competence_id'] not in valid_competence_ids:
        raise ValueError({'error': 'INVALID_COMPETENCE_ID'})

    try:
        years_of_experience = float(competence['years_of_experience'])
    except ValueError:
        raise ValueError({'error': 'INVALID_YEARS_OF_EXPERIENCE'})

    if years_of_experience < 0:
        raise ValueError({'error': 'INVALID_YEARS_OF_EXPERIENCE'})

    return CompetenceProfile(
            person_id, competence['competence_id'], years_of_experience)


def __validate_availabilities(
        person_id: int, availabilities: list[dict]) -> list[Availability]:
    """
    Validate availabilities.

    This function validates the availabilities of an application. It checks if
    the availabilities are a list and if they are valid availabilities.

    :param person_id: The ID of the person submitting the application.
    :param availabilities: A list of dictionaries representing the
                           availabilities of the application.
    :returns: A list of Availability objects representing the validated
              availabilities.
    :raises TypeError: If the availabilities are not a list.
    :raises ValueError: If there are no availabilities.
    """
    if not isinstance(availabilities, list):
        raise TypeError({'error': 'INVALID_PAYLOAD_STRUCTURE'})

    if not availabilities:
        raise ValueError({'error': 'MISSING_AVAILABILITIES'})

    return [__validate_availability(person_id, availability)
            for availability in availabilities]


def __validate_availability(person_id: int,
                            availability: dict) -> Availability:
    """
    Validate an availability.

    This function validates a single availability of an application. It checks
    if the availability is a dictionary and if it contains the required keys.
    It also checks if the dates are valid and if the date range is valid.

    :param person_id: The ID of the person submitting the application.
    :param availability: A dictionary representing an availability of the
                         application.
    :returns: An Availability object representing the validated availability.
    :raises TypeError: If the availability is not a dictionary.
    :raises KeyError: If a required key is missing from the availability.
    :raises ValueError: If a value in the availability is invalid.
    """

    if not isinstance(availability, dict):
        raise TypeError({'error': 'INVALID_AVAILABILITY'})

    if 'from_date' not in availability:
        raise KeyError({'error': 'MISSING_FROM_DATE'})

    if 'to_date' not in availability:
        raise KeyError({'error': 'MISSING_TO_DATE'})

    try:
        from_date = datetime.strptime(
                availability['from_date'], '%Y-%m-%d')
        to_date = datetime.strptime(
                availability['to_date'], '%Y-%m-%d')
    except ValueError:
        raise ValueError({'error': 'INVALID_DATE_FORMAT'})

    if from_date > to_date:
        raise ValueError({'error': 'INVALID_DATE_RANGE'})

    return Availability(person_id, from_date, to_date)
