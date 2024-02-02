from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.person import Person


def get_person_from_db(user_id: int) -> Person:
    try:
        return Person.query.filter_by(person_id=user_id).one()
    except NoResultFound:
        __log_and_raise(NoResultFound, f'USER NOT FOUND: {user_id}.')
    except SQLAlchemyError:
        __log_and_raise(SQLAlchemyError, 'DATABASE CONNECTION ERROR.')


def __log_and_raise(exception_type: type, message: str) -> None:
    exception = exception_type(message)
    current_app.logger.error(exception)
    raise exception
