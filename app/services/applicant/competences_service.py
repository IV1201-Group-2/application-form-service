from sqlalchemy.exc import SQLAlchemyError

from app.models.applicant.competence_profile import CompetenceProfile
from app.repositories.applicant.competences_repository import \
    insert_competences_in_db


def store_applicant_competences(user_id: int, competences: list[dict]) -> dict:
    """
    Store applicant competences in the database.

    This function takes a list of competences and stores them in the database.

    :param user_id: The ID of the user to store the competences for.
    :param competences: A list of competences to store.
    :returns: A dictionary containing the results of the operation.
    """
    successes = []
    failures = []

    for competence in competences:
        try:
            competence_id, experience = __valid_input_competence(competence)
            applicant_competence = CompetenceProfile(user_id, competence_id,
                                                     experience)
            insert_competences_in_db(applicant_competence)
            successes.append(
                    __applicant_competence_to_dict(applicant_competence))
        except (ValueError, SQLAlchemyError) as exception:
            failures.append({'competence_id': competence.get('competence_id'),
                             'error': str(exception)})

    return {'successes': successes, 'failures': failures}


def __applicant_competence_to_dict(
        applicant_competence: CompetenceProfile) -> dict:
    """
    Convert an applicant competence object to a dictionary.

    This function takes an ApplicantCompetence object and converts it into a
    dictionary  containing relevant information.

    :param applicant_competence: The ApplicantCompetence object to convert.
    :returns: A dictionary representation of the applicant competence.
    """

    return {
        'person_id': applicant_competence.person_id,
        'competence_id': applicant_competence.competence_id,
        'years_of_experience': applicant_competence.years_of_experience
    }


def __valid_input_competence(competence: dict) -> tuple[int, float]:
    """
    Validate the input data.

    This function takes a list of competences and checks if the data is valid.

    :param competence: The list of competences to validate.
    :returns: True if the data is valid, False otherwise.
    """

    competence_id_raw = competence.get('competence_id')
    experience_raw = competence.get('experience')

    if competence_id_raw is None or not isinstance(competence_id_raw,
                                                   (int, str)):
        raise ValueError(
                'competence_id is missing or not an int or string')

    if experience_raw is None or not isinstance(experience_raw,
                                                (float, str, int)):
        raise ValueError(
                'experience is missing or not a float, string, or int')

    competence_id = int(competence_id_raw)
    experience = float(experience_raw)

    if competence_id <= 0 or experience < 0.0 or experience > 100.0:
        raise ValueError('Invalid competence ID or experience value')

    return competence_id, experience
