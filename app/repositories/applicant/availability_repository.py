from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import database
from app.models.applicant.availability import Availability


def insert_availability_in_db(applicant_availability: Availability) -> None:
    """
    Insert applicant availability into the database.

    This function inserts an applicant's availability into the database using
    the provided Availability object.

    :param applicant_availability: The Availability object to insert into the
           database.
    :type applicant_availability: Availability
    :returns: None
    :raises SQLAlchemyError: If there is an issue with the database operation,
            an SQLAlchemyError is raised.
    """

    try:
        database.session.add(applicant_availability)
        database.session.commit()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError('COULD NOT PERSIST AVAILABILITY') from exception
