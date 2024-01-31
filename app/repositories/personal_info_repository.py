from app.models.person import Person


def get_person_from_db(username: str) -> Person or None:
    return Person.query.filter_by(username=username).first()
