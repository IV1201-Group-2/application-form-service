from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.applicant.person import Person


def get_person_from_db(user_id: int) -> Person:
    """
    Retrieves a person from the database by their user ID.

    :param user_id: The user ID of the person.
    :return: The Person object.
    """

    try:
        return Person.query.filter_by(person_id=user_id).one()
    except NoResultFound as exception:
        current_app.logger.error(exception)
        raise NoResultFound(f'USER NOT FOUND: {user_id}.')
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError('COULD NOT FETCH PERSONAL INFO.')
