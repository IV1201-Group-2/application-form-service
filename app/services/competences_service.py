from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.competence import Competence
from app.repositories.competences_repository import get_competences_from_db


def fetch_competences() -> dict[int, str]:
    """
    Fetches competences.

    :return: A dictionary containing the selectable competences.
    """

    try:
        competences = get_competences_from_db()
        return __competences_to_dict(competences)
    except (NoResultFound, SQLAlchemyError) as exception:
        raise exception


def __competences_to_dict(competences: list[Competence]) -> dict:
    """
    Converts a list of competences to a dictionary.

    :param competences: A list of competences.
    :return: A dictionary containing the competences.
    """

    return {competence.competence_id: competence.name
            for competence in competences}
