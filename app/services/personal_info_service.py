from flask import Response

from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(username: str) -> Response or None:
    person = get_person_from_db(username)

    if person is None:
        return None

    return person_to_dict(person)


def person_to_dict(person):
    return {
        'person_id': person.person_id,
        'name': person.name,
        'surname': person.surname,
        'pnr': person.pnr,
        'email': person.email,
        'username': person.username
    }
