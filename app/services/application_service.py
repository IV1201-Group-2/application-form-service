from sqlalchemy.exc import SQLAlchemyError

from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile
from app.repositories.application_repository import \
    get_application_status_from_db, insert_application_in_db


def store_application(
        person_id: int, competences: list[CompetenceProfile],
        availabilities: list[Availability]) -> dict:
    """
    Store an application.

    This function stores an application in the database. It first creates an
    ApplicationStatus object, then tries to insert the application into the
    database. If the insertion fails, it raises an SQLAlchemyError.

    :param person_id: The ID of the person submitting the application.
    :param competences: A list of CompetenceProfile objects representing the
                        competences of the application.
    :param availabilities: A list of Availability objects representing the
                           availabilities of the application.
    :returns: A dictionary representing the stored application.
    :raises SQLAlchemyError: If there is an issue with the database operation.
    """

    application_status = ApplicationStatus(person_id)
    try:
        insert_application_in_db(
                competences, availabilities, application_status)
    except SQLAlchemyError:
        raise SQLAlchemyError({'error': 'DATABASE_ERROR'})

    return __format_application(application_status, competences,
                                availabilities)


def already_applied(person_id: int):
    """
    Check if a person has already applied.

    This function checks if a person has already applied for a job by checking
    if there is an application status with the person's ID in the database.

    :param person_id: The ID of the person to check.
    :returns: True if the person has already applied, False otherwise.
    """

    application_status = get_application_status_from_db(person_id)

    if application_status:
        return True

    return False


def __format_application(application_status: ApplicationStatus,
                         competences: list[CompetenceProfile],
                         availabilities: list[Availability]) -> dict:
    """
    Format an application.

    This function formats an application for output. It creates a dictionary
    that includes the application's status, competences, and availabilities.

    :param application_status: An ApplicationStatus object representing the
                               status of the application.
    :param competences: A list of CompetenceProfile objects representing the
                        competences of the application.
    :param availabilities: A list of Availability objects representing the
                           availabilities of the application.
    :returns: A dictionary representing the formatted application.
    """

    return {
        'status': application_status.status,
        'competences': [competence.to_dict() for competence in competences],
        'availabilities': [availability.to_dict() for availability in
                           availabilities]
    }
