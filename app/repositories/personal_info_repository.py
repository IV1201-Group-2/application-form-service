from flask import current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError

from app.models.person import Person


def get_person_from_db(username: str) -> Person:
    try:
        return Person.query.filter_by(username=username).one()
    except NoResultFound:
        log_and_raise(NoResultFound, f'No user found with username {username}.')
    except MultipleResultsFound:
        log_and_raise(MultipleResultsFound,
                      f'Multiple users found with username {username}.')
    except SQLAlchemyError:
        log_and_raise(SQLAlchemyError, 'Error retrieving user from the database.')


def log_and_raise(exception_type, message):
    exception = exception_type(message)
    current_app.logger.error(exception)
    raise exception
