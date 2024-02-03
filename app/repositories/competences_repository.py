from flask import current_app
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from app.models.competence import Competence


def get_competences_from_db() -> list[Competence]:
    """
    Retrieves a list of competences from the database.

    :return: A list of Competence objects.
    """

    try:
        competences = Competence.query.all()
        if not competences:
            exception = NoResultFound('No competences found in the database')
            current_app.logger.error(exception)
            raise exception
        return competences
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError('COULD_NOT_FETCH_COMPETENCES')
