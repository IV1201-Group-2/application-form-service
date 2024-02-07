from datetime import date, datetime

from sqlalchemy.exc import SQLAlchemyError

from app.models.applicant.availability import Availability
from app.repositories.applicant.availability_repository import \
    insert_availability_in_db


def store_applicant_availabilities(
        user_id: int, availabilities: list[dict]) -> dict:
    """
    Store applicant availabilities in the database.

    This function stores the applicant's availabilities in the database.

    :param user_id: The ID of the user to associate the availabilities with.
    :param availabilities: A list of dictionaries representing the
           availabilities to store.
    :returns: A dictionary containing successes and failures of availability
              storage.
    """

    successes = []
    failures = []

    for availability in availabilities:
        try:
            from_date, to_date = __valid_input_availability(availability)
            applicant_availability = Availability(user_id, from_date, to_date)
            insert_availability_in_db(applicant_availability)
            successes.append(
                    __applicant_availability_to_dict(applicant_availability))
        except (ValueError, SQLAlchemyError) as exception:
            failures.append({
                'from_date': availability.get('from_date'), 'to_date':
                    availability.get('to_date'), 'error': str(exception)})

    return {'successes': successes, 'failures': failures}


def __applicant_availability_to_dict(
        applicant_availability: Availability) -> dict:
    """
    Convert an applicant availability object to a dictionary.

    This function takes an Availability object and converts it into a
    dictionary containing relevant information.

    :param applicant_availability: The Availability object to convert.
    :returns: A dictionary representation of the applicant availability.
    """

    return {
        'person_id': applicant_availability.person_id,
        'from_date': applicant_availability.from_date,
        'to_date': applicant_availability.to_date
    }


def __valid_input_availability(availability: dict) -> tuple[date, date]:
    """
    Validate and parse input availability dates.

    This function validates and parses the from_date and to_date from a
    dictionary representing an availability.

    :param availability: A dictionary representing the availability.
    :returns: A tuple containing validated and parsed from_date and to_date.
    :raises ValueError: If from_date or to_date is missing or in an invalid
            format, a ValueError is raised.
    """

    from_date_raw = availability.get('from_date')
    to_date_raw = availability.get('to_date')

    if from_date_raw is None:
        raise ValueError('From date is missing.')

    if to_date_raw is None:
        raise ValueError('To date is missing.')

    from_date = datetime.strptime(from_date_raw, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_raw, '%Y-%m-%d').date()

    return from_date, to_date
