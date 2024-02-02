from sqlalchemy.exc import MultipleResultsFound, SQLAlchemyError, NoResultFound

from app.models.person import Person
from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(username: str) -> dict[str, str]:
    """
    Fetches personal information for a given username.

    :param username: The username of the person.
    :return: A dictionary containing the personal information of the person.
    """

    try:
        person = get_person_from_db(username)
        return __person_to_dict(person)
    except (NoResultFound, MultipleResultsFound, SQLAlchemyError) as exception:
        raise exception


def __person_to_dict(person: Person) -> dict:
    """
    Converts a Person object to a dictionary.

    :param person: The Person object.
    :return: A dictionary representation of the Person object.
    """
    
    return {
        'person_id': person.person_id,
        'name': person.name,
        'surname': person.surname,
        'pnr': person.pnr,
        'email': person.email,
        'username': person.username
    }
