from sqlalchemy.exc import MultipleResultsFound, SQLAlchemyError, NoResultFound

from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(username: str) -> dict[str, str]:
    try:
        person = get_person_from_db(username)
        return person_to_dict(person)
    except (NoResultFound, MultipleResultsFound, SQLAlchemyError) as exception:
        raise exception


def person_to_dict(person):
    return {
        'person_id': person.person_id,
        'name': person.name,
        'surname': person.surname,
        'pnr': person.pnr,
        'email': person.email,
        'username': person.username
    }
