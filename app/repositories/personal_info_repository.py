from typing import NoReturn

from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.person import Person


def get_person_from_db(user_id: int) -> Person:
    """
    Retrieves a person from the database by their user ID.

    :param user_id: The user ID of the person.
    :return: The Person object.
    """

    try:
        return Person.query.filter_by(person_id=user_id).one()
    except NoResultFound:
        __log_and_raise(NoResultFound, f'USER NOT FOUND: {user_id}.')
    except SQLAlchemyError:
        __log_and_raise(SQLAlchemyError, 'DATABASE CONNECTION ERROR.')


def __log_and_raise(exception_type: type, message: str) -> NoReturn:
    """
    Logs an error and raises an exception.

    :param exception_type: The type of the exception.
    :param message: The error message.
    """

    exception = exception_type(message)
    current_app.logger.error(exception)
    raise exception
