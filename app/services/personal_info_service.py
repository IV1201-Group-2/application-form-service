from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app.models.person import Person
from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(user_id: int) -> dict[str, str]:
	"""
	Fetches personal information for a given email.

	:param user_id: The user id of the user.
	:return: A dictionary containing the personal information of the person.
	"""

	try:
		person = get_person_from_db(user_id)
		return __person_to_dict(person)
	except (NoResultFound, SQLAlchemyError) as exception:
		raise exception


def __person_to_dict(person: Person) -> dict:
	"""
	Converts a Person object to a dictionary.

	:param person: The Person object.
	:return: A dictionary representation of the Person object.
	"""

	return {
		'id': person.person_id,
		'name': person.name,
		'surname': person.surname,
		'pnr': person.pnr,
		'email': person.email,
		'username': person.username,
		'role': person.role_id
	}
