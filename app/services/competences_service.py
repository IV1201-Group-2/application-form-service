from app.repositories.competences_repository import get_competences_from_db


def fetch_competences() -> list[dict]:
    """
    Fetches the competences.

    This function fetches the competences from the database. It then
    converts each competence into a dictionary and returns a list of these
    dictionaries.

    :returns: A list of dictionaries, each representing a competence.
    """

    competences = get_competences_from_db()
    return [competence.to_dict() for competence in competences]
