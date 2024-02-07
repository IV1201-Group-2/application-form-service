from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import database
from app.models.applicant.competence_profile import CompetenceProfile


def insert_competences_in_db(applicant_competence: CompetenceProfile) -> None:
    """
    Insert applicant competences into the database.

    This function inserts an applicant's competences into the database using
    the provided CompetenceProfile object.

    :param applicant_competence: The CompetenceProfile object to insert
           into the database.
    :raises SQLAlchemyError: If there is an issue with the database operation,
            an SQLAlchemyError is raised.
    """

    try:
        database.session.add(applicant_competence)
        database.session.commit()
    except SQLAlchemyError as exception:
        current_app.logger.error(exception)
        raise SQLAlchemyError('COULD NOT PERSIST COMPETENCE PROFILE') from (
            exception)
