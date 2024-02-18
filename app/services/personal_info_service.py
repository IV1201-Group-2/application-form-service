from app.repositories.personal_info_repository import get_person_from_db


def fetch_personal_info(person_id: int) -> dict[str, str]:
    """
    Fetches personal information for a given user ID.

    This function fetches the personal information of a user from the database
    using their user ID. It then converts the Person object into a dictionary
    and returns it.

    :param person_id: The user ID of the user.
    :returns: A dictionary containing the personal information of the user.
    """

    return get_person_from_db(person_id).to_dict()
