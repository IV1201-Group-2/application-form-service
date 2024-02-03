from flask import current_app
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.competence import Competence


def get_competences_from_db() -> list[Competence]:
    """
    Retrieves a list of competences from the database.

    :return: A list of Competence objects.
    """

    try:
        competences = Competence.query.all()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError('COULD NOT FETCH COMPETENCES')

    if not competences:
        exception = NoResultFound('NO COMPETENCES FOUND')
        current_app.logger.error(exception)
        raise exception
    return competences
