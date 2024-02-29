import logging

from sqlalchemy.exc import SQLAlchemyError

from app.extensions import database
from app.models.application import ApplicationStatus
from app.models.availability import Availability
from app.models.competence_profile import CompetenceProfile


def insert_application_in_db(
        competences: list[CompetenceProfile],
        availabilities: list[Availability],
        application_status: ApplicationStatus) -> None:
    """
        Insert an application into the database.

        This function inserts an application's competences, availabilities,
        and status into the database. If any of the insert operations fail,
        the database session is rolled back to maintain data integrity.

        :param competences: List of CompetenceProfile objects representing
        the competences of the application.
        :param availabilities: A list of Availability objects representing
        the availabilities of the application.
        :param application_status: An ApplicationStatus object representing
        the status of the application.
        :returns: None
        :raises SQLAlchemyError: If there is an issue with any of the database
        operations, an SQLAlchemyError is raised.
    """

    __insert_competences_in_db(competences)
    __insert_availabilities_in_db(availabilities)
    __insert_application_status_in_db(application_status)
    database.session.commit()


def get_application_status_from_db(person_id: int) -> ApplicationStatus:
    """
    Get application status from the database.

    This function retrieves the application status of a person from the
    database.

    :param person_id: The ID of the person to retrieve the application status
    for.
    :returns: The ApplicationStatus object representing the application status
    of the person.
    :raises SQLAlchemyError: If there is an issue with the database operation,
    an SQLAlchemyError is raised.
    """

    try:
        return ApplicationStatus.query.filter_by(person_id=person_id).first()
    except SQLAlchemyError as exception:
        logging.debug(str(exception), exc_info=True)
        raise SQLAlchemyError


def __insert_availabilities_in_db(availabilities: list[Availability]) -> None:
    """
    Insert applicant availability into the database.

    This function inserts an applicant's availability into the database using
    the provided Availability object.

    :param availabilities: List of Availability objects to insert into the
             database.
    :returns: None
    :raises SQLAlchemyError: If there is an issue with the database operation,
            an SQLAlchemyError is raised.
    """

    try:
        database.session.add_all(availabilities)
    except SQLAlchemyError as exception:
        database.session.rollback()
        logging.debug(str(exception), exc_info=True)
        raise SQLAlchemyError


def __insert_competences_in_db(
        competences: list[CompetenceProfile]) -> None:
    """
    Insert applicant competences into the database.

    This function inserts an applicant's competences into the database using
    the provided CompetenceProfile object.

    :param competences: List of CompetenceProfile object to insert
           into the database.
    :raises SQLAlchemyError: If there is an issue with the database operation,
            an SQLAlchemyError is raised.
    """

    try:
        database.session.add_all(competences)
    except SQLAlchemyError as exception:
        database.session.rollback()
        logging.debug(str(exception), exc_info=True)
        raise SQLAlchemyError


def __insert_application_status_in_db(
        application_status: ApplicationStatus) -> None:
    """
    Insert application into the database.

    This function inserts an application into the database using the
    provided Application object.

    :param application_status: The Application object to insert into the
           database.
    :raises SQLAlchemyError: If there is an issue with the database operation,
            an SQLAlchemyError is raised.
    """

    try:
        database.session.add(application_status)
    except SQLAlchemyError as exception:
        database.session.rollback()
        logging.debug(str(exception), exc_info=True)
        raise SQLAlchemyError
