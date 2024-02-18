from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.person import Person


def get_person_from_db(person_id: int) -> Person:
    """
    Retrieve a person from the database by their user ID.

    This function retrieves a person from the database using their user ID. If
    the person is not found, it raises a NoResultFound exception. If there is
    an issue with the database operation, it raises an SQLAlchemyError.

    :param person_id: The user ID of the person.
    :returns: The Person object.
    :raises NoResultFound: If no person is found with the provided user ID.
    :raises SQLAlchemyError: If there is an issue with the database operation.
    """

    try:
        return Person.query.filter_by(person_id=person_id).one()
    except NoResultFound as exception:
        current_app.logger.error(exception)
        raise NoResultFound
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError
