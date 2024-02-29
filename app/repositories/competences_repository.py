import logging

from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.competence import Competence


def get_competences_from_db() -> list[Competence]:
    """
    Retrieve a list of competences from the database.

    This function retrieves a list of competences from the database. If the
    retrieval fails, it raises an SQLAlchemyError. If no competences are found,
    it raises a NoResultFound exception.

    :returns: A list of Competence objects.
    :raises SQLAlchemyError: If there is an issue with the database operation.
    :raises NoResultFound: If no competences are found in the database.
    """

    try:
        competences = Competence.query.all()
    except SQLAlchemyError as exception:
        logging.debug(str(exception), exc_info=True)
        raise SQLAlchemyError

    if not competences:
        logging.debug(NoResultFound('NO COMPETENCES FOUND'))
        raise NoResultFound
    return competences
