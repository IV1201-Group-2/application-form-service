from flask import current_app
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, SQLAlchemyError

from app.models.person import Person


def get_person_from_db(username: str) -> Person:
    try:
        return Person.query.filter_by(username=username).one()
    except NoResultFound as exception:
        log_and_raise(exception, f'No user found with username {username}.')
    except MultipleResultsFound as exception:
        log_and_raise(exception, f'Multiple users found with username {username}.')
    except SQLAlchemyError as exception:
        log_and_raise(exception, 'Error retrieving user from database.')


def log_and_raise(exception, message):
    current_app.logger.error(exception)
    raise exception(message)
